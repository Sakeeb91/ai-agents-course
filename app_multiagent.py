#!/usr/bin/env python3
"""
Enhanced Gradio Interface for AI Agent Chat
Includes both simple agent and multi-agent system demos
Deployment-ready version for Hugging Face Spaces

Features:
- Simple chat with single agent (Day 1A)
- Multi-agent demonstrations (Day 1B):
  * Research & Summarization (LLM-based orchestration)
  * Blog Post Pipeline (Sequential agents)
  * Parallel Research (Parallel agents with aggregation)
"""

import os
import asyncio
import gradio as gr
from google.adk.agents import Agent, SequentialAgent, ParallelAgent
from google.adk.runners import InMemoryRunner
from google.adk.tools import AgentTool, google_search

# Get API key from environment (for Hugging Face Spaces) or use default
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyBR3sPTYuwKGkBBkAKvV13vBrqxBAfWL6Q")

# Set up environment
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"

print("=" * 80)
print("🚀 AI Multi-Agent Chat - Gradio Interface")
print("=" * 80)


# ============================================================================
# SIMPLE AGENT (Day 1A)
# ============================================================================

simple_agent = Agent(
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

simple_runner = InMemoryRunner(agent=simple_agent)
print("✅ Simple Agent initialized")


# ============================================================================
# MULTI-AGENT SYSTEMS (Day 1B)
# ============================================================================

# 1. Research & Summarization System (LLM-based orchestration)
def build_research_system():
    research_agent = Agent(
        name="ResearchAgent",
        model="gemini-2.5-flash-lite",
        instruction="""You are a specialized research agent. Your only job is to use the
        google_search tool to find 2-3 pieces of relevant information on the given topic
        and present the findings with citations.""",
        tools=[google_search],
        output_key="research_findings",
    )

    summarizer_agent = Agent(
        name="SummarizerAgent",
        model="gemini-2.5-flash-lite",
        instruction="""Read the provided research findings: {research_findings}
        Create a concise summary as a bulleted list with 3-5 key points.""",
        output_key="final_summary",
    )

    root_agent = Agent(
        name="ResearchCoordinator",
        model="gemini-2.5-flash-lite",
        instruction="""You are a research coordinator. Your goal is to answer the user's query by orchestrating a workflow.
        1. First, you MUST call the `ResearchAgent` tool to find relevant information.
        2. Next, after receiving the research findings, you MUST call the `SummarizerAgent` tool to create a concise summary.
        3. Finally, present the final summary clearly to the user as your response.""",
        tools=[
            AgentTool(research_agent),
            AgentTool(summarizer_agent)
        ],
    )

    return root_agent


# 2. Blog Pipeline (Sequential agents)
def build_blog_pipeline():
    outline_agent = Agent(
        name="OutlineAgent",
        model="gemini-2.5-flash-lite",
        instruction="""Create a blog outline for the given topic with:
        1. A catchy headline
        2. An introduction hook
        3. 3-5 main sections with 2-3 bullet points for each
        4. A concluding thought""",
        output_key="blog_outline",
    )

    writer_agent = Agent(
        name="WriterAgent",
        model="gemini-2.5-flash-lite",
        instruction="""Following this outline strictly: {blog_outline}
        Write a brief, 200 to 300-word blog post with an engaging and informative tone.""",
        output_key="blog_draft",
    )

    editor_agent = Agent(
        name="EditorAgent",
        model="gemini-2.5-flash-lite",
        instruction="""Edit this draft: {blog_draft}
        Your task is to polish the text by fixing any grammatical errors,
        improving the flow and sentence structure, and enhancing overall clarity.""",
        output_key="final_blog",
    )

    root_agent = SequentialAgent(
        name="BlogPipeline",
        sub_agents=[outline_agent, writer_agent, editor_agent],
    )

    return root_agent


# 3. Parallel Research System
def build_parallel_research():
    tech_researcher = Agent(
        name="TechResearcher",
        model="gemini-2.5-flash-lite",
        instruction="""Research the latest AI/ML trends. Include 3 key developments,
        the main companies involved, and the potential impact. Keep the report very concise (100 words).""",
        tools=[google_search],
        output_key="tech_research",
    )

    health_researcher = Agent(
        name="HealthResearcher",
        model="gemini-2.5-flash-lite",
        instruction="""Research recent medical breakthroughs. Include 3 significant advances,
        their practical applications, and estimated timelines. Keep the report concise (100 words).""",
        tools=[google_search],
        output_key="health_research",
    )

    finance_researcher = Agent(
        name="FinanceResearcher",
        model="gemini-2.5-flash-lite",
        instruction="""Research current fintech trends. Include 3 key trends,
        their market implications, and the future outlook. Keep the report concise (100 words).""",
        tools=[google_search],
        output_key="finance_research",
    )

    aggregator_agent = Agent(
        name="AggregatorAgent",
        model="gemini-2.5-flash-lite",
        instruction="""Combine these three research findings into a single executive summary:

        **Technology Trends:**
        {tech_research}

        **Health Breakthroughs:**
        {health_research}

        **Finance Innovations:**
        {finance_research}

        Your summary should highlight common themes, surprising connections, and the most important
        key takeaways from all three reports. The final summary should be around 200 words.""",
        output_key="executive_summary",
    )

    parallel_research_team = ParallelAgent(
        name="ParallelResearchTeam",
        sub_agents=[tech_researcher, health_researcher, finance_researcher],
    )

    root_agent = SequentialAgent(
        name="ResearchSystem",
        sub_agents=[parallel_research_team, aggregator_agent],
    )

    return root_agent


# Initialize multi-agent systems
research_system = build_research_system()
blog_pipeline = build_blog_pipeline()
parallel_research = build_parallel_research()

research_runner = InMemoryRunner(agent=research_system)
blog_runner = InMemoryRunner(agent=blog_pipeline)
parallel_runner = InMemoryRunner(agent=parallel_research)

print("✅ Research System initialized")
print("✅ Blog Pipeline initialized")
print("✅ Parallel Research System initialized")
print("=" * 80)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def run_agent_query(runner, message):
    """Run an agent query and return the response"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(runner.run_debug(message))
        loop.close()

        if response and len(response) > 0:
            return response[0].content.parts[0].text
        else:
            return "❌ Sorry, I couldn't generate a response. Please try again."

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return f"❌ Error: {str(e)}"


# ============================================================================
# GRADIO INTERFACE FUNCTIONS
# ============================================================================

def simple_chat(message, history):
    """Simple chat with single agent"""
    if not message or not message.strip():
        return ""

    bot_message = run_agent_query(simple_runner, message)
    return bot_message


def research_chat(topic):
    """Research & Summarization demo"""
    if not topic or not topic.strip():
        return "Please enter a research topic."

    return run_agent_query(research_runner, topic)


def blog_chat(topic):
    """Blog Pipeline demo"""
    if not topic or not topic.strip():
        return "Please enter a blog topic."

    return run_agent_query(blog_runner, f"Write a blog post about {topic}")


def parallel_chat(briefing_type):
    """Parallel Research demo"""
    query = f"Run the daily executive briefing on {briefing_type}"
    return run_agent_query(parallel_runner, query)


# ============================================================================
# CUSTOM CSS
# ============================================================================

custom_css = """
.gradio-container {
    max-width: 1200px !important;
}

/* Orange-mauve gradient header */
#header-banner {
    background: linear-gradient(135deg, #ff6b35 0%, #c44569 50%, #8b5a9e 100%);
    color: white;
    padding: 30px;
    border-radius: 10px;
    text-align: center;
    margin-bottom: 20px;
    box-shadow: 0 4px 15px rgba(255, 107, 53, 0.3);
}

/* Orange-mauve gradient for buttons */
button.primary {
    background: linear-gradient(135deg, #ff6b35 0%, #c44569 100%) !important;
    border: none !important;
}

/* Accent colors */
.chatbot .message.bot {
    background: linear-gradient(135deg, rgba(255, 107, 53, 0.1) 0%, rgba(196, 69, 105, 0.1) 100%) !important;
    border-left: 3px solid #ff6b35 !important;
}

/* Tab styling */
.tab-nav button.selected {
    border-bottom: 3px solid #ff6b35 !important;
}
"""


# ============================================================================
# GRADIO INTERFACE
# ============================================================================

with gr.Blocks(
    theme=gr.themes.Soft(
        primary_hue="orange",
        secondary_hue="pink",
    ),
    css=custom_css,
    title="AI Multi-Agent Chat",
) as demo:

    # Header
    gr.HTML("""
        <div id="header-banner">
            <h1>🤖 AI Multi-Agent Chat</h1>
            <h3>Powered by Google ADK & Gemini 2.5 Flash Lite</h3>
            <p>Explore single agents and multi-agent systems from Kaggle's 5-Day AI Agents Course</p>
        </div>
    """)

    # Tabs for different agent types
    with gr.Tabs():

        # Tab 1: Simple Chat (Day 1A)
        with gr.Tab("💬 Simple Chat"):
            gr.Markdown("""
                ### Single Agent Chat (Day 1A)
                A helpful assistant that can search the web and answer your questions.
            """)

            simple_chatbot = gr.Chatbot(
                height=400,
                show_label=False,
                avatar_images=(
                    None,
                    "https://em-content.zobj.net/source/apple/391/robot_1f916.png"
                ),
            )

            with gr.Row():
                simple_msg = gr.Textbox(
                    placeholder="Ask me anything...",
                    show_label=False,
                    scale=9,
                )
                simple_submit = gr.Button("Send 📤", variant="primary", scale=1)

            gr.Examples(
                examples=[
                    "What's the weather in Tokyo?",
                    "What are the latest tech news?",
                    "Explain quantum computing in simple terms",
                ],
                inputs=simple_msg,
            )

            simple_clear = gr.Button("🗑️ Clear Chat")

            def respond(message, chat_history):
                bot_message = simple_chat(message, chat_history)
                chat_history.append((message, bot_message))
                return "", chat_history

            simple_msg.submit(respond, [simple_msg, simple_chatbot], [simple_msg, simple_chatbot])
            simple_submit.click(respond, [simple_msg, simple_chatbot], [simple_msg, simple_chatbot])
            simple_clear.click(lambda: None, None, simple_chatbot, queue=False)

        # Tab 2: Research & Summarization (Day 1B)
        with gr.Tab("🔍 Research System"):
            gr.Markdown("""
                ### Research & Summarization System (Day 1B)
                Multi-agent system with **LLM-based orchestration**:
                1. **Research Agent** searches the web for information
                2. **Summarizer Agent** creates a concise summary
                3. **Coordinator Agent** orchestrates the workflow
            """)

            research_topic = gr.Textbox(
                label="Research Topic",
                placeholder="e.g., What are the latest advancements in quantum computing?",
            )

            research_btn = gr.Button("🔬 Research & Summarize", variant="primary")

            research_output = gr.Textbox(
                label="Summary",
                lines=15,
                show_copy_button=True,
            )

            gr.Examples(
                examples=[
                    "What are the latest advancements in quantum computing?",
                    "Recent developments in renewable energy",
                    "Current trends in artificial intelligence",
                ],
                inputs=research_topic,
            )

            research_btn.click(research_chat, inputs=research_topic, outputs=research_output)

        # Tab 3: Blog Pipeline (Day 1B)
        with gr.Tab("✏️ Blog Writer"):
            gr.Markdown("""
                ### Blog Post Pipeline (Day 1B)
                **Sequential agent workflow**:
                1. **Outline Agent** creates a structured outline
                2. **Writer Agent** writes the blog post
                3. **Editor Agent** polishes and refines the content
            """)

            blog_topic = gr.Textbox(
                label="Blog Topic",
                placeholder="e.g., Benefits of multi-agent systems",
            )

            blog_btn = gr.Button("📝 Generate Blog Post", variant="primary")

            blog_output = gr.Textbox(
                label="Blog Post",
                lines=20,
                show_copy_button=True,
            )

            gr.Examples(
                examples=[
                    "Benefits of multi-agent systems",
                    "How AI is transforming healthcare",
                    "The future of work with AI assistants",
                ],
                inputs=blog_topic,
            )

            blog_btn.click(blog_chat, inputs=blog_topic, outputs=blog_output)

        # Tab 4: Parallel Research (Day 1B)
        with gr.Tab("📊 Executive Briefing"):
            gr.Markdown("""
                ### Parallel Multi-Topic Research (Day 1B)
                **Parallel agents with aggregation**:
                1. **Tech, Health, Finance Researchers** work in parallel
                2. Each searches for trends in their domain (simultaneously!)
                3. **Aggregator Agent** combines findings into executive summary
            """)

            briefing_type = gr.Dropdown(
                choices=[
                    "Technology, Health, and Finance",
                    "AI, Sustainability, and Education",
                    "Cybersecurity, Cloud Computing, and DevOps",
                ],
                value="Technology, Health, and Finance",
                label="Briefing Topics",
            )

            parallel_btn = gr.Button("📈 Generate Executive Briefing", variant="primary")

            parallel_output = gr.Textbox(
                label="Executive Summary",
                lines=20,
                show_copy_button=True,
            )

            parallel_btn.click(parallel_chat, inputs=briefing_type, outputs=parallel_output)

        # Tab 5: About
        with gr.Tab("ℹ️ About"):
            gr.Markdown("""
                # About This Application

                ## 🎓 Learning Journey

                This application demonstrates concepts from **Kaggle's 5-Day AI Agents Course**:

                ### Day 1A: From Prompt to Action
                - ✅ Built first AI agent with Google Search tool
                - ✅ Learned the Think → Act → Observe → Respond loop
                - ✅ Understood grounding and source attribution
                - ✅ Deployed simple chat interface

                ### Day 1B: Agent Architectures
                - ✅ **LLM-Based Orchestration**: Root agent coordinates sub-agents using AgentTool
                - ✅ **Sequential Workflows**: SequentialAgent for pipeline processing
                - ✅ **Parallel Processing**: ParallelAgent for concurrent execution
                - ✅ **Output Keys**: Data passing between agents using {output_key} syntax

                ## 🏗️ Technical Architecture

                ### Single Agent (Day 1A)
                ```
                User Query → Agent → Google Search (if needed) → Response
                ```

                ### Multi-Agent Systems (Day 1B)

                **Research System (LLM Orchestration):**
                ```
                Coordinator → ResearchAgent → SummarizerAgent → Final Response
                ```

                **Blog Pipeline (Sequential):**
                ```
                OutlineAgent → WriterAgent → EditorAgent → Final Blog
                ```

                **Executive Briefing (Parallel + Sequential):**
                ```
                ┌─ TechResearcher ─────┐
                ├─ HealthResearcher ───┤ → AggregatorAgent → Summary
                └─ FinanceResearcher ──┘
                ```

                ## 🛠️ Technology Stack

                - **Framework**: Google Agent Development Kit (ADK)
                - **Model**: Gemini 2.5 Flash Lite
                - **Tools**: Google Search
                - **Interface**: Gradio
                - **Deployment**: Hugging Face Spaces

                ## 📚 Key Concepts Learned

                1. **Agent Components**: name, model, instruction, tools, output_key
                2. **Tool Types**: FunctionTool (Python functions), AgentTool (other agents)
                3. **Workflow Patterns**:
                   - LLM-based orchestration (flexible, intelligent routing)
                   - Sequential (step-by-step pipeline)
                   - Parallel (concurrent execution)
                   - Loop (iterative refinement)
                4. **Data Flow**: Using output_key and {placeholder} syntax
                5. **Grounding**: Backing responses with verifiable sources

                ## 🚀 Performance Benefits

                | Pattern | Speed | Use Case |
                |---------|-------|----------|
                | LLM Orchestration | Flexible | Complex decision trees |
                | Sequential | Predictable | Step-by-step workflows |
                | Parallel | Fast | Independent tasks |
                | Loop | Iterative | Refinement & validation |

                ## 📖 Source Code

                Built as part of the [Kaggle 5-Day AI Agents Course](https://www.kaggle.com/learn-guide/5-day-agents)

                **GitHub**: Coming soon!

                ---

                Made with ❤️ using Google ADK and Gradio
            """)


if __name__ == "__main__":
    print("\n🌐 Starting Multi-Agent Gradio interface...")
    print("📱 The interface will open in your browser automatically")
    print("\n✨ Features:")
    print("   - Simple Chat (Day 1A)")
    print("   - Research & Summarization (Day 1B)")
    print("   - Blog Post Pipeline (Day 1B)")
    print("   - Executive Briefing (Day 1B)")
    print("\nPress CTRL+C to stop the server\n")

    # Launch the app
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
    )
