#!/bin/bash

# Setup script for momoGPT environment

echo "============================================================"
echo "🚀 momoGPT Environment Setup"
echo "============================================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cat > .env << 'EOF'
# Add your API key here
# You can use either OpenAI or Anthropic

# For OpenAI (GPT-4, GPT-3.5-turbo)
OPENAI_API_KEY=your_openai_api_key_here

# OR for Anthropic (Claude)
# ANTHROPIC_API_KEY=your_anthropic_api_key_here
EOF
    echo "✓ Created .env file"
fi

echo ""
echo "Please choose your AI provider:"
echo "  1) OpenAI (GPT-4 / GPT-3.5)"
echo "  2) Anthropic (Claude)"
echo ""
read -p "Enter your choice (1 or 2): " choice

if [ "$choice" = "1" ]; then
    echo ""
    echo "Get your OpenAI API key from: https://platform.openai.com/api-keys"
    read -p "Enter your OpenAI API key: " api_key
    
    if [ ! -z "$api_key" ]; then
        # Update .env file
        if grep -q "OPENAI_API_KEY=" .env; then
            sed -i.bak "s|OPENAI_API_KEY=.*|OPENAI_API_KEY=$api_key|" .env
            rm -f .env.bak
        else
            echo "OPENAI_API_KEY=$api_key" >> .env
        fi
        echo "✓ OpenAI API key saved to .env"
    fi
    
elif [ "$choice" = "2" ]; then
    echo ""
    echo "Get your Anthropic API key from: https://console.anthropic.com/"
    read -p "Enter your Anthropic API key: " api_key
    
    if [ ! -z "$api_key" ]; then
        # Update .env file
        if grep -q "ANTHROPIC_API_KEY=" .env; then
            sed -i.bak "s|ANTHROPIC_API_KEY=.*|ANTHROPIC_API_KEY=$api_key|" .env
            rm -f .env.bak
        else
            echo "ANTHROPIC_API_KEY=$api_key" >> .env
        fi
        echo "✓ Anthropic API key saved to .env"
    fi
else
    echo "Invalid choice. Please manually edit the .env file."
    exit 1
fi

echo ""
echo "============================================================"
echo "✅ Setup Complete!"
echo "============================================================"
echo ""
echo "You can now run momoGPT:"
echo "  Terminal chat: python3 chat.py"
echo "  Web interface: python3 app.py"
echo ""


