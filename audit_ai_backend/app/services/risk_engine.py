"""Rule-based risk evaluation engine for extracted document data."""

from datetime import datetime
from typing import Any, Dict, List

from app.models.document import Document


class RiskRule:
    """Base class for a risk rule.

    Subclasses should implement ``apply`` returning a list of flag dicts.
    """

    def apply(self, document: Document, extracted: Dict[str, Any]) -> List[Dict[str, Any]]:
        raise NotImplementedError


class DuplicateInvoiceRule(RiskRule):
    """Flag documents with invoice numbers that appear multiple times.

    (Database query placeholder in MVP.)
    """

    def apply(self, document: Document, extracted: Dict[str, Any]) -> List[Dict[str, Any]]:
        flags = []
        # actual duplication check should query DB; placeholder
        if "invoice_number" in extracted.get("fields", {}):
            invoice = extracted["fields"]["invoice_number"]
            # TODO: query db for same invoice in other documents
            # if duplicate found:
            #    flags.append({..})
        return flags


class RoundNumberRule(RiskRule):
    """Flag amounts that are exact multiples of 1000."""

    def apply(self, document: Document, extracted: Dict[str, Any]) -> List[Dict[str, Any]]:
        flags = []
        amt = extracted.get("fields", {}).get("amount")
        if amt is not None and amt % 1000 == 0:
            flags.append(
                {
                    "rule": "ROUND_NUMBER",
                    "severity": "medium",
                    "message": "Transaction amount is a round number",
                }
            )
        return flags


class YearEndRule(RiskRule):
    """Flag transactions that occur near the end of the year (Dec 26+)."""

    def apply(self, document: Document, extracted: Dict[str, Any]) -> List[Dict[str, Any]]:
        flags = []
        date_str = extracted.get("fields", {}).get("date")
        if date_str:
            try:
                dt = datetime.fromisoformat(date_str)
                if dt.month == 12 and dt.day >= 26:
                    flags.append(
                        {
                            "rule": "YEAR_END",
                            "severity": "low",
                            "message": "Transaction near year-end",
                        }
                    )
            except ValueError:
                pass
        return flags


class MissingFieldsRule(RiskRule):
    """Flag documents missing any of the required fields."""

    def apply(self, document: Document, extracted: Dict[str, Any]) -> List[Dict[str, Any]]:
        flags = []
        required = ["invoice_number", "amount", "date"]
        for field in required:
            if field not in extracted.get("fields", {}):
                flags.append(
                    {
                        "rule": "MISSING_FIELD",
                        "severity": "high",
                        "message": f"Required field {field} is missing",
                    }
                )
        return flags


RULES = [
    DuplicateInvoiceRule(),
    RoundNumberRule(),
    YearEndRule(),
    MissingFieldsRule(),
]


def evaluate(document: Document, extracted: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Run all configured rules against a document and return collected flags."""
    flags: List[Dict[str, Any]] = []
    for rule in RULES:
        flags.extend(rule.apply(document, extracted))
    return flags
