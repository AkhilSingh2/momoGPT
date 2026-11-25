"""
Combined Training Script
Train momoGPT on multiple WhatsApp chat files
"""

import argparse
import json
import os
from parser import WhatsAppParser
from analyzer import PersonalityAnalyzer


def merge_messages(chat_files, target_name):
    """Merge messages from multiple chat files for the same person"""
    all_messages = []
    
    for chat_file in chat_files:
        print(f"🔄 Parsing: {chat_file}")
        parser = WhatsAppParser(chat_file)
        messages = parser.parse()
        
        # Get messages from target person
        target_messages = parser.get_messages_by_sender(target_name)
        
        if not target_messages:
            print(f"⚠️  Warning: No messages from '{target_name}' in {chat_file}")
            print(f"   Available names: {', '.join(parser.participants)}")
            continue
        
        all_messages.extend(target_messages)
        print(f"   ✓ Found {len(target_messages)} messages from {target_name}")
    
    return all_messages


def main():
    parser = argparse.ArgumentParser(description='Train momoGPT on multiple WhatsApp chat files')
    parser.add_argument('--chat-files', nargs='+', required=True, help='Paths to WhatsApp chat export files')
    parser.add_argument('--her-name', required=True, help='Her name as it appears in the chats')
    parser.add_argument('--output-dir', default='.', help='Output directory for generated files')
    
    args = parser.parse_args()
    
    print("="*60)
    print("🚀 momoGPT Combined Training")
    print("="*60)
    
    # Merge messages from all chat files
    all_messages = merge_messages(args.chat_files, args.her_name)
    
    if not all_messages:
        print("\n❌ Error: No messages found from the specified person!")
        return
    
    print(f"\n📊 Total Messages: {len(all_messages)}")
    print(f"   From: {args.her_name}")
    
    # Analyze personality
    print(f"\n🧠 Analyzing personality...")
    analyzer = PersonalityAnalyzer(all_messages)
    profile = analyzer.analyze()
    
    # Save profile
    profile_path = os.path.join(args.output_dir, 'personality.json')
    analyzer.save_profile(profile_path)
    print(f"✓ Saved personality profile to: {profile_path}")
    
    # Generate and save system prompt
    system_prompt = analyzer.generate_system_prompt(args.her_name)
    prompt_path = os.path.join(args.output_dir, 'system_prompt.txt')
    with open(prompt_path, 'w', encoding='utf-8') as f:
        f.write(system_prompt)
    print(f"✓ Saved system prompt to: {prompt_path}")
    
    # Print analysis summary
    print(f"\n✨ Personality Analysis Summary:")
    print(f"\n   Message Style:")
    msg_stats = profile['message_stats']
    print(f"   - Total messages analyzed: {msg_stats['total_messages']}")
    print(f"   - Average message length: {msg_stats['avg_length']:.1f} characters")
    print(f"   - Average words per message: {msg_stats['avg_words']:.1f}")
    
    emoji_data = profile['emoji_usage']
    if emoji_data['uses_emojis']:
        fav_emojis = ' '.join([e[0] for e in emoji_data['favorite_emojis'][:5]])
        print(f"   - Favorite emojis: {fav_emojis}")
    
    punct = profile['punctuation_style']
    enthusiasm = 'High' if punct['enthusiasm_level'] > 0.3 else 'Moderate' if punct['enthusiasm_level'] > 0.1 else 'Low'
    print(f"   - Enthusiasm level: {enthusiasm}")
    
    vocab = profile['vocabulary']
    top_words = ', '.join([w[0] for w in vocab['signature_words'][:8]])
    print(f"   - Signature words: {top_words}")
    
    print(f"\n   Texting Habits:")
    style = profile['texting_style']
    if style['concise']:
        print(f"   - Style: Concise and brief")
    elif style['verbose']:
        print(f"   - Style: Detailed and verbose")
    else:
        print(f"   - Style: Balanced")
    
    if style['expressive']:
        print(f"   - Very expressive with emojis and punctuation")
    
    print(f"\n" + "="*60)
    print(f"✅ Training complete! momoGPT is ready.")
    print(f"="*60)
    print(f"\n   Next steps:")
    print(f"   1. Set up your API key in .env file")
    print(f"      (Add OPENAI_API_KEY or ANTHROPIC_API_KEY)")
    print(f"   2. Run terminal chat: python3 chat.py")
    print(f"   3. Or web interface: python3 app.py")
    print(f"")


if __name__ == '__main__':
    main()


