"""
Training Script
Parse chat history, analyze personality, and prepare momoGPT
"""

import argparse
import json
import os
from parser import WhatsAppParser
from analyzer import PersonalityAnalyzer


def export_finetuning_data(parser: WhatsAppParser, your_name: str, her_name: str, output_file: str):
    """Export conversation pairs in OpenAI fine-tuning format"""
    pairs = parser.get_conversation_pairs(your_name, her_name)
    
    finetuning_data = []
    
    for pair in pairs:
        # OpenAI fine-tuning format (for gpt-3.5-turbo or gpt-4)
        finetuning_data.append({
            "messages": [
                {"role": "user", "content": pair['prompt']},
                {"role": "assistant", "content": pair['response']}
            ]
        })
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in finetuning_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    print(f"✓ Exported {len(finetuning_data)} conversation pairs to {output_file}")
    print(f"  Upload this file to OpenAI for fine-tuning: https://platform.openai.com/finetune")


def main():
    parser = argparse.ArgumentParser(description='Train momoGPT on WhatsApp chat history')
    parser.add_argument('--chat-file', required=True, help='Path to WhatsApp chat export file')
    parser.add_argument('--name', '--her-name', dest='her_name', required=True, help="The person's name exactly as it appears in the chat")
    parser.add_argument('--your-name', help='Your name as it appears in the chat (for fine-tuning export)')
    parser.add_argument('--export-finetuning', action='store_true', help='Export data for fine-tuning')
    parser.add_argument('--output-dir', default='.', help='Output directory for generated files')
    
    args = parser.parse_args()
    
    print(f"🔄 Parsing WhatsApp chat from: {args.chat_file}")
    
    # Parse chat
    chat_parser = WhatsAppParser(args.chat_file)
    messages = chat_parser.parse()
    
    stats = chat_parser.get_stats()
    print(f"\n📊 Chat Statistics:")
    print(f"   Total messages: {stats['total_messages']}")
    print(f"   Participants: {', '.join(stats['participants'])}")
    print(f"   Date range: {stats['date_range']['start']} to {stats['date_range']['end']}")
    
    # Verify her name
    if args.her_name not in chat_parser.participants:
        print(f"\n⚠️  Warning: '{args.her_name}' not found in participants!")
        print(f"   Available names: {', '.join(chat_parser.participants)}")
        print(f"   Make sure the name matches exactly as it appears in the chat.")
        return
    
    # Get her messages
    her_messages = chat_parser.get_messages_by_sender(args.her_name)
    print(f"\n📱 Analyzing {len(her_messages)} messages from {args.her_name}...")
    
    # Analyze personality
    analyzer = PersonalityAnalyzer(her_messages)
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
    print(f"   - Average message length: {msg_stats['avg_length']:.1f} characters")
    print(f"   - Average words per message: {msg_stats['avg_words']:.1f}")
    
    emoji_data = profile['emoji_usage']
    if emoji_data['uses_emojis']:
        fav_emojis = ' '.join([e[0] for e in emoji_data['favorite_emojis'][:5]])
        print(f"   - Favorite emojis: {fav_emojis}")
    
    punct = profile['punctuation_style']
    print(f"   - Enthusiasm level: {'High' if punct['enthusiasm_level'] > 0.3 else 'Moderate' if punct['enthusiasm_level'] > 0.1 else 'Low'}")
    
    vocab = profile['vocabulary']
    top_words = ', '.join([w[0] for w in vocab['signature_words'][:5]])
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
    
    # Export fine-tuning data if requested
    if args.export_finetuning:
        if not args.your_name:
            print(f"\n⚠️  --your-name is required for fine-tuning export")
            print(f"   Available names: {', '.join(chat_parser.participants)}")
        else:
            finetuning_path = os.path.join(args.output_dir, 'finetuning_data.jsonl')
            export_finetuning_data(chat_parser, args.your_name, args.her_name, finetuning_path)
    
    print(f"\n✅ Training complete! momoGPT is ready.")
    print(f"\n   Next steps:")
    print(f"   1. Review the system prompt in: {prompt_path}")
    print(f"   2. Set up your API key in .env file")
    print(f"   3. Run: python chat.py")


if __name__ == '__main__':
    main()

