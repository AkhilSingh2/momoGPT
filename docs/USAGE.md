# momoGPT Usage Guide

## Step-by-Step Setup

### 1. Export Your WhatsApp Chat

On your phone:

**iPhone:**
1. Open WhatsApp conversation with the person you want to model
2. Tap her name at the top
3. Scroll down and tap "Export Chat"
4. Select "Without Media"
5. Save or email the `.txt` file to yourself

**Android:**
1. Open WhatsApp conversation
2. Tap the three dots (⋮) in the top right
3. Tap "More" → "Export chat"
4. Choose "Without media"
5. Save or share the `.txt` file

The file will look something like:
```
12/25/2024, 10:30 AM - You: hey babe
12/25/2024, 10:31 AM - Momo: hiii!! how are you? 💕
12/25/2024, 10:32 AM - You: good! miss you
12/25/2024, 10:33 AM - Momo: aww miss you too 🥺
```

### 2. Install Dependencies

```bash
cd /tmp/momoGPT
pip install -r requirements.txt
```

### 3. Set Up API Key

**Option A: OpenAI (GPT-4 / GPT-3.5)**
1. Get API key from: https://platform.openai.com/api-keys
2. Create `.env` file:
```
OPENAI_API_KEY=sk-your-key-here
```

**Option B: Anthropic (Claude)**
1. Get API key from: https://console.anthropic.com/
2. Create `.env` file:
```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

You only need ONE of these.

### 4. Train momoGPT

```bash
python train.py --chat-file "WhatsApp Chat with Momo.txt" --her-name "Momo"
```

**Important:** 
- Replace `"Momo"` with her name EXACTLY as it appears in the chat
- If the parser can't find her name, it will show you available names

This will:
- Parse all messages
- Analyze their texting style
- Generate `personality.json` (her patterns)
- Create `system_prompt.txt` (instructions for the AI)

### 5. Chat with momoGPT

**Terminal Chat:**
```bash
python chat.py
```

**Web Interface (Recommended):**
```bash
python app.py
```
Then open: http://localhost:5000

## Advanced Features

### Export Fine-Tuning Data

For even more accurate responses, you can fine-tune a model:

```bash
python train.py \
  --chat-file "WhatsApp Chat.txt" \
  --her-name "Momo" \
  --your-name "John" \
  --export-finetuning
```

This creates `finetuning_data.jsonl` - upload it to OpenAI's fine-tuning dashboard:
https://platform.openai.com/finetune

### Customize the Personality

After running `train.py`, you can edit `system_prompt.txt` to:
- Add specific phrases she uses
- Emphasize certain personality traits
- Include inside jokes or references

### Test the Parser

```bash
python parser.py "WhatsApp Chat.txt"
```

### Test the Analyzer

```bash
python analyzer.py "WhatsApp Chat.txt" "Momo"
```

## Troubleshooting

### "Her name not found in participants"
- Check the exact spelling in the chat export
- Names are case-sensitive
- Run `python parser.py "your_chat.txt"` to see all participant names

### "No API key found"
- Make sure `.env` file exists in the project directory
- Check that your API key is valid
- Verify no extra spaces in the `.env` file

### Parser can't read messages
- The parser supports multiple WhatsApp export formats
- If it fails, check the date/time format in your export
- You may need to adjust the patterns in `parser.py`

### Responses don't sound like her
- Make sure you have enough chat history (at least 100+ messages)
- Edit `system_prompt.txt` to be more specific
- Consider fine-tuning for better accuracy

### Import errors
- Run: `pip install -r requirements.txt`
- Make sure you're using Python 3.8+

## Tips for Best Results

1. **More data = better results**
   - Use several months of chat history if possible
   - Include various conversation types (casual, deep, playful)

2. **Review the analysis**
   - Check `personality.json` after training
   - Adjust `system_prompt.txt` if needed

3. **Context matters**
   - The bot learns from conversation flow
   - Longer conversations work better than single messages

4. **Privacy**
   - All processing happens locally
   - Only the AI API calls go online
   - Your chat data never leaves your machine
   - Delete the chat export after training if desired

## Examples

### Quick Start Example
```bash
# 1. Get your chat export (example: "chat_with_momo.txt")

# 2. Install
pip install -r requirements.txt

# 3. Setup API key
echo "OPENAI_API_KEY=sk-..." > .env

# 4. Train
python train.py --chat-file "chat_with_momo.txt" --her-name "Momo"

# 5. Chat
python app.py
```

### What You'll See

**Terminal output:**
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

   Message Style:
   - Average message length: 45.2 characters
   - Average words per message: 8.3
   - Favorite emojis: 💕 😊 🥺 😂 ✨
   - Enthusiasm level: High

   Texting Habits:
   - Style: Concise and brief
   - Very expressive with emojis and punctuation

✅ Training complete! momoGPT is ready.
```

## Cost Estimates

**OpenAI (GPT-3.5-turbo):** ~$0.002 per conversation turn
**OpenAI (GPT-4):** ~$0.03 per conversation turn  
**Anthropic (Claude):** ~$0.015 per conversation turn

A typical chat session with 20 messages costs:
- GPT-3.5: $0.04
- GPT-4: $0.60
- Claude: $0.30

Training (analysis) is FREE - all local processing.

---

Enjoy chatting with momoGPT! 💬✨

