"""
Terminal Chat Interface - FREE VERSION
Interactive chat with momoGPT using free AI models
"""

import os
import sys
from dotenv import load_dotenv
from chatbot_local import MomoGPT

load_dotenv()


def main():
    """Run the chat interface"""
    
    # Load system prompt
    if not os.path.exists('system_prompt.txt'):
        print("❌ Error: system_prompt.txt not found!")
        print("   Run the training script first: python3 train_multi_name.py")
        sys.exit(1)
    
    with open('system_prompt.txt', 'r', encoding='utf-8') as f:
        system_prompt = f.read()
    
    # Extract bot name from prompt
    bot_name = "Momo"
    if "You are " in system_prompt:
        try:
            bot_name = system_prompt.split("You are ")[1].split(",")[0].strip()
        except:
            pass
    
    print("\n" + "="*60)
    print(f"💬 {bot_name}GPT - FREE AI Chat Interface")
    print("="*60)
    print(f"Using: 100% FREE Local/Cloud AI")
    print("Type 'quit' or 'exit' to end the conversation")
    print("Type 'reset' to start a new conversation")
    print("="*60 + "\n")
    
    # Initialize bot
    try:
        bot = MomoGPT(system_prompt)
    except Exception as e:
        print(f"❌ Error initializing AI: {e}")
        sys.exit(1)
    
    # Chat loop
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Check for commands
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print(f"\n{bot_name}: Bye! 👋\n")
                break
            
            if user_input.lower() == 'reset':
                bot.reset_conversation()
                print(f"\n🔄 Conversation reset!\n")
                continue
            
            # Get bot response
            response = bot.chat(user_input)
            
            # Print response
            print(f"\n{bot_name}: {response}\n")
            
        except KeyboardInterrupt:
            print(f"\n\n{bot_name}: Bye! 👋\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")
            continue


if __name__ == '__main__':
    main()



