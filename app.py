"""
Web Interface for momoGPT
Flask-based chat interface
"""

import os
import sys
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from chatbot import MomoGPT

load_dotenv()

app = Flask(__name__)

# Global bot instance
bot = None
bot_name = "Momo"


def initialize_bot():
    """Initialize the chatbot"""
    global bot, bot_name
    
    if not os.path.exists('system_prompt.txt'):
        raise FileNotFoundError("system_prompt.txt not found. Run train.py first!")
    
    with open('system_prompt.txt', 'r', encoding='utf-8') as f:
        system_prompt = f.read()
    
    # Extract name from system prompt if possible
    if "You are " in system_prompt:
        try:
            bot_name = system_prompt.split("You are ")[1].split(",")[0].strip()
        except:
            pass
    
    bot = MomoGPT(system_prompt)
    print(f"✅ {bot_name}GPT initialized!")


@app.route('/')
def index():
    """Render chat interface"""
    return render_template('chat.html', bot_name=bot_name)


@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        # Get bot response
        response = bot.chat(user_message)
        
        return jsonify({
            'response': response,
            'success': True
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500


@app.route('/reset', methods=['POST'])
def reset():
    """Reset conversation"""
    try:
        bot.reset_conversation()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/history', methods=['GET'])
def history():
    """Get conversation history"""
    try:
        return jsonify({
            'history': bot.get_history(),
            'success': True
        })
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500


if __name__ == '__main__':
    try:
        initialize_bot()
        print("\n" + "="*50)
        print(f"🚀 {bot_name}GPT Web Interface")
        print("="*50)
        print("📱 Open in browser: http://localhost:5001")
        print("⌨️  Press Ctrl+C to stop")
        print("="*50 + "\n")
        
        app.run(debug=True, host='0.0.0.0', port=5001)
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure you have:")
        print("  1. Run: python train.py --chat-file <file> --her-name <name>")
        print("  2. Created .env with OPENAI_API_KEY or ANTHROPIC_API_KEY")
        print("  3. Installed: pip install -r requirements.txt")
        sys.exit(1)

