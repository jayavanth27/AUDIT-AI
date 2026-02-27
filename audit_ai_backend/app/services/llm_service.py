"""Amazon Bedrock wrapper for generating working paper summaries."""

import boto3

from app.config import settings


bedrock = boto3.client("bedrock", region_name=settings.AWS_REGION)


def generate_working_paper(extracted: dict, risk_flags: list) -> str:
    """Build prompt and call Bedrock to create a draft working paper.

    Parameters
    ----------
    extracted : dict
        Structured fields extracted from documents.
    risk_flags : list
        List of risk flag dictionaries.

    Returns
    -------
    str
        Generated text, or empty string on failure.
    """
    # build prompt
    prompt = """
You are an audit assistant. Based on the extracted data and risk flags provide a professional working paper draft.

Extracted fields:
{fields}

Risk flags:
{flags}

Write a concise paragraph summarizing potential issues.
""".format(fields=extracted.get("fields"), flags=risk_flags)

    response = bedrock.invoke_model(
        modelId=settings.BEDROCK_MODEL_ID,
        body={
            "inputText": prompt,
        },
    )
    # depending on response structure
    output = response.get("body", {}).get("outputText")
    if isinstance(output, bytes):
        output = output.decode("utf-8")
    return output or ""
