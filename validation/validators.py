"""
Deterministic validation functions for specific data types and business rules.
"""

import re
from typing import Any, List, Optional
from models.research_plan import FieldSpec
from utils.helpers import is_valid_email, is_valid_url


def validate_acceptance_rate(value: Any) -> Optional[str]:
    """Validate acceptance rate is a percentage between 0 and 100."""
    try:
        val_str = str(value).replace("%", "").strip()
        num = float(val_str)
        if not (0 <= num <= 100):
            return f"Acceptance rate {num}% is out of valid range (0-100%)"
    except (ValueError, TypeError):
        return f"Invalid numeric acceptance rate: '{value}'"
    return None


def validate_rank(value: Any) -> Optional[str]:
    """Validate rank is a positive integer or range (e.g. 501-600)."""
    val_str = str(value).strip()
    # Matches '1', '501-600', '=25', '#10'
    if not re.search(r"\d+", val_str):
        return f"Rank must contain numeric value: '{value}'"
    return None


def validate_email_field(value: Any) -> Optional[str]:
    """Validate email format."""
    if not is_valid_email(str(value)):
        return f"Invalid email format: '{value}'"
    return None


def validate_url_field(value: Any) -> Optional[str]:
    """Validate URL format and protocol."""
    if not is_valid_url(str(value)):
        return f"Invalid URL: '{value}'"
    return None


def run_deterministic_validations(field_spec: FieldSpec, value: Any) -> List[str]:
    """Run applicable deterministic validators for a field."""
    if value is None or str(value).strip().upper() == "N/A":
        return []

    errors: List[str] = []
    field_name_lower = field_spec.name.lower()
    data_type = field_spec.data_type.lower()

    if data_type == "email" or "email" in field_name_lower:
        err = validate_email_field(value)
        if err:
            errors.append(err)

    elif data_type == "url" or "website" in field_name_lower or "url" in field_name_lower or "link" in field_name_lower:
        err = validate_url_field(value)
        if err:
            errors.append(err)

    elif "acceptance_rate" in field_name_lower or (data_type == "percentage" and "rate" in field_name_lower):
        err = validate_acceptance_rate(value)
        if err:
            errors.append(err)

    elif "rank" in field_name_lower:
        err = validate_rank(value)
        if err:
            errors.append(err)

    return errors
