"""
Provenance tracking and source authority classification.
"""

from typing import Optional
from models.research_result import FieldResult, SourceType
from utils.helpers import extract_domain


def classify_source_type(url: str, official_domain: Optional[str] = None) -> SourceType:
    """Classify the source type of a URL."""
    if not url:
        return SourceType.OTHER

    domain = extract_domain(url).lower()

    if official_domain and (official_domain.lower() in domain or domain in official_domain.lower()):
        return SourceType.OFFICIAL

    if domain.endswith(".gov") or ".gov." in domain or ".edu" in domain or ".ac." in domain:
        return SourceType.GOVERNMENT

    # Ranking domains
    ranking_domains = [
        "topuniversities.com",
        "timeshighereducation.com",
        "usnews.com",
        "shanghairanking.com",
        "forbes.com",
    ]
    if any(rd in domain for rd in ranking_domains):
        return SourceType.RANKING_SOURCE

    # Reputable secondary sources
    reputable = [
        "wikipedia.org",
        "reuters.com",
        "bloomberg.com",
        "bbc.com",
        "nytimes.com",
    ]
    if any(rep in domain for rep in reputable):
        return SourceType.REPUTABLE_SECONDARY

    return SourceType.WEB_SEARCH


def enrich_field_provenance(
    field_result: FieldResult,
    official_domain: Optional[str] = None,
) -> FieldResult:
    """Ensure provenance fields are fully populated."""
    if field_result.source_url and field_result.source_type == SourceType.OTHER:
        field_result.source_type = classify_source_type(
            field_result.source_url, official_domain
        )
    return field_result
