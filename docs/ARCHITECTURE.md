# momoGPT - Project Summary

## 🎯 What This Does

**momoGPT** is a personalized AI chatbot that learns a person's texting style from WhatsApp conversations and replicates it. It analyzes her vocabulary, emoji usage, message length, punctuation patterns, and personality traits to create an AI that texts just like her.

## ✨ Key Features

### 1. **Smart WhatsApp Parser** (`parser.py`)
- Reads WhatsApp chat exports (handles multiple date formats)
- Extracts conversations and metadata
- Filters system messages
- Creates conversation pairs for training

### 2. **Personality Analyzer** (`analyzer.py`)
- Analyzes texting style patterns:
  - Message length and structure
  - Emoji preferences and frequency
  - Punctuation style (enthusiasm, questions)
  - Common words and phrases
  - Response patterns
- Generates personality profile (JSON)
- Creates custom AI system prompt

### 3. **AI Chatbot Engine** (`chatbot.py`)
- Works with OpenAI (GPT-3.5/GPT-4) or Anthropic (Claude)
- Personality-aware responses
- Maintains conversation context
- Adjustable temperature for response variety

### 4. **Interactive Interfaces**
- **Terminal Chat** (`chat.py`): Simple command-line interface
- **Web Interface** (`app.py` + `templates/chat.html`): Beautiful, modern UI with:
  - Real-time chat
  - Typing indicators
  - Conversation history
  - Reset functionality
  - Responsive design

### 5. **Training Tools** (`train.py`)
- One-command training pipeline
- Exports fine-tuning datasets for advanced users
- Validation and error checking
- Detailed analysis reports

### 6. **Easy Setup** (`quickstart.sh`)
- Interactive setup wizard
- Automatic dependency installation
- API key configuration
- Guided training process

## 📂 Project Structure

```
momoGPT/
├── README.md              # Overview and introduction
├── USAGE.md              # Detailed usage instructions
├── PROJECT_SUMMARY.md    # This file
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variable template
├── .gitignore           # Git ignore rules
├── quickstart.sh        # Setup wizard script
│
├── parser.py            # WhatsApp chat parser
├── analyzer.py          # Personality analyzer
├── chatbot.py           # AI chatbot engine
├── train.py             # Training script
├── chat.py              # Terminal interface
├── app.py               # Web server
│
├── templates/
│   └── chat.html        # Web UI
│
└── example_chat.txt     # Sample chat for testing
```

## 🔧 Technical Details

### Architecture

```
WhatsApp Export (.txt)
        ↓
    [Parser] → Structured messages
        ↓
    [Analyzer] → Personality profile + System prompt
        ↓
    [Chatbot Engine] → AI with personality
        ↓
    [Interface] → User interaction
```

### Data Flow

1. **Input**: WhatsApp chat export (text file)
2. **Parsing**: Extract messages, timestamps, senders
3. **Analysis**: 
   - Calculate statistics
   - Identify patterns
   - Extract vocabulary
   - Detect style
4. **Profile Generation**: Create system prompt encoding personality
5. **Runtime**: AI uses prompt to generate personality-matched responses

### AI Integration

The system uses **prompt engineering** rather than fine-tuning by default:

- **System Prompt**: Detailed instructions describing their texting style
- **Context**: Maintains conversation history
- **Temperature**: Controlled randomness for natural variation

**Optional Fine-tuning**: Export conversation pairs in OpenAI format for more accurate results.

## 📊 What Gets Analyzed

### Message Statistics
- Total message count
- Average message length
- Words per message
- Message distribution (short vs. long)

### Vocabulary Analysis
- Unique words
- Most common words
- Signature phrases
- Characteristic expressions

### Emoji Patterns
- Emoji frequency
- Favorite emojis (top 15)
- Emoji placement patterns

### Punctuation Style
- Exclamation mark usage (enthusiasm)
- Question mark frequency
- Ellipsis usage
- ALL CAPS patterns

### Conversation Patterns
- Single word vs. multi-message responses
- Question asking frequency
- Greeting/sign-off habits
- Laugh patterns (haha, lol, etc.)

### Texting Style
- Concise vs. verbose
- Expressive vs. reserved
- Casual vs. formal
- Use of abbreviations

## 🚀 How to Use

### Quick Start

```bash
# 1. Clone/download the project
cd /tmp/momoGPT

# 2. Run setup wizard
./quickstart.sh

# 3. Follow prompts to:
#    - Install dependencies
#    - Configure API key
#    - Import WhatsApp chat
#    - Train momoGPT

# 4. Start chatting!
python3 app.py  # Web interface
# or
python3 chat.py  # Terminal interface
```

