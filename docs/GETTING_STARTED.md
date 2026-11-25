# Getting Started with momoGPT

Welcome! This guide will help you set up and start using momoGPT in just a few minutes.

## 🎯 What You'll Need

- [ ] Python 3.8 or higher
- [ ] WhatsApp chat export with the person you want to model
- [ ] API key (OpenAI or Anthropic)
- [ ] 5-10 minutes for setup

## 📱 Step 1: Export WhatsApp Chat

### On iPhone:
1. Open WhatsApp
2. Open the conversation with the person you want to model
3. Tap her name at the top
4. Scroll down and tap **"Export Chat"**
5. Select **"Without Media"** (important!)
6. Save or email the `.txt` file to your computer

### On Android:
1. Open WhatsApp
2. Open the conversation
3. Tap the three dots (⋮) menu
4. Select **More** → **Export chat**
5. Choose **"Without media"**
6. Save the `.txt` file

### What the file looks like:
```
12/25/2024, 10:30 AM - You: hey babe
12/25/2024, 10:31 AM - Momo: hiii!! 💕
```

**Tips:**
- Export the entire conversation (more data = better results)
- At least 100+ messages recommended
- Include variety: casual chats, deep talks, playful banter

## 🔑 Step 2: Get an API Key

You need an API key from either OpenAI or Anthropic:

### Option A: OpenAI (GPT)
1. Go to: https://platform.openai.com/signup
2. Create an account
3. Go to: https://platform.openai.com/api-keys
4. Click **"Create new secret key"**
5. Copy the key (starts with `sk-`)
6. Add billing: https://platform.openai.com/account/billing

**Pricing:** GPT-3.5 is very cheap (~$0.002/message), GPT-4 is more expensive (~$0.03/message)

### Option B: Anthropic (Claude)
1. Go to: https://console.anthropic.com/
2. Create an account
3. Navigate to API Keys
4. Create a new key
5. Copy the key (starts with `sk-ant-`)

**Pricing:** Claude is mid-range (~$0.015/message)

## 🚀 Step 3: Quick Setup

### Automatic (Easiest):
```bash
cd /tmp/momoGPT
./quickstart.sh
```

The wizard will:
- Install dependencies automatically
- Guide you through API key setup
- Help you import your chat
- Train momoGPT
- Launch the chat interface

### Manual Setup:

#### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 2. Create `.env` file
Create a file named `.env` in the project folder:

For OpenAI:
```
OPENAI_API_KEY=sk-your-openai-key-here
```

For Anthropic:
```
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
```

#### 3. Train momoGPT
Replace the names with your actual chat file and her name:
```bash
python train.py --chat-file "WhatsApp Chat with Momo.txt" --her-name "Momo"
```

**Important:** Her name must match EXACTLY as it appears in the chat export!

#### 4. Launch Chat Interface

Web interface (recommended):
```bash
python app.py
```
Then open: http://localhost:5000

Terminal interface:
```bash
python chat.py
```

## ✅ Verification

After training, you should see:
- ✓ `personality.json` - Her personality profile
- ✓ `system_prompt.txt` - AI instructions

Check the system prompt:
```bash
cat system_prompt.txt
```

You should see details about their texting style, emoji usage, and personality!

## 💬 First Conversation

### Web Interface:
1. Open http://localhost:5000
2. You'll see momoGPT's greeting
3. Type a message like "hey babe, how's your day?"
4. Press Send or hit Enter
5. Watch the AI respond in her style!

### Terminal Interface:
```bash
$ python chat.py
💬 Chat with momoGPT
Type 'quit' to exit, 'reset' to start over

You: hey babe
Momo: hiii!! what's up? 💕

You: miss you
Momo: aww miss you too!! 🥺
```

## 🎨 What to Expect

The AI will try to match:
- **Her message length** (short and sweet vs. long paragraphs)
- **Her emoji style** (which emojis, how often)
- **Her punctuation** (lots of !!! or more reserved)
- **Her vocabulary** (words she uses often)
- **Her personality** (playful, serious, affectionate)
- **Her response patterns** (single messages vs. multiple)

## 🔧 Troubleshooting

### "Name not found in participants"
Run this to see all names in your chat:
```bash
python parser.py "your_chat_file.txt"
```
Copy the exact spelling (case-sensitive!).

### "No module named 'openai'"
Install dependencies:
```bash
pip install -r requirements.txt
```

