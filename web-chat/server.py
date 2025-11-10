#!/usr/bin/env python3
"""
Flask API server for AI Agent Chat
"""

import os
import asyncio
from flask import Flask, request, jsonify
from flask_cors import CORS
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search

# Set up API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyBR3sPTYuwKGkBBkAKvV13vBrqxBAfWL6Q"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Create the AI agent
root_agent = Agent(
    name="helpful_assistant",
    model="gemini-2.5-flash-lite",
    description="A helpful AI assistant that can answer questions and search the web.",
    instruction="""You are a helpful and friendly AI assistant.
    Use Google Search for current information, news, weather, or any time-sensitive queries.
    Provide clear, concise, and accurate responses.
    Be conversational and engaging.""",
    tools=[google_search],
)

# Create the runner
runner = InMemoryRunner(agent=root_agent)

print("=" * 80)
print("🚀 AI Agent Chat Server Starting...")
print("=" * 80)
print("✅ Agent initialized with Google Search tool")
print("✅ Model: gemini-2.5-flash-lite")
print("=" * 80)


@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests from the frontend"""
    try:
        data = request.get_json()

        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400

        user_message = data['message']

        if not user_message.strip():
            return jsonify({'error': 'Message cannot be empty'}), 400

        print(f"\n📨 Received: {user_message}")

        # Run the agent query
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(runner.run_debug(user_message))
        loop.close()

        # Extract the text response
        if response and len(response) > 0:
            response_text = response[0].content.parts[0].text
            print(f"💬 Response: {response_text[:100]}...")

            return jsonify({
                'response': response_text,
                'success': True
            })
        else:
            return jsonify({'error': 'No response from agent'}), 500

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'agent': 'ready',
        'model': 'gemini-2.5-flash-lite'
    })


@app.route('/')
def index():
    """Serve the HTML page"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Agent Chat - Server Running</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }
            .container {
                background: white;
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                text-align: center;
            }
            h1 { color: #667eea; margin-bottom: 20px; }
            p { color: #666; line-height: 1.6; }
            .status {
                display: inline-block;
                background: #10b981;
                color: white;
                padding: 8px 16px;
                border-radius: 20px;
                font-weight: 600;
                margin: 20px 0;
            }
            code {
                background: #f1f1f1;
                padding: 2px 8px;
                border-radius: 4px;
                font-family: monospace;
            }
            a {
                color: #667eea;
                text-decoration: none;
                font-weight: 600;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 AI Agent Chat Server</h1>
            <div class="status">✅ Server Running</div>
            <p>The API server is running successfully!</p>
            <p style="margin-top: 20px;">
                Open <code>index.html</code> in your browser to access the chat interface.
            </p>
            <p style="margin-top: 10px; font-size: 14px; color: #999;">
                API endpoint: <code>POST /api/chat</code>
            </p>
        </div>
    </body>
    </html>
    """


if __name__ == '__main__':
    print("\n🌐 Starting Flask server on http://localhost:8080")
    print("📱 Open index.html in your browser to use the chat interface")
    print("\nPress CTRL+C to stop the server\n")
    app.run(debug=True, host='0.0.0.0', port=8080)
