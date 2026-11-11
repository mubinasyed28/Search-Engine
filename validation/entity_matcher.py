"""
Entity matching and verification — ensures retrieved sources belong to the requested target.
"""

import re
from typing import Optional, Tuple
from utils.helpers import extract_domain, normalize_entity_name


class EntityMatcher:
    """
    Validates whether a source URL or page snippet belongs to the target entity
    rather than an unrelated or similarly-named entity.
    """

    @staticmethod
    def match_entity(
        target_name: str,
        source_url: str,
        source_title: str = "",
        snippet: str = "",
    ) -> Tuple[bool, float, str]:
        """
        Check entity match.

        Returns:
            (is_match, score_0_to_1, explanation)
        """
        if not target_name:
            return True, 1.0, "No target entity name specified"

        norm_target = normalize_entity_name(target_name)
        norm_title = normalize_entity_name(source_title) if source_title else ""
        norm_snippet = normalize_entity_name(snippet) if snippet else ""
        domain = extract_domain(source_url)

        # 1. Exact or near-exact name in page title
        if norm_target in norm_title or norm_title in norm_target:
            return True, 0.95, f"Target name matched source title '{source_title}'"

        # 2. Token overlap with domain
        target_tokens = [t for t in re.split(r"[^a-z0-9]", norm_target) if len(t) > 2]
        domain_tokens = [t for t in re.split(r"[^a-z0-9]", domain) if len(t) > 2]

        matching_tokens = set(target_tokens) & set(domain_tokens)
        if matching_tokens and len(matching_tokens) >= max(1, len(target_tokens) // 2):
            return True, 0.90, f"Target tokens {matching_tokens} match domain {domain}"

        # 3. Target name in snippet
        if norm_target in norm_snippet:
            return True, 0.85, "Target name found in content snippet"

        # 4. Partial token match in snippet / title
        content_text = f"{norm_title} {norm_snippet}"
        matched_in_content = [t for t in target_tokens if t in content_text]
        score = len(matched_in_content) / max(1, len(target_tokens))

        if score >= 0.6:
            return True, score, f"Partial token match ({int(score * 100)}%)"

        return False, score, f"Low entity match confidence ({int(score * 100)}%) for '{target_name}'"