### "Invalid API key"
- Check for typos in `.env`
- Make sure no extra spaces
- Verify key is active at provider's website
- For OpenAI, ensure billing is set up

### Parser can't read messages
The parser supports most WhatsApp formats. If it fails:
1. Check the first few lines of your export match this format:
   ```
   MM/DD/YYYY, HH:MM AM/PM - Name: Message
   ```
2. Open an issue or check `parser.py` to add your format

### Responses don't sound like her
- Need more training data (100+ messages minimum)
- Edit `system_prompt.txt` to add specific details
- Try different AI models (GPT-4 is more accurate than GPT-3.5)
- Consider fine-tuning (advanced)

### Web interface won't start
- Check port 5000 isn't in use
- Try: `python app.py` again
- Check error messages

## 💡 Pro Tips

### 1. Improve Accuracy
```bash
# Export more conversation history
# Aim for 500-1000+ messages for best results
```

### 2. Customize Personality
Edit `system_prompt.txt` after training:
```bash
nano system_prompt.txt
```
Add specific phrases, inside jokes, or personality traits.

### 3. Test Different Models
In `chatbot.py`, you can specify:
- `gpt-3.5-turbo` (fast, cheap)
- `gpt-4` (smarter, more expensive)
- `claude` (good balance)

### 4. Export for Fine-Tuning
For even better accuracy:
```bash
python train.py \
  --chat-file "chat.txt" \
  --her-name "Momo" \
  --your-name "Your Name" \
  --export-finetuning
```
Upload `finetuning_data.jsonl` to OpenAI for fine-tuning.

### 5. Privacy
After training, you can delete the chat export:
```bash
rm "WhatsApp Chat.txt"
```
The personality profile is saved, so you don't need the original anymore.

## 📊 Example Session

```bash
$ ./quickstart.sh

🚀 momoGPT Setup
==================
✓ Python found: Python 3.11.5
📦 Installing dependencies...
✓ Dependencies installed
✓ .env file found

📱 WhatsApp Chat Export
Enter path to your WhatsApp chat export file: chat.txt
✓ Chat file found

🔍 Detecting participants...
   Found: You, Momo
Enter her name exactly as shown above: Momo

🧠 Training momoGPT...
📊 Chat Statistics:
   Total messages: 1,234
   Participants: You, Momo
   Date range: 2024-01-15 to 2024-10-25

📱 Analyzing 627 messages from Momo...
✓ Saved personality profile to: personality.json
✓ Saved system prompt to: system_prompt.txt

✨ Personality Analysis Summary:
   - Average message length: 38.5 characters
   - Favorite emojis: 💕 😊 🥺 ✨ 😂
   - Enthusiasm level: High
   - Style: Concise and expressive

✅ momoGPT is ready!

Start web interface now? (y/n): y

🚀 momoGPT Web Interface
📱 Open in browser: http://localhost:5000
```

## 🎉 You're Ready!

Congratulations! You now have a personalized chatbot that texts like the person you modelled.

### Next Steps:
1. **Chat**: Try different conversation topics
2. **Refine**: Edit the system prompt if needed
3. **Share**: Show her the fun project (with permission!)
4. **Enjoy**: Use it when you miss her

### Remember:
- This is a fun AI project, not a replacement for real communication
- Always prioritize actual conversations with your partner
- Use it ethically and with her knowledge
- Have fun exploring AI personality modeling!

## 📚 More Resources

- **Detailed Guide**: See `USAGE.md`
- **Technical Details**: See `PROJECT_SUMMARY.md`
- **README**: See `README.md`

## 💬 Questions?

Common questions:

**Q: Is this creepy?**  
A: It's a fun technical project! Use it openly and ethically. Many couples think it's cute.

**Q: Will she find out?**  
A: Better to tell her! It's actually a sweet gesture showing you care about understanding her communication style.

**Q: How accurate is it?**  
A: With 500+ messages, it can capture their texting style remarkably well. With fine-tuning, even better.

**Q: Can I use it for other people?**  
A: Yes! Works with any WhatsApp chat. Try it with friends, family (with permission).

**Q: Does it learn over time?**  
A: Not automatically. Re-run training with updated chat exports to refresh.

**Q: Is my data safe?**  
A: Yes! Everything processes locally. Only chat responses use APIs (not the training data).

---

**Happy chatting with momoGPT!** 💕🤖

If you get stuck, check the troubleshooting section or review the example files included.

