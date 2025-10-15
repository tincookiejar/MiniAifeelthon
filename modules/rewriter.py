import os
from openai import OpenAI

def _get_client() -> OpenAI:
    # 환경 변수 OPENAI_API_KEY 사용. 없으면 에러 발생.
    # 테스트용으로 코드에 직접 넣고 싶다면: OpenAI(api_key="sk-...")
    return OpenAI()

def rewrite_sentence_with_simple_words(text: str, difficult_words: list[str]) -> str:
    """
    LLM을 사용해 '지정된 어려운 단어들'만 더 쉬운 표현으로 바꿔달라고 요청.
    문장의 의미는 유지하고, 가능한 한 간결하게.
    """
    if not difficult_words:
        return text

    client = _get_client()
    prompt = f"""
아래 문장에서 지정한 '어려운 단어'들을 더 쉬운 한국어로 바꾸어 주세요.
- 문장의 의미는 유지합니다.
- 바꾸지 않아도 되는 단어는 그대로 둡니다.
- 전체 문장을 자연스럽게 다듬되, 과한 의역은 피합니다.

어려운 단어 목록: {", ".join(sorted(set(difficult_words)))}

문장:
{text}
"""

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "당신은 한국어 문장을 쉬운 단어로 자연스럽게 바꾸는 교정 전문가입니다."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    return res.choices[0].message.content.strip()
