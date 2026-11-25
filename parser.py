"""
WhatsApp Chat Parser
Extracts and structures conversations from WhatsApp export files
"""

import re
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class Message:
    """Represents a single message in the conversation"""
    timestamp: datetime
    sender: str
    text: str
    is_system: bool = False


class WhatsAppParser:
    """Parse WhatsApp chat export files"""
    
    # WhatsApp export formats vary by region
    # Common patterns:
    # [DD/MM/YYYY, HH:MM:SS] Name: Message
    # DD/MM/YYYY, HH:MM - Name: Message
    # M/D/YY, H:MM AM/PM - Name: Message
    
    PATTERNS = [
        # [09/10/25, 2:02:53 AM] Name: Message
        r'\[(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2}\s[AP]M)\]\s([^:]+):\s(.+)',
        # [12/31/2024, 14:30:45] Name: Message
        r'\[(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2})\]\s([^:]+):\s(.+)',
        # 12/09/24, 22:01 - Name: Message (no seconds)
        r'(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2})\s-\s([^:]+):\s(.+)',
        # 12/31/24, 2:30 PM - Name: Message (with AM/PM)
        r'(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[AP]M)\s-\s([^:]+):\s(.+)',
        # [2024-12-31, 14:30:45] Name: Message
        r'\[(\d{4}-\d{2}-\d{2},\s\d{2}:\d{2}:\d{2})\]\s([^:]+):\s(.+)',
    ]
    
    DATE_FORMATS = [
        '%m/%d/%y, %I:%M:%S %p',  # 09/10/25, 2:02:53 AM
        '%d/%m/%y, %I:%M:%S %p',  # 09/10/25, 2:02:53 AM (EU)
        '%m/%d/%Y, %I:%M %p',  # US format with AM/PM (most common)
        '%d/%m/%Y, %I:%M %p',  # EU format with AM/PM
        '%m/%d/%Y, %H:%M:%S',
        '%d/%m/%Y, %H:%M:%S',
        '%m/%d/%Y, %H:%M',
        '%d/%m/%Y, %H:%M',
        '%m/%d/%y, %H:%M',  # 12/09/24, 22:01
        '%d/%m/%y, %H:%M',  # 12/09/24, 22:01 (EU)
        '%m/%d/%y, %I:%M %p',
        '%d/%m/%y, %I:%M %p',
        '%Y-%m-%d, %H:%M:%S',
    ]
    
    def __init__(self, chat_file: str):
        self.chat_file = chat_file
        self.messages: List[Message] = []
        self.participants: set = set()
        
    def parse(self) -> List[Message]:
        """Parse the WhatsApp chat file"""
        with open(self.chat_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        current_message = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Try to match message pattern
            message_data = self._parse_line(line)
            
            if message_data:
                # Save previous message if exists
                if current_message:
                    self.messages.append(current_message)
                
                timestamp, sender, text = message_data
                
                # Check if it's a system message
                is_system = self._is_system_message(text)
                
                current_message = Message(
                    timestamp=timestamp,
                    sender=sender.strip(),
                    text=text.strip(),
                    is_system=is_system
                )
                
                if not is_system:
                    self.participants.add(sender.strip())
            else:
                # Continuation of previous message (multiline)
                if current_message:
                    current_message.text += '\n' + line
        
        # Add last message
        if current_message:
            self.messages.append(current_message)
        
        return self.messages
    
    def _parse_line(self, line: str) -> Optional[tuple]:
        """Try to parse a line with different patterns"""
        for pattern in self.PATTERNS:
            match = re.match(pattern, line)
            if match:
                timestamp_str, sender, text = match.groups()
                timestamp = self._parse_timestamp(timestamp_str)
                if timestamp:
                    return timestamp, sender, text
        return None
    
    def _parse_timestamp(self, timestamp_str: str) -> Optional[datetime]:
        """Try to parse timestamp with different formats"""
        for date_format in self.DATE_FORMATS:
            try:
                return datetime.strptime(timestamp_str, date_format)
            except ValueError:
                continue
        return None
    
    def _is_system_message(self, text: str) -> bool:
        """Check if message is a system message"""
        system_keywords = [
            'created group',
            'added',
            'left',
            'removed',
            'changed the subject',
            'changed this group',
            'changed the group',
            'You deleted this message',
            'This message was deleted',
            'Waiting for this message',  # Deleted messages
            'Messages and calls are end-to-end encrypted',
            'security code changed',
            'is a contact',
            '<Media omitted>',
            'file attached',
            'Missed voice call',
            'Tap to call back',
        ]
        
        text_lower = text.lower()
        return any(keyword.lower() in text_lower for keyword in system_keywords)
    
    def get_messages_by_sender(self, sender: str) -> List[Message]:
        """Get all messages from a specific sender"""
        return [msg for msg in self.messages if msg.sender == sender and not msg.is_system]
    
    def get_conversation_pairs(self, person1: str, person2: str) -> List[Dict]:
        """Extract conversation pairs (turn-taking between two people)"""
        pairs = []
        filtered_messages = [msg for msg in self.messages if not msg.is_system]
        
        for i in range(len(filtered_messages) - 1):
            current = filtered_messages[i]
            next_msg = filtered_messages[i + 1]
            
            # Create pairs where person1 speaks, then person2 responds
            if current.sender == person1 and next_msg.sender == person2:
                pairs.append({
                    'prompt': current.text,
                    'response': next_msg.text,
                    'timestamp': next_msg.timestamp
                })
        
        return pairs
    
    def get_stats(self) -> Dict:
        """Get conversation statistics"""
        non_system = [msg for msg in self.messages if not msg.is_system]
        
        stats = {
            'total_messages': len(non_system),
            'participants': list(self.participants),
            'date_range': {
                'start': min(msg.timestamp for msg in non_system) if non_system else None,
                'end': max(msg.timestamp for msg in non_system) if non_system else None,
            }
        }
        
        # Per-person stats
        for participant in self.participants:
            participant_msgs = self.get_messages_by_sender(participant)
            stats[participant] = {
                'message_count': len(participant_msgs),
                'avg_length': sum(len(msg.text) for msg in participant_msgs) / len(participant_msgs) if participant_msgs else 0,
            }
        
        return stats


if __name__ == '__main__':
    # Test the parser
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python parser.py <chat_file>")
        sys.exit(1)
    
    parser = WhatsAppParser(sys.argv[1])
    messages = parser.parse()
    
    print(f"Parsed {len(messages)} messages")
    print(f"Participants: {parser.participants}")
    print("\nStats:")
    
    stats = parser.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")

