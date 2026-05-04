from autogen import ConversableAgent
from src.research_agent.config import LLM_CONFIG
from src.research_agent.tools.research_tools import search_research_papers


def create_research_agent() -> ConversableAgent:
    research_agent = ConversableAgent(
        name="research_agent",
        system_message=(
            "You are an AI research assistant for finding academic research papers. "
            "Your task is to understand the user's request, identify research-paper constraints, "
            "use the available tools to search for candidate papers, and return a structured, "
            "evidence-based answer. "
            "\n\n"
            "You have access to a tool called search_research_papers. "
            "Use this tool whenever the user asks you to find research papers. "
            "\n\n"
            "The tool supports these parameters: "
            "topic, year_operator, year, citation_operator, citation_count, and limit. "
            "\n\n"
            "Valid year_operator values are: none, before, after, in. "
            "Valid citation_operator values are: none, at_least, more_than, less_than, approximate. "
            "\n\n"
            "After receiving a tool result, your next response must be the final answer. "
            "Do not call the tool again unless the tool result contains an error. "
            "If valid_papers is empty, do not call the tool again. State that no valid paper "
            "was found, mention the failed constraints, and end with TERMINATE. "
            "If valid_papers contains papers, select exactly one paper from valid_papers and "
            "return it using the required structure. "
            "Do not write a general essay or broad analysis. "
            "\n\n"
            "You must not invent paper metadata, citation counts, URLs, DOIs, authors, or publication years. "
            "Citation counts must come from tool results. "
            "\n\n"
            "Your final answer must use this structure:\n"
            "Title: ...\n"
            "Authors: ...\n"
            "Publication year: ...\n"
            "Citation count: ...\n"
            "Citation source: ...\n"
            "URL: ...\n"
            "DOI: ...\n"
            "Why this paper matches the request: ...\n"
            "\n\n"
            "If no paper satisfies the user's constraints, say that no valid paper was found and explain which "
            "constraints could not be satisfied. "
            "\n\n"
            "When the task is complete, end your response with TERMINATE."
        ),
        llm_config=LLM_CONFIG,
    )

    return research_agent


def create_user_proxy() -> ConversableAgent:
    user_proxy = ConversableAgent(
        name="user_proxy",
        llm_config=False,
        is_termination_msg=lambda msg: (msg.get("content") is not None and "TERMINATE" in msg["content"]),
        human_input_mode="NEVER",
    )

    return user_proxy


def register_tools(research_agent: ConversableAgent, user_proxy: ConversableAgent) -> None:
    """
    Register Python functions as AutoGen tools.

    The research agent can suggest calling the tool.
    The user proxy executes the actual Python function.
    """
    research_agent.register_for_llm(
        name="search_research_papers",
        description=(
            "Search for academic research papers using OpenAlex. "
            "The tool returns JSON with applied constraints, valid_papers, rejected_paper_count, and errors. "
            "Each valid paper includes title, authors, publication_year, citation_count, citation_source, URL, DOI, venue, abstract, and source_api. "
            "Use the returned valid_papers only; do not invent metadata."
        ),
    )(search_research_papers)

    user_proxy.register_for_execution(
        name="search_research_papers"
    )(search_research_papers)