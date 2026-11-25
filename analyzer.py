"""
Conversation Analyzer
Analyzes texting patterns, style, and personality from chat history
"""

import re
import json
from collections import Counter, defaultdict
from typing import List, Dict
from parser import WhatsAppParser, Message


class PersonalityAnalyzer:
    """Analyze conversation patterns to build personality profile"""
    
    def __init__(self, messages: List[Message]):
        self.messages = messages
        self.profile = {}
        
    def analyze(self) -> Dict:
        """Run all analysis methods"""
        self.profile = {
            'message_stats': self._analyze_message_stats(),
            'vocabulary': self._analyze_vocabulary(),
            'emoji_usage': self._analyze_emojis(),
            'punctuation_style': self._analyze_punctuation(),
            'common_phrases': self._analyze_common_phrases(),
            'response_patterns': self._analyze_response_patterns(),
            'topics': self._analyze_topics(),
            'texting_style': self._analyze_texting_style(),
        }
        
        return self.profile
    
    def _analyze_message_stats(self) -> Dict:
        """Analyze basic message statistics"""
        lengths = [len(msg.text) for msg in self.messages]
        word_counts = [len(msg.text.split()) for msg in self.messages]
        
        return {
            'total_messages': len(self.messages),
            'avg_length': sum(lengths) / len(lengths) if lengths else 0,
            'avg_words': sum(word_counts) / len(word_counts) if word_counts else 0,
            'median_length': sorted(lengths)[len(lengths) // 2] if lengths else 0,
            'short_messages': sum(1 for l in lengths if l < 20),
            'long_messages': sum(1 for l in lengths if l > 100),
        }
    
    def _analyze_vocabulary(self) -> Dict:
        """Analyze vocabulary and common words"""
        all_text = ' '.join(msg.text.lower() for msg in self.messages)
        words = re.findall(r'\b[a-z]+\b', all_text)
        
        word_freq = Counter(words)
        
        # Remove common stopwords
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                    'of', 'with', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
                    'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'}
        
        unique_words = {word: count for word, count in word_freq.items() 
                       if word not in stopwords and len(word) > 2}
        
        return {
            'unique_words': len(word_freq),
            'most_common': word_freq.most_common(30),
            'signature_words': sorted(unique_words.items(), key=lambda x: x[1], reverse=True)[:20],
        }
    
    def _analyze_emojis(self) -> Dict:
        """Analyze emoji usage patterns"""
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "\U0001F900-\U0001F9FF"  # supplemental symbols
            "\U0001FA00-\U0001FA6F"  # extended symbols
            "]+", 
            flags=re.UNICODE
        )
        
        all_emojis = []
        messages_with_emojis = 0
        
        for msg in self.messages:
            emojis = emoji_pattern.findall(msg.text)
            if emojis:
                all_emojis.extend(emojis)
                messages_with_emojis += 1
        
        emoji_freq = Counter(all_emojis)
        
        return {
            'total_emojis': len(all_emojis),
            'emoji_frequency': messages_with_emojis / len(self.messages) if self.messages else 0,
            'favorite_emojis': emoji_freq.most_common(15),
            'uses_emojis': messages_with_emojis > len(self.messages) * 0.1,  # Uses emojis in 10%+ of messages
        }
    
    def _analyze_punctuation(self) -> Dict:
        """Analyze punctuation style"""
        exclamation_count = sum(msg.text.count('!') for msg in self.messages)
        question_count = sum(msg.text.count('?') for msg in self.messages)
        period_count = sum(msg.text.count('.') for msg in self.messages)
        ellipsis_count = sum(msg.text.count('...') for msg in self.messages)
        
        all_caps_msgs = sum(1 for msg in self.messages 
                           if len(msg.text) > 5 and msg.text.isupper())
        
        return {
            'exclamation_marks': exclamation_count,
            'question_marks': question_count,
            'periods': period_count,
            'ellipsis': ellipsis_count,
            'all_caps_messages': all_caps_msgs,
            'enthusiasm_level': exclamation_count / len(self.messages) if self.messages else 0,
        }
    
    def _analyze_common_phrases(self) -> Dict:
        """Find common phrases and expressions"""
        all_text = [msg.text.lower() for msg in self.messages]
        
        # Common greetings
        greetings = ['hi', 'hey', 'hello', 'hii', 'hiii', 'yo', 'sup', 'heyyy']
        greeting_count = sum(1 for text in all_text 
                           for greeting in greetings 
                           if greeting in text.split())
        
        # Common sign-offs
        signoffs = ['bye', 'goodnight', 'good night', 'gn', 'ttyl', 'talk later', 'love you', 'ly']
        signoff_count = sum(1 for text in all_text 
                          for signoff in signoffs 
                          if signoff in text.lower())
        
        # Laughs
        laughs = ['haha', 'lol', 'lmao', 'hehe', 'hahaha', 'lmfao', 'rofl', '😂']
        laugh_count = sum(1 for text in all_text 
                         for laugh in laughs 
                         if laugh in text.lower())
        
        # Find repeated phrases (simple n-grams)
        phrases = []
        for msg in self.messages:
            words = msg.text.lower().split()
            for i in range(len(words) - 2):
                phrases.append(' '.join(words[i:i+3]))
        
        phrase_freq = Counter(phrases)
        
        return {
            'uses_greetings': greeting_count > 0,
            'greeting_frequency': greeting_count / len(self.messages) if self.messages else 0,
            'uses_signoffs': signoff_count > 0,
            'laugh_frequency': laugh_count / len(self.messages) if self.messages else 0,
            'common_phrases': [p for p, c in phrase_freq.most_common(10) if c > 2],
        }
    
    def _analyze_response_patterns(self) -> Dict:
        """Analyze how messages are structured"""
        single_word_msgs = sum(1 for msg in self.messages if len(msg.text.split()) == 1)
        multi_message_ratio = 0  # Would need timestamp analysis
        
        # Questions asked
        questions = sum(1 for msg in self.messages if '?' in msg.text)
        
        return {
            'single_word_messages': single_word_msgs,
            'single_word_ratio': single_word_msgs / len(self.messages) if self.messages else 0,
            'asks_questions': questions > len(self.messages) * 0.05,
            'question_frequency': questions / len(self.messages) if self.messages else 0,
        }
    
    def _analyze_topics(self) -> List[str]:
        """Identify common topics (simple keyword-based)"""
        all_text = ' '.join(msg.text.lower() for msg in self.messages)
        
        topic_keywords = {
            'work': ['work', 'job', 'office', 'boss', 'meeting', 'project'],
            'food': ['eat', 'food', 'lunch', 'dinner', 'breakfast', 'hungry', 'restaurant'],
            'plans': ['tomorrow', 'tonight', 'weekend', 'later', 'meet', 'going'],
            'feelings': ['love', 'miss', 'feel', 'happy', 'sad', 'excited', 'tired'],
            'questions': ['what', 'when', 'where', 'why', 'how', 'who'],
        }
        
        topics = []
        for topic, keywords in topic_keywords.items():
            if any(keyword in all_text for keyword in keywords):
                topics.append(topic)
        
        return topics
    
    def _analyze_texting_style(self) -> Dict:
        """Determine overall texting style"""
        stats = self._analyze_message_stats()
        emoji_data = self._analyze_emojis()
        punct_data = self._analyze_punctuation()
        
        style = {
            'concise': stats['avg_length'] < 50,
            'verbose': stats['avg_length'] > 150,
            'expressive': emoji_data['uses_emojis'] or punct_data['enthusiasm_level'] > 0.3,
            'casual': True,  # Most chat is casual
            'uses_abbreviations': False,  # Would need more sophisticated analysis
        }
        
        return style
    
    def generate_system_prompt(self, name: str = "Momo") -> str:
        """Generate a system prompt based on the personality analysis"""
        stats = self.profile.get('message_stats', {})
        emoji_data = self.profile.get('emoji_usage', {})
        punct = self.profile.get('punctuation_style', {})
        phrases = self.profile.get('common_phrases', {})
        style = self.profile.get('texting_style', {})
        vocab = self.profile.get('vocabulary', {})
        
        prompt_parts = [
            f"You are {name}, texting your boyfriend. Reply exactly as {name} would - match her personality, style, and way of texting.",
            "\n\n**Texting Style:**"
        ]
        
        # Message length
        avg_len = stats.get('avg_length', 50)
        if avg_len < 30:
            prompt_parts.append("- Keep messages SHORT and concise (usually 1-2 sentences)")
        elif avg_len < 80:
            prompt_parts.append("- Send medium-length messages (2-4 sentences)")
        else:
            prompt_parts.append("- Often send longer, detailed messages")
        
        # Emoji usage
        if emoji_data.get('uses_emojis'):
            fav_emojis = [e[0] for e in emoji_data.get('favorite_emojis', [])[:5]]
            if fav_emojis:
                prompt_parts.append(f"- Use emojis frequently, especially: {' '.join(fav_emojis)}")
        else:
            prompt_parts.append("- Rarely use emojis")
        
        # Punctuation
        enthusiasm = punct.get('enthusiasm_level', 0)
        if enthusiasm > 0.3:
            prompt_parts.append("- Very enthusiastic - use exclamation marks often!")
        elif enthusiasm > 0.1:
            prompt_parts.append("- Moderately enthusiastic, occasional exclamation marks")
        
        # Expressions
        if phrases.get('laugh_frequency', 0) > 0.1:
            prompt_parts.append("- Laugh often in texts (haha, lol)")
        
        # Common words/phrases
        signature_words = vocab.get('signature_words', [])[:10]
        if signature_words:
            words_list = ', '.join([w[0] for w in signature_words[:5]])
            prompt_parts.append(f"- Favorite words: {words_list}")
        
        # Overall personality
        prompt_parts.append("\n**Personality Traits:**")
        if style.get('expressive'):
            prompt_parts.append("- Expressive and emotionally open")
        if style.get('concise'):
            prompt_parts.append("- Direct and to-the-point")
        if phrases.get('asks_questions'):
            prompt_parts.append("- Curious, asks questions")
        
        prompt_parts.append("\n**Important Rules:**")
        prompt_parts.append("- Reply naturally as if you're in a real conversation")
        prompt_parts.append("- Match the energy and tone of the messages you receive")
        prompt_parts.append("- Don't be overly formal or robotic")
        prompt_parts.append("- You're his girlfriend - be warm, genuine, and authentic")
        prompt_parts.append(f"- Respond exactly how {name} would text")
        
        return '\n'.join(prompt_parts)
    
    def save_profile(self, filepath: str):
        """Save personality profile to JSON"""
        # Convert Counter objects to lists for JSON serialization
        profile_copy = json.loads(json.dumps(self.profile, default=str))
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(profile_copy, f, indent=2, ensure_ascii=False)
    
    def load_profile(self, filepath: str):
        """Load personality profile from JSON"""
        with open(filepath, 'r', encoding='utf-8') as f:
            self.profile = json.load(f)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python analyzer.py <chat_file> <her_name>")
        sys.exit(1)
    
    chat_file = sys.argv[1]
    her_name = sys.argv[2]
    
    # Parse chat
    parser = WhatsAppParser(chat_file)
    messages = parser.parse()
    
    # Get her messages only
    her_messages = parser.get_messages_by_sender(her_name)
    
    print(f"Analyzing {len(her_messages)} messages from {her_name}...")
    
    # Analyze
    analyzer = PersonalityAnalyzer(her_messages)
    profile = analyzer.analyze()
    
    print("\n=== Personality Analysis ===\n")
    print(json.dumps(profile, indent=2, default=str))
    
    print("\n=== Generated System Prompt ===\n")
    print(analyzer.generate_system_prompt(her_name))

