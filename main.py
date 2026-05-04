from src.research_agent.agent import (create_research_agent, create_user_proxy, register_tools)


def main() -> None:
    research_agent = create_research_agent()
    user_proxy = create_user_proxy()

    register_tools(
        research_agent=research_agent,
        user_proxy=user_proxy,
    )

    user_request = (
        "Find a paper about retrieval-augmented generation published after 2022 "
        "with at least 500 citations. Explain why the paper is relevant and provide "
        "the source of the citation count."
    )

    user_proxy.initiate_chat(
        research_agent,
        message=user_request,
    )


if __name__ == "__main__":
    main()