### Manual Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure API key
echo "OPENAI_API_KEY=sk-your-key" > .env

# Train on chat export
python3 train.py --chat-file "chat.txt" --her-name "Momo"

# Start chatting
python3 app.py
```

## 🔒 Privacy & Security

- **All processing is local**: Chat analysis happens on your machine
- **No data storage**: Conversations aren't saved externally
- **API only for responses**: Only chatbot responses use external APIs
- **Secure keys**: API keys stored in `.env` (git-ignored)
- **No telemetry**: Zero data collection or tracking

## 💡 Use Cases

1. **Missing your partner**: Chat when you can't talk
2. **Practice conversations**: Prepare for discussions
3. **Understand communication**: Learn her texting patterns
4. **Fun project**: Build something personal and meaningful
5. **AI learning**: Hands-on experience with personality modeling

## 📈 Scalability

- Handles chats of any size (tested with 10,000+ messages)
- Efficient parsing (regex-based)
- Streaming responses (real-time in web UI)
- Low memory footprint
- Works on any platform (Windows, Mac, Linux)

## 🛠 Technologies Used

- **Python 3.8+**: Core language
- **Flask**: Web framework
- **OpenAI API**: GPT models
- **Anthropic API**: Claude models
- **Regex**: Pattern matching
- **JSON**: Data storage
- **HTML/CSS/JS**: Web interface

## 🎨 Design Philosophy

1. **Privacy First**: Your data stays yours
2. **Easy to Use**: Simple setup, clear instructions
3. **Flexible**: Works with multiple AI providers
4. **Extensible**: Easy to modify and enhance
5. **Beautiful**: Modern, clean UI design
6. **Accurate**: Deep personality analysis

## 🔮 Future Enhancements (Ideas)

- [ ] Voice chat integration
- [ ] Multi-language support
- [ ] Image/video memory (remember shared media)
- [ ] Mood detection and adaptation
- [ ] Time-of-day personality variations
- [ ] Integration with other messaging platforms
- [ ] Local LLM support (offline mode)
- [ ] Mobile app version
- [ ] Personality evolution over time
- [ ] Multiple personality profiles

## 📝 Example Output

**Training Output:**
```
🔄 Parsing WhatsApp chat from: chat_with_momo.txt

📊 Chat Statistics:
   Total messages: 3,542
   Participants: You, Momo
   Date range: 2024-01-15 to 2024-10-25

📱 Analyzing 1,823 messages from Momo...
✓ Saved personality profile to: personality.json
✓ Saved system prompt to: system_prompt.txt

✨ Personality Analysis Summary:
   - Average message length: 45.2 characters
   - Favorite emojis: 💕 😊 🥺 😂 ✨
   - Enthusiasm level: High
   - Style: Concise and expressive

✅ Training complete! momoGPT is ready.
```

**Generated System Prompt Example:**
```
You are Momo, texting your boyfriend. Reply exactly as Momo would - 
match her personality, style, and way of texting.

**Texting Style:**
- Keep messages SHORT and concise (usually 1-2 sentences)
- Use emojis frequently, especially: 💕 😊 🥺 ✨ 😂
- Very enthusiastic - use exclamation marks often!
- Laugh often in texts (haha, lol)
- Favorite words: yeah, omg, love, like, super

**Personality Traits:**
- Expressive and emotionally open
- Direct and to-the-point
- Curious, asks questions

**Important Rules:**
- Reply naturally as if you're in a real conversation
- Match the energy and tone of the messages you receive
- Don't be overly formal or robotic
- You're his girlfriend - be warm, genuine, and authentic
```

## 🤝 Contributing

This is a personal project, but ideas for improvement are welcome!

Areas for contribution:
- Additional chat format parsers
- More sophisticated personality analysis
- UI enhancements
- Performance optimizations
- Bug fixes

## ⚠️ Ethical Considerations

This tool is designed for **personal use** in relationships where both parties are aware and comfortable with it. Consider:

1. **Transparency**: Let your partner know if you're building this
2. **Consent**: Ensure she's okay with her messages being analyzed
3. **Purpose**: Use it responsibly (not for deception)
4. **Privacy**: Keep the data secure and don't share it
5. **Limitations**: Remember it's AI, not her actual thoughts/feelings

## 📄 License

This is an educational project. Use responsibly and ethically.

## 🙏 Acknowledgments

Built with love for memorable conversations. Inspired by the desire to stay connected even when apart.

---

**Remember**: This is a fun technical project, but nothing replaces real human connection. Use it to complement your relationship, not replace actual communication! 💕

