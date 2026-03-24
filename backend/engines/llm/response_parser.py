import json
import re


def parse_llm_response(response_text: str) -> dict:
    """LLM 응답에서 JSON 추출"""
    json_match = re.search(r'```(?:json)?\s*([\s\S]*?)```', response_text)
    if json_match:
        try:
            return json.loads(json_match.group(1).strip())
        except json.JSONDecodeError:
            pass

    try:
        return json.loads(response_text.strip())
    except json.JSONDecodeError:
        pass

    return {
        "action": "approve",
        "reason": response_text[:500],
        "confidence": 0.5,
    }
