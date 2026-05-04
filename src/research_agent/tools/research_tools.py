import json
from src.research_agent.models import SearchConstraints
from src.research_agent.workflow import search_and_filter_papers


def search_research_papers(
    topic: str,
    year_operator: str = "none",
    year: int | None = None,
    citation_operator: str = "none",
    citation_count: int | None = None,
    limit: int = 25,
) -> str:
    """
    Search for academic research papers using the OpenAlex tool and filter them
    by publication-year and citation-count constraints using the workflow layer.

    This function is registered as an AutoGen tool.

    Args:
        topic: Research topic to search for.
        year_operator: One of "none", "before", "after", or "in".
        year: Target publication year.
        citation_operator: One of "none", "at_least", "more_than", "less_than", or "approximate".
        citation_count: Target citation count.
        limit: Maximum number of papers to search.

    Returns:
        A JSON string containing the applied constraints, valid papers, rejected paper count, and errors.
    """

    search_limit = max(limit, 25)

    constraints = SearchConstraints(
        topic=topic,
        year_operator=year_operator,
        year=year,
        citation_operator=citation_operator,
        citation_count=citation_count,
        limit=search_limit,
    )

    result = search_and_filter_papers(constraints)

    response = {
        "constraints": {
            "topic": constraints.topic,
            "year_operator": constraints.year_operator,
            "year": constraints.year,
            "citation_operator": constraints.citation_operator,
            "citation_count": constraints.citation_count,
            "limit": constraints.limit,
        },
        "valid_papers": [
            {
                "title": paper.title,
                "authors": paper.authors[:5],
                "publication_year": paper.publication_year,
                "citation_count": paper.citation_count,
                "citation_source": paper.citation_source,
                "url": paper.url,
                "doi": paper.doi,
                "venue": paper.venue,
                "abstract": paper.abstract[:800] if paper.abstract else None,
                "source_api": paper.source_api,
            }
            for paper in result.valid_papers[:3]
        ],
        "rejected_paper_count": len(result.rejected_papers),
        "errors": result.errors,
    }

    return json.dumps(response, indent=2)