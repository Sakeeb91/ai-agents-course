#!/usr/bin/env python3
"""
Day 1B: Multi-Agent Systems & Workflow Patterns
Demonstrates Sequential, Parallel, and Loop agent architectures
"""

import os
import asyncio
from google.adk.agents import Agent, SequentialAgent, ParallelAgent, LoopAgent
from google.adk.runners import InMemoryRunner
from google.adk.tools import AgentTool, FunctionTool, google_search

# Set up API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY environment variable is required.\n"
        "Set it with: export GOOGLE_API_KEY=your-key"
    )

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"

print("=" * 80)
print("🚀 Day 1B: Multi-Agent Systems & Workflow Patterns")
print("=" * 80)
print()


# ============================================================================
# EXAMPLE 1: LLM-Based Orchestration (Research & Summarization)
# ============================================================================

def build_research_system():
    """Build a multi-agent research and summarization system"""

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


# ============================================================================
# EXAMPLE 2: Sequential Agent (Blog Post Pipeline)
# ============================================================================

def build_blog_pipeline():
    """Build a sequential blog post creation pipeline"""

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


# ============================================================================
# EXAMPLE 3: Parallel Agent (Multi-Topic Research)
# ============================================================================

def build_parallel_research():
    """Build a parallel multi-topic research system"""

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


async def demo_all_patterns():
    """Run demonstrations of all agent patterns"""

    print("=" * 80)
    print("📋 EXAMPLE 1: LLM-Based Orchestration (Research & Summarization)")
    print("=" * 80)
    print()

    research_system = build_research_system()
    runner = InMemoryRunner(agent=research_system)

    print("Query: What are the latest advancements in quantum computing?")
    print()
    response = await runner.run_debug("What are the latest advancements in quantum computing?")
    print()

    print("=" * 80)
    print("✏️ EXAMPLE 2: Sequential Agent (Blog Post Pipeline)")
    print("=" * 80)
    print()

    blog_pipeline = build_blog_pipeline()
    runner = InMemoryRunner(agent=blog_pipeline)

    print("Topic: Benefits of multi-agent systems")
    print()
    response = await runner.run_debug("Write a blog post about the benefits of multi-agent systems")
    print()

    print("=" * 80)
    print("🔄 EXAMPLE 3: Parallel Agent (Multi-Topic Research)")
    print("=" * 80)
    print()

    parallel_research = build_parallel_research()
    runner = InMemoryRunner(agent=parallel_research)

    print("Briefing: Daily executive summary on Tech, Health, and Finance")
    print()
    response = await runner.run_debug("Run the daily executive briefing on Tech, Health, and Finance")
    print()

    print("=" * 80)
    print("✅ All Multi-Agent Patterns Demonstrated!")
    print("=" * 80)


if __name__ == "__main__":
    print("\n🤖 Day 1B: Multi-Agent Systems Demonstrations\n")
    asyncio.run(demo_all_patterns())
