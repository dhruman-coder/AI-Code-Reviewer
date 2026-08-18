import ollama
import json


def review_code(code, language):

    prompt = f"""
You are an expert software engineer and code reviewer.

Analyze the following {language} code.

Identify only REAL problems present in the submitted code.

Return VALID JSON ONLY.

Use exactly this structure:

{{
    "score": 0,
    "bugs": [],
    "security": [],
    "performance": [],
    "quality": [],
    "suggestions": [],
    "improved_code": ""
}}

Rules:

- score must be an integer from 0 to 100.
- bugs must contain actual bugs only.
- security must contain actual security vulnerabilities only.
- performance must contain actual performance problems only.
- quality must contain actual code quality issues.
- suggestions must contain practical improvements.
- improved_code must contain corrected code when necessary.
- If a category has no issues, return an empty list.
- Do not invent problems.
- Do not report normal arithmetic operations as security vulnerabilities.
- Do not claim a syntax error unless the code actually has invalid syntax.
- Do not mention SQL injection unless SQL is actually used.
- Do not recommend password hashing unless authentication or password storage is actually present.
- Do not report type hints as bugs.
- Do not report exception handling as a performance problem.
- Base every finding strictly on the submitted code.
- Return JSON only.
- Do not use Markdown.
- Do not add explanations outside the JSON.

Code:

{code}
"""

    response = ollama.chat(
        model="qwen2.5-coder:1.5b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    content = response["message"]["content"].strip()

    try:

        result = json.loads(content)

    except json.JSONDecodeError:

        try:

            start = content.find("{")
            end = content.rfind("}") + 1

            if start == -1 or end == 0:
                raise ValueError("No JSON object found")

            result = json.loads(
                content[start:end]
            )

        except (json.JSONDecodeError, ValueError):

            return {
                "score": None,
                "bugs": [],
                "security": [],
                "performance": [],
                "quality": [],
                "suggestions": [
                    "AI response could not be parsed."
                ],
                "improved_code": ""
            }

    required_keys = [
        "score",
        "bugs",
        "security",
        "performance",
        "quality",
        "suggestions",
        "improved_code"
    ]

    if not all(key in result for key in required_keys):

        return {
            "score": None,
            "bugs": [],
            "security": [],
            "performance": [],
            "quality": [],
            "suggestions": [
                "AI response was missing required fields."
            ],
            "improved_code": ""
        }

    if not isinstance(result["score"], int):

        result["score"] = None

    return result