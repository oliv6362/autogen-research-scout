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
            "You must not invent paper metadata, citation counts, URLs, DOIs, authors, or publication years. "
            "Citation counts must come from tool results. "
            "\n\n"
            "When answering, include: "
            "paper title, authors, publication year, citation count, source of the citation count, "
            "paper URL or DOI, and a short explanation of why the paper matches the request. "
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
            "Filters papers by topic, publication year, and citation count. "
            "Returns paper title, authors, publication year, citation count, citation source, URL, DOI, venue, and abstract."
        ),
    )(search_research_papers)

    user_proxy.register_for_execution(
        name="search_research_papers"
    )(search_research_papers)