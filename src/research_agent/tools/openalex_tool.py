import requests
from src.research_agent.models import Paper

OPENALEX_WORKS_URL = "https://api.openalex.org/works"

def search_openalex_papers(topic: str, limit: int = 10) -> list[Paper]:
    """
    Search OpenAlex for academic papers related to a topic.
    """

    params = {
        "search": topic,
        "per-page": limit,
        "sort": "cited_by_count:desc",
    }

    response = requests.get(
        OPENALEX_WORKS_URL,
        params=params,
        timeout=15,
    )

    response.raise_for_status()

    data = response.json()
    results = data.get("results", [])

    papers: list[Paper] = []

    for item in results:
        paper = _map_openalex_work_to_paper(item)
        papers.append(paper)

    return papers


def _map_openalex_work_to_paper(work: dict) -> Paper:
    """
    Convert one OpenAlex work result into the internal Paper model.
    """

    title = work.get("title") or "Unknown title"
    publication_year = work.get("publication_year")
    citation_count = work.get("cited_by_count")
    doi = work.get("doi")
    url = work.get("id")

    authors = _extract_authors(work)
    abstract = _extract_abstract(work)
    venue = _extract_venue(work)

    return Paper(
        title=title,
        authors=authors,
        publication_year=publication_year,
        citation_count=citation_count,
        citation_source="OpenAlex",
        url=url,
        doi=doi,
        abstract=abstract,
        venue=venue,
        source_api="OpenAlex",
    )


def _extract_authors(work: dict) -> list[str]:
    """
    Extract author names from an OpenAlex work.
    """

    authorships = work.get("authorships", [])
    authors: list[str] = []

    for authorship in authorships:
        author = authorship.get("author", {})
        display_name = author.get("display_name")

        if display_name:
            authors.append(display_name)

    return authors


def _extract_venue(work: dict) -> str | None:
    """
    Extract the publication venue/source name from an OpenAlex work.
    """

    primary_location = work.get("primary_location")

    if not primary_location:
        return None

    source = primary_location.get("source")

    if not source:
        return None

    return source.get("display_name")


def _extract_abstract(work: dict) -> str | None:
    """
    Reconstruct the abstract text from OpenAlex's inverted abstract index.
    """

    inverted_index = work.get("abstract_inverted_index")

    if not inverted_index:
        return None

    words_by_position: dict[int, str] = {}

    for word, positions in inverted_index.items():
        for position in positions:
            words_by_position[position] = word

    ordered_words = [
        words_by_position[position]
        for position in sorted(words_by_position)
    ]

    return " ".join(ordered_words)