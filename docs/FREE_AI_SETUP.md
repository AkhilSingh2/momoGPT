# 🆓 momoGPT - 100% FREE AI Setup Guide

Your momoGPT is already trained! Now let's set it up with **completely FREE AI** options.

## 🎯 Best Free Options (Choose One)

### ⭐ Option 1: Ollama (RECOMMENDED - 100% Free, Private, No API Key)

**Best for**: Complete privacy, unlimited usage, no API keys

**Setup:**

1. **Install Ollama** (one-time setup):
   ```bash
   # Download and install from: https://ollama.ai
   # Or on macOS:
   brew install ollama
   ```

2. **Start Ollama**:
   ```bash
   ollama serve
   ```
   (Leave this running in a terminal)

3. **Download a model** (one-time, ~4-5GB):
   ```bash
   ollama pull llama3.2
   ```

4. **Run momoGPT**:
   ```bash
   python3 chat_free.py
   # or for web interface:
   python3 app_free.py
   ```

**Pros:**
- ✅ 100% FREE forever
- ✅ No API keys needed
- ✅ Runs on your computer (private)
- ✅ Unlimited conversations
- ✅ Works offline
- ✅ No rate limits

**Cons:**
- ⚠️ Requires 8GB+ RAM
- ⚠️ Initial model download (~4-5GB)
- ⚠️ Slightly slower than cloud APIs

---

### 🚀 Option 2: Groq (FREE Cloud API - Very Fast)

**Best for**: Fast responses, no local installation

**Setup:**

1. **Get FREE API key**:
   - Go to: https://console.groq.com
   - Sign up (free)
   - Copy your API key

2. **Add to .env file**:
   ```bash
   echo "GROQ_API_KEY=your_key_here" > .env
   ```

3. **Install Groq package**:
   ```bash
   pip install groq
   ```

4. **Run momoGPT**:
   ```bash
   python3 chat_free.py
   ```

**Pros:**
- ✅ Completely FREE
- ✅ Super FAST responses
- ✅ No local installation
- ✅ Works on any device

**Cons:**
- ⚠️ Requires internet
- ⚠️ Rate limits (generous but exist)
- ⚠️ Data sent to cloud

---

### 💡 Option 3: OpenRouter (FREE Models Available)

**Best for**: Access to many different models

**Setup:**

1. **Get FREE API key**:
   - Go to: https://openrouter.ai
   - Sign up (free tier available)
   - Get API key

2. **Add to .env file**:
   ```bash
   echo "OPENROUTER_API_KEY=your_key_here" > .env
   ```

3. **Run momoGPT**:
   ```bash
   python3 chat_free.py
   ```

**Pros:**
- ✅ Many FREE models to choose from
- ✅ Good quality
- ✅ Easy to switch models

**Cons:**
- ⚠️ Some models are paid (but many are free)
- ⚠️ Requires internet

---

## 🎮 Quick Start Commands

### For Terminal Chat:
```bash
cd momoGPT
python3 chat_free.py
```

### For Web Interface:
```bash
cd momoGPT
python3 app_free.py
# Then open: http://localhost:5000
```

---

## 📊 Comparison Table

| Feature | Ollama | Groq | OpenRouter |
|---------|--------|------|------------|
| **Cost** | 100% Free | 100% Free | Free tier |
| **Speed** | Medium | Very Fast | Fast |
| **Privacy** | 🔒 100% Private | Cloud | Cloud |
| **Setup Time** | 10 min | 2 min | 2 min |
| **Offline** | ✅ Yes | ❌ No | ❌ No |
| **Rate Limits** | None | Generous | Varies |
| **Recommended?** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |

---

## 🔧 Detailed Ollama Setup (Recommended)

### Step-by-Step for macOS:

1. **Download Ollama**:
   ```bash
   # Visit https://ollama.ai and download for macOS
   # Or use Homebrew:
   brew install ollama
   ```

2. **Start Ollama service**:
   ```bash
   # In one terminal, run:
   ollama serve
   ```

3. **Open a NEW terminal and pull the model**:
   ```bash
   ollama pull llama3.2
   # This downloads ~4.7GB, takes 5-10 minutes depending on internet
   ```

4. **Verify it's working**:
   ```bash
   ollama list
   # Should show llama3.2 in the list
   ```

5. **Run momoGPT**:
   ```bash
   cd momoGPT
   python3 chat_free.py
   ```

### Alternative Models (Optional):

```bash
# Faster but less capable:
ollama pull llama3.2:1b

# More capable but slower:
ollama pull mistral

# Excellent quality:
ollama pull llama3.1
```

---

## 🆘 Troubleshooting

### "Connection refused" with Ollama:
```bash
# Make sure Ollama is running:
ollama serve
# In another terminal, try again
```

### "Model not found" with Ollama:
```bash
# Pull the model:
ollama pull llama3.2
```

### Ollama is slow:
```bash
# Use a smaller model:
ollama pull llama3.2:1b
# Then restart chat_free.py
```

### Groq rate limit reached:
- Wait a few minutes, or
- Switch to Ollama for unlimited usage

---

## 🎉 Ready to Chat!

Choose your preferred option above, follow the setup steps, and you'll be chatting with momoGPT in minutes!

**My Recommendation**: Start with **Ollama** for best privacy and unlimited usage. If you want faster responses and don't mind cloud APIs, try **Groq**.

---

## 💬 Example Usage

```bash
$ python3 chat_free.py

============================================================
💬 MomoGPT - FREE AI Chat Interface
============================================================
Using: 100% FREE Local/Cloud AI
Type 'quit' or 'exit' to end the conversation
Type 'reset' to start a new conversation
============================================================

You: hey, how's your day going?

Momo: Pretty good. Just been busy with work. You?

You: same here, thinking about dinner plans

Momo: What you thinking?

You: maybe that pizza place?

Momo: Yeah okay sounds good
```

---

**Questions?** Check the main README.md or open an issue!



