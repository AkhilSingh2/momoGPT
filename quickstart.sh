#!/bin/bash

# momoGPT Quick Start Script

echo "🚀 momoGPT Setup"
echo "=================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✓ Dependencies installed"

# Check for .env file
echo ""
if [ ! -f .env ]; then
    echo "⚠️  No .env file found"
    echo ""
    echo "Please create a .env file with your API key:"
    echo ""
    echo "For OpenAI (GPT-3.5/GPT-4):"
    echo "  OPENAI_API_KEY=sk-your-key-here"
    echo ""
    echo "OR for Anthropic (Claude):"
    echo "  ANTHROPIC_API_KEY=sk-ant-your-key-here"
    echo ""
    read -p "Do you want to create .env now? (y/n): " create_env
    
    if [ "$create_env" = "y" ] || [ "$create_env" = "Y" ]; then
        echo ""
        read -p "Enter your API key: " api_key
        
        if [[ $api_key == sk-ant-* ]]; then
            echo "ANTHROPIC_API_KEY=$api_key" > .env
        else
            echo "OPENAI_API_KEY=$api_key" > .env
        fi
        
        echo "✓ .env file created"
    else
        echo ""
        echo "Please create .env manually and run this script again"
        exit 1
    fi
else
    echo "✓ .env file found"
fi

# Ask about chat file
echo ""
echo "📱 WhatsApp Chat Export"
echo ""
read -p "Enter path to your WhatsApp chat export file: " chat_file

if [ ! -f "$chat_file" ]; then
    echo "❌ File not found: $chat_file"
    echo ""
    echo "To export your WhatsApp chat:"
    echo "1. Open WhatsApp conversation"
    echo "2. Tap contact name → Export Chat → Without Media"
    exit 1
fi

echo "✓ Chat file found"

# Parse participants
echo ""
echo "🔍 Detecting participants..."
participants=$(python3 parser.py "$chat_file" 2>/dev/null | grep "Participants:" | cut -d':' -f2)

if [ -z "$participants" ]; then
    echo "❌ Could not parse chat file"
    exit 1
fi

echo "   Found:$participants"
echo ""
read -p "Enter her name exactly as shown above: " her_name

# Train momoGPT
echo ""
echo "🧠 Training momoGPT..."
python3 train.py --chat-file "$chat_file" --her-name "$her_name"

if [ $? -ne 0 ]; then
    echo "❌ Training failed"
    exit 1
fi

# Success!
echo ""
echo "✅ momoGPT is ready!"
echo ""
echo "To start chatting:"
echo "  Terminal: python3 chat.py"
echo "  Web:      python3 app.py"
echo ""
read -p "Start web interface now? (y/n): " start_web

if [ "$start_web" = "y" ] || [ "$start_web" = "Y" ]; then
    python3 app.py
fi

