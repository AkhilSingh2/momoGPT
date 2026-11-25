#!/bin/bash

# Quick start script for FREE momoGPT

echo "============================================================"
echo "🚀 momoGPT - FREE AI Quick Start"
echo "============================================================"
echo ""
echo "Choose your FREE AI option:"
echo ""
echo "  1) Ollama (100% free, private, runs locally)"
echo "     - Best for privacy and unlimited usage"
echo "     - Requires: 8GB RAM, one-time 4GB download"
echo ""
echo "  2) Groq (free cloud API, super fast)"
echo "     - Best for quick setup"
echo "     - Requires: Free API key from console.groq.com"
echo ""
echo "  3) Skip setup, just run (if already configured)"
echo ""
read -p "Enter your choice (1, 2, or 3): " choice

if [ "$choice" = "1" ]; then
    echo ""
    echo "Setting up Ollama..."
    echo ""
    
    # Check if Ollama is installed
    if ! command -v ollama &> /dev/null; then
        echo "Ollama not found. Installing..."
        echo ""
        echo "Please visit: https://ollama.ai"
        echo "Download and install Ollama, then run this script again."
        echo ""
        echo "Or on macOS, run: brew install ollama"
        exit 1
    fi
    
    echo "✓ Ollama is installed"
    echo ""
    
    # Check if Ollama is running
    if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "Starting Ollama service..."
        ollama serve > /dev/null 2>&1 &
        sleep 2
    fi
    
    echo "✓ Ollama service is running"
    echo ""
    
    # Check if model is downloaded
    echo "Checking for llama3.2 model..."
    if ! ollama list | grep -q "llama3.2"; then
        echo "Downloading llama3.2 model (this may take 5-10 minutes)..."
        ollama pull llama3.2
    fi
    
    echo "✓ Model ready!"
    echo ""
    echo "Starting momoGPT..."
    python3 chat_free.py
    
elif [ "$choice" = "2" ]; then
    echo ""
    echo "Setting up Groq..."
    echo ""
    
    # Check if groq is installed
    if ! python3 -c "import groq" 2>/dev/null; then
        echo "Installing Groq package..."
        python3 -m pip install --user groq
    fi
    
    echo "✓ Groq package installed"
    echo ""
    
    # Check for API key
    if [ ! -f .env ] || ! grep -q "GROQ_API_KEY" .env; then
        echo "Get your FREE Groq API key from: https://console.groq.com"
        echo ""
        read -p "Enter your Groq API key: " api_key
        
        if [ ! -z "$api_key" ]; then
            echo "GROQ_API_KEY=$api_key" >> .env
            echo "✓ API key saved!"
        else
            echo "❌ No API key provided"
            exit 1
        fi
    else
        echo "✓ API key found in .env"
    fi
    
    echo ""
    echo "Starting momoGPT..."
    python3 chat_free.py
    
elif [ "$choice" = "3" ]; then
    echo ""
    echo "Starting momoGPT..."
    python3 chat_free.py
    
else
    echo "Invalid choice"
    exit 1
fi



