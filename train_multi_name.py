"""
Multi-Name Training Script
Train momoGPT on multiple chat files where the same person has different names
"""

import argparse
import json
import os
from parser import WhatsAppParser
from analyzer import PersonalityAnalyzer


def merge_messages_multi_name(chat_configs):
    """
    Merge messages from multiple chat files where person has different names
    chat_configs: list of tuples (chat_file, name_in_that_chat)
    """
    all_messages = []
    
    for chat_file, target_name in chat_configs:
        print(f"🔄 Parsing: {chat_file} (looking for '{target_name}')")
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
    ap = argparse.ArgumentParser(
        description="Train on several chat exports where the same person appears under different names")
    ap.add_argument("--chat", action="append", required=True, metavar="FILE:NAME",
                    help="chat export and the person's name in it, e.g. chat1.txt:Momo (repeatable)")
    ap.add_argument("--display-name", default="Momo", help="name the chatbot uses")
    args = ap.parse_args()
    chat_configs = []
    for item in args.chat:
        file_name, _, person = item.partition(":")
        if not person:
            ap.error(f"--chat expects FILE:NAME, got {item!r}")
        chat_configs.append((file_name, person))

    display_name = args.display_name
    
    print("="*60)
    print("🚀 momoGPT Multi-Chat Training")
    print("="*60)
    print(f"Training on: {display_name}")
    print(f"Combining messages from {len(chat_configs)} chat files...")
    print()
    
    # Merge messages from all chat files
    all_messages = merge_messages_multi_name(chat_configs)
    
    if not all_messages:
        print("\n❌ Error: No messages found!")
        return
    
    print(f"\n📊 Total Messages Combined: {len(all_messages)}")
    
    # Analyze personality
    print(f"\n🧠 Analyzing personality...")
    analyzer = PersonalityAnalyzer(all_messages)
    profile = analyzer.analyze()
    
    # Save profile
    profile_path = 'personality.json'
    analyzer.save_profile(profile_path)
    print(f"✓ Saved personality profile to: {profile_path}")
    
    # Generate and save system prompt
    system_prompt = analyzer.generate_system_prompt(display_name)
    prompt_path = 'system_prompt.txt'
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
        fav_emojis = ' '.join([e[0] for e in emoji_data['favorite_emojis'][:8]])
        print(f"   - Uses emojis frequently")
        print(f"   - Favorite emojis: {fav_emojis}")
    else:
        print(f"   - Rarely uses emojis")
    
    punct = profile['punctuation_style']
    enthusiasm = 'High' if punct['enthusiasm_level'] > 0.3 else 'Moderate' if punct['enthusiasm_level'] > 0.1 else 'Low'
    print(f"   - Enthusiasm level: {enthusiasm}")
    
    vocab = profile['vocabulary']
    # Filter out common filler words
    sig_words = [w[0] for w in vocab['signature_words'][:15] 
                 if w[0] not in ['omitted', 'am', 'pm', 'i', 'you', 'it', 'u', 't']][:8]
    if sig_words:
        print(f"   - Signature words: {', '.join(sig_words)}")
    
    phrases = profile['common_phrases']
    if phrases.get('laugh_frequency', 0) > 0.05:
        print(f"   - Laughs in texts frequently")
    
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
    print(f"✅ Training complete! {display_name}GPT is ready.")
    print(f"="*60)
    print(f"\n   Next steps:")
    print(f"   1. Set up your API key in .env file")
    print(f"      Edit .env and add:")
    print(f"      OPENAI_API_KEY=your_key_here")
    print(f"      OR")
    print(f"      ANTHROPIC_API_KEY=your_key_here")
    print(f"")
    print(f"   2. Run terminal chat:")
    print(f"      python3 chat.py")
    print(f"")
    print(f"   3. Or launch web interface:")
    print(f"      python3 app.py")
    print(f"      Then open: http://localhost:5000")
    print(f"")


if __name__ == '__main__':
    main()


