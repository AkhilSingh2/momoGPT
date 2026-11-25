"""
Chat Interface (Command Line)
Chat with momoGPT via terminal
"""

import os
import sys
from dotenv import load_dotenv
from chatbot import MomoGPT


def main():
    load_dotenv()
    
    # Check for system prompt
    if not os.path.exists('system_prompt.txt'):
        print("⚠️  System prompt not found!")
        print("   Please run: python train.py --chat-file <file> --her-name <name>")
        sys.exit(1)
    
    # Load system prompt
    with open('system_prompt.txt', 'r', encoding='utf-8') as f:
        system_prompt = f.read()
    
    # Initialize chatbot
    try:
        bot = MomoGPT(system_prompt)
        print("✅ momoGPT loaded successfully!")
    except Exception as e:
        print(f"❌ Error initializing momoGPT: {e}")
        print("\nMake sure you have:")
        print("  1. Created a .env file with OPENAI_API_KEY or ANTHROPIC_API_KEY")
        print("  2. Installed dependencies: pip install -r requirements.txt")
        sys.exit(1)
    
    print("\n" + "="*50)
    print("💬 Chat with momoGPT")
    print("="*50)
    print("Type 'quit' or 'exit' to end the conversation")
    print("Type 'reset' to start a new conversation")
    print("="*50 + "\n")
    
    # Chat loop
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\n👋 Goodbye!")
                break
            
            if user_input.lower() == 'reset':
                bot.reset_conversation()
                print("🔄 Conversation reset!\n")
                continue
            
            # Get response
            response = bot.chat(user_input)
            print(f"\nMomo: {response}\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == '__main__':
    main()

