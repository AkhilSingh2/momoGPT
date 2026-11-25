"""
MomoGPT Chatbot Engine - FREE VERSION
Handles conversation with personality-aware AI using free models
Supports: Ollama (local), Groq (cloud), OpenRouter (cloud)
"""

import os
import sys
from typing import List, Dict


class MomoGPT:
    """Chatbot that mimics personality using FREE AI models"""
    
    def __init__(self, system_prompt: str):
        """
        Initialize momoGPT with free AI backend
        
        Args:
            system_prompt: Personality and style instructions
        """
        self.system_prompt = system_prompt
        self.conversation_history: List[Dict] = []
        self.temperature = 0.8
        
        # Auto-detect which free AI service to use
        self._initialize_client()
    
    def _initialize_client(self):
        """Auto-detect and initialize the best available free AI service"""
        
        # Priority 1: Check for Ollama (local, private, unlimited)
        if self._check_ollama():
            self.backend = 'ollama'
            self.model = 'llama3.2'
            print(f"✅ Using Ollama (Local AI) - Model: {self.model}")
            return
        
        # Priority 2: Check for Groq (fast cloud API)
        groq_key = os.getenv('GROQ_API_KEY')
        if groq_key:
            try:
                from groq import Groq
                self.client = Groq(api_key=groq_key)
                self.backend = 'groq'
                self.model = 'llama-3.1-8b-instant'  # Fast and free
                print(f"✅ Using Groq (Cloud AI) - Model: {self.model}")
                return
            except ImportError:
                print("⚠️  Groq API key found but 'groq' package not installed.")
                print("   Run: pip install groq")
        
        # Priority 3: Check for OpenRouter
        openrouter_key = os.getenv('OPENROUTER_API_KEY')
        if openrouter_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=openrouter_key
                )
                self.backend = 'openrouter'
                self.model = 'meta-llama/llama-3.2-3b-instruct:free'  # Free model
                print(f"✅ Using OpenRouter (Cloud AI) - Model: {self.model}")
                return
            except ImportError:
                print("⚠️  OpenRouter API key found but 'openai' package not installed.")
        
        # No free AI service available
        raise ValueError(
            "❌ No free AI service available!\n\n"
            "Please set up one of these FREE options:\n\n"
            "1. OLLAMA (Recommended - 100% free, private):\n"
            "   - Install: https://ollama.ai\n"
            "   - Run: ollama serve\n"
            "   - Pull model: ollama pull llama3.2\n\n"
            "2. GROQ (Fast cloud API - free):\n"
            "   - Get key: https://console.groq.com\n"
            "   - Add to .env: GROQ_API_KEY=your_key\n"
            "   - Install: pip install groq\n\n"
            "3. OPENROUTER (Multiple free models):\n"
            "   - Get key: https://openrouter.ai\n"
            "   - Add to .env: OPENROUTER_API_KEY=your_key\n\n"
            "See FREE_AI_SETUP.md for detailed instructions."
        )
    
    def _check_ollama(self) -> bool:
        """Check if Ollama is running and available"""
        try:
            import requests
            response = requests.get('http://localhost:11434/api/tags', timeout=2)
            return response.status_code == 200
        except:
            return False
    
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
        
        # Get response based on backend
        if self.backend == 'ollama':
            response = self._chat_ollama()
        elif self.backend == 'groq':
            response = self._chat_groq()
        elif self.backend == 'openrouter':
            response = self._chat_openrouter()
        else:
            raise ValueError(f"Unknown backend: {self.backend}")
        
        # Add assistant response to history
        self.conversation_history.append({
            'role': 'assistant',
            'content': response
        })
        
        return response
    
    def _chat_ollama(self) -> str:
        """Get response from Ollama (local)"""
        import requests
        
        # Ollama API format
        messages = [
            {'role': 'system', 'content': self.system_prompt}
        ] + self.conversation_history
        
        try:
            response = requests.post(
                'http://localhost:11434/api/chat',
                json={
                    'model': self.model,
                    'messages': messages,
                    'stream': False,
                    'options': {
                        'temperature': self.temperature,
                        'num_predict': 300,
                    }
                },
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            return result['message']['content'].strip()
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                "Cannot connect to Ollama. Make sure it's running:\n"
                "  1. Open a terminal and run: ollama serve\n"
                "  2. Make sure you've pulled a model: ollama pull llama3.2"
            )
        except Exception as e:
            raise Exception(f"Ollama error: {e}")
    
    def _chat_groq(self) -> str:
        """Get response from Groq API"""
        messages = [
            {'role': 'system', 'content': self.system_prompt}
        ] + self.conversation_history
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=300,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"Groq API error: {e}")
    
    def _chat_openrouter(self) -> str:
        """Get response from OpenRouter API"""
        messages = [
            {'role': 'system', 'content': self.system_prompt}
        ] + self.conversation_history
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=300,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"OpenRouter API error: {e}")
    
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
    from dotenv import load_dotenv
    
    load_dotenv()
    
    if not os.path.exists('system_prompt.txt'):
        print("Create a system_prompt.txt file first!")
        sys.exit(1)
    
    with open('system_prompt.txt', 'r') as f:
        prompt = f.read()
    
    try:
        bot = MomoGPT(prompt)
        print("\nTest chat:")
        print("You: hey, how's it going?")
        response = bot.chat("hey, how's it going?")
        print(f"Bot: {response}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


