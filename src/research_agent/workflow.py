from src.research_agent.models import Paper, SearchConstraints, SearchResult
from src.research_agent.tools.openalex_tool import search_openalex_papers


def search_and_filter_papers(constraints: SearchConstraints) -> SearchResult:
    """
    Search for papers using the external OpenAlex tool and filter the results
    using deterministic year and citation constraints.

    Args:
        constraints: The topic, year constraint, citation constraint, and result
            limit extracted from the user's request.

    Returns:
        A SearchResult containing valid papers and rejected papers.
    """

    try:
        papers = search_openalex_papers(
            topic=constraints.topic,
            limit=constraints.limit,
        )
    except Exception as error:
        return SearchResult(
            constraints=constraints,
            errors=[f"OpenAlex search failed: {error}"],
        )

    return filter_papers_by_constraints(
        papers=papers,
        constraints=constraints,
    )


def filter_papers_by_constraints(papers: list[Paper], constraints: SearchConstraints) -> SearchResult:
    """
    Split papers into valid and rejected lists based on the user's constraints.
    """

    valid_papers: list[Paper] = []
    rejected_papers: list[Paper] = []

    for paper in papers:
        if _paper_matches_constraints(paper, constraints):
            valid_papers.append(paper)
        else:
            rejected_papers.append(paper)

    return SearchResult(
        constraints=constraints,
        valid_papers=valid_papers,
        rejected_papers=rejected_papers,
    )


def _paper_matches_constraints(paper: Paper, constraints: SearchConstraints) -> bool:
    """
    Check whether a paper satisfies all required constraints.
    """

    if not paper.has_required_metadata():
        return False

    if not _paper_matches_year_constraint(paper, constraints):
        return False

    if not _paper_matches_citation_constraint(paper, constraints):
        return False

    return True


def _paper_matches_year_constraint(paper: Paper, constraints: SearchConstraints) -> bool:
    """
    Check whether a paper satisfies the publication-year constraint.
    """

    if not constraints.has_year_constraint():
        return True

    if paper.publication_year is None:
        return False

    if constraints.year_operator == "before":
        return paper.publication_year < constraints.year

    if constraints.year_operator == "after":
        return paper.publication_year > constraints.year

    if constraints.year_operator == "in":
        return paper.publication_year == constraints.year

    return False


def _paper_matches_citation_constraint(paper: Paper, constraints: SearchConstraints) -> bool:
    """
    Check whether a paper satisfies the citation-count constraint.
    """

    if not constraints.has_citation_constraint():
        return True

    if paper.citation_count is None:
        return False

    if constraints.citation_operator == "at_least":
        return paper.citation_count >= constraints.citation_count

    if constraints.citation_operator == "more_than":
        return paper.citation_count > constraints.citation_count

    if constraints.citation_operator == "less_than":
        return paper.citation_count < constraints.citation_count

    if constraints.citation_operator == "approximate":
        lower_bound, upper_bound = _approximate_citation_range(constraints.citation_count)
        return lower_bound <= paper.citation_count <= upper_bound

    return False


def _approximate_citation_range(target_count: int) -> tuple[int, int]:
    """
    Create a simple 20% tolerance range for approximate citation constraints.
    """

    tolerance = 0.20
    lower_bound = int(target_count * (1 - tolerance))
    upper_bound = int(target_count * (1 + tolerance))

    return lower_bound, upper_bound