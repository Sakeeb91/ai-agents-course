#!/usr/bin/env python3
"""
Gradio Interface for AI Agent Chat
Deployment-ready version for Hugging Face Spaces

To deploy on Hugging Face Spaces:
1. Create a new Space (select Gradio as SDK)
2. Upload app.py and requirements.txt
3. Add GOOGLE_API_KEY as a secret in Space settings
4. Your Space will automatically deploy!
"""

import os
import asyncio
import gradio as gr
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search

# Get API key from environment (required for Hugging Face Spaces)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY environment variable is required.\n"
        "For Hugging Face Spaces: Add it as a secret in Space settings.\n"
        "For local development: Set it with 'export GOOGLE_API_KEY=your-key'"
    )

# Set up environment
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"

# Create the AI agent
root_agent = Agent(
    name="helpful_assistant",
    model="gemini-2.5-flash-lite",
    description="A helpful AI assistant that can answer questions and search the web.",
    instruction="""You are a helpful and friendly AI assistant.
    Use Google Search for current information, news, weather, or any time-sensitive queries.
    Provide clear, concise, and accurate responses.
    Be conversational and engaging.
    Format your responses nicely with markdown when appropriate.""",
    tools=[google_search],
)

# Create the runner
runner = InMemoryRunner(agent=root_agent)

print("=" * 80)
print("🚀 AI Agent Chat - Gradio Interface")
print("=" * 80)
print("✅ Agent initialized with Google Search tool")
print("✅ Model: gemini-2.5-flash-lite")
print("=" * 80)


def chat_with_agent(message, history):
    """
    Process user message and return agent response

    Args:
        message: User's current message
        history: Chat history in Gradio format [[user_msg, bot_msg], ...]

    Returns:
        str: Agent's response
    """
    if not message or not message.strip():
        return ""

    try:
        # Run the agent query
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(runner.run_debug(message))
        loop.close()

        # Extract the text response
        if response and len(response) > 0:
            response_text = response[0].content.parts[0].text
            return response_text
        else:
            return "❌ Sorry, I couldn't generate a response. Please try again."

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return f"❌ Error: {str(e)}"


# Custom CSS for a beautiful interface with orange-mauve gradient
custom_css = """
.gradio-container {
    max-width: 900px !important;
}

#component-0 {
    background: linear-gradient(135deg, #ff6b35 0%, #c44569 50%, #8b5a9e 100%);
    color: white;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    margin-bottom: 20px;
    box-shadow: 0 4px 15px rgba(255, 107, 53, 0.3);
}

/* Orange-mauve gradient for buttons */
.primary-button {
    background: linear-gradient(135deg, #ff6b35 0%, #c44569 100%) !important;
}

/* Accent colors */
button.primary {
    background: linear-gradient(135deg, #ff6b35 0%, #c44569 100%) !important;
    border: none !important;
}

.chatbot .message.bot {
    background: linear-gradient(135deg, rgba(255, 107, 53, 0.1) 0%, rgba(196, 69, 105, 0.1) 100%) !important;
    border-left: 3px solid #ff6b35 !important;
}
"""

# Create Gradio interface with orange-mauve theme
with gr.Blocks(
    theme=gr.themes.Soft(
        primary_hue="orange",
        secondary_hue="pink",
    ),
    css=custom_css,
    title="AI Agent Chat",
) as demo:

    # Header
    gr.Markdown(
        """
        # 🤖 AI Agent Chat
        ### Powered by Google ADK & Gemini

        Ask me anything! I can search the web for current information, answer questions, and help with various tasks.
        """
    )

    # Chat interface
    chatbot = gr.Chatbot(
        height=500,
        show_label=False,
        avatar_images=(
            None,  # User avatar (default)
            "https://em-content.zobj.net/source/apple/391/robot_1f916.png"  # Agent avatar
        ),
        bubble_full_width=False,
    )

    # Input area
    with gr.Row():
        msg = gr.Textbox(
            placeholder="Type your message here...",
            show_label=False,
            scale=9,
            autofocus=True,
        )
        submit = gr.Button("Send 📤", variant="primary", scale=1)

    # Examples
    gr.Examples(
        examples=[
            "What's the weather in Tokyo?",
            "Explain how AI agents work in simple terms",
            "Write a Python function to calculate factorial",
            "What are the latest tech news?",
            "Compare cats vs dogs in a table",
        ],
        inputs=msg,
        label="💡 Try these examples:",
    )

    # Clear button
    clear = gr.Button("🗑️ Clear Chat", variant="secondary")

    # Info section
    with gr.Accordion("ℹ️ About this AI Agent", open=False):
        gr.Markdown(
            """
            ### Features:
            - 🔍 **Google Search**: Can search the web for current information
            - 🧠 **Smart Tool Usage**: Decides when to use search based on your query
            - ⚡ **Fast Responses**: Using Gemini 2.5 Flash Lite
            - 📊 **Rich Formatting**: Supports markdown for beautiful responses

            ### How it works:
            1. You ask a question
            2. The agent analyzes if it needs current information
            3. If needed, it searches Google
            4. It synthesizes the information into a clear answer

            ### Technical Details:
            - **Framework**: Google Agent Development Kit (ADK)
            - **Model**: Gemini 2.5 Flash Lite
            - **Tools**: Google Search
            - **Interface**: Gradio

            ### Source Code:
            Built as part of the Kaggle 5-Day AI Agents Course
            """
        )

    # Event handlers
    def respond(message, chat_history):
        bot_message = chat_with_agent(message, chat_history)
        chat_history.append((message, bot_message))
        return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    submit.click(respond, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)


if __name__ == "__main__":
    print("\n🌐 Starting Gradio interface...")
    print("📱 The interface will open in your browser automatically")
    print("\nPress CTRL+C to stop the server\n")

    # Launch the app
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,  # Set to True to create a public link
        show_error=True,
    )
