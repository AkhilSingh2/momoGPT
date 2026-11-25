"""
MomoGPT Chatbot Engine
Handles conversation with personality-aware AI
"""

import os
from typing import List, Dict, Optional


class MomoGPT:
    """Chatbot that mimics personality based on analyzed conversation patterns"""
    
    def __init__(self, system_prompt: str, model: str = "auto"):
        """
        Initialize momoGPT
        
        Args:
            system_prompt: Personality and style instructions
            model: "gpt-4", "gpt-3.5-turbo", "claude", or "auto" (detect from env)
        """
        self.system_prompt = system_prompt
        self.conversation_history: List[Dict] = []
        
        # Auto-detect which API is available
        if model == "auto":
            if os.getenv('OPENAI_API_KEY'):
                model = "gpt-4"
            elif os.getenv('ANTHROPIC_API_KEY'):
                model = "claude"
            else:
                raise ValueError("No API key found. Set OPENAI_API_KEY or ANTHROPIC_API_KEY in .env")
        
        self.model = model
        
        # Initialize API client
        if model.startswith('gpt'):
            from openai import OpenAI
            self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            self.api_type = 'openai'
        elif model == 'claude':
            from anthropic import Anthropic
            self.client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
            self.api_type = 'anthropic'
            # Claude uses different model names
            self.model = 'claude-3-5-sonnet-20241022'
        else:
            raise ValueError(f"Unknown model: {model}")
    
    def chat(self, message: str) -> str:
        """
        Send a message and get a response
        
        Args:
            message: User's message
            
        Returns:
            Bot's response
        """
        # Add user message to history
        self.conversation_history.append({
            'role': 'user',
            'content': message
        })
        
        # Get response based on API type
        if self.api_type == 'openai':
            response = self._chat_openai()
        else:
            response = self._chat_anthropic()
        
        # Add assistant response to history
        self.conversation_history.append({
            'role': 'assistant',
            'content': response
        })
        
        return response
    
    def _chat_openai(self) -> str:
        """Get response from OpenAI API"""
        messages = [
            {'role': 'system', 'content': self.system_prompt}
        ] + self.conversation_history
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.8,  # Slightly random for natural variation
            max_tokens=300,
        )
        
        return response.choices[0].message.content.strip()
    
    def _chat_anthropic(self) -> str:
        """Get response from Anthropic API"""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=300,
            temperature=0.8,
            system=self.system_prompt,
            messages=self.conversation_history
        )
        
        return response.content[0].text.strip()
    
    def reset_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_history(self) -> List[Dict]:
        """Get conversation history"""
        return self.conversation_history
    
    def set_temperature(self, temperature: float):
        """Adjust response randomness (0.0 - 1.0)"""
        self.temperature = temperature


if __name__ == '__main__':
    # Test the chatbot
    import sys
    from dotenv import load_dotenv
    
    load_dotenv()
    
    if not os.path.exists('system_prompt.txt'):
        print("Create a system_prompt.txt file first!")
        sys.exit(1)
    
    with open('system_prompt.txt', 'r') as f:
        prompt = f.read()
    
    bot = MomoGPT(prompt)
    
    print("Test chat:")
    print(bot.chat("hey babe, how was your day?"))

