import math
import pandas as pd
from modules.tokenizer import tokenize, pos_variety

def morph_count(word: str) -> int:
    return len(tokenize(word))

def syllable_count(word: str) -> int:
    # 한글 음절 길이 기반
    return len(word)

def compute_features_for_words(words: list[str], freq_df: pd.DataFrame) -> pd.DataFrame:
    freq_map = dict(zip(freq_df["word"], freq_df["raw_freq"]))
    rows = []
    for w in words:
        f = int(freq_map.get(w, 0))
        rows.append({
            "word": w,
            "raw_freq": f,
            "log_freq": math.log(f + 1),
            "morph_count": morph_count(w),
            "syllable_count": syllable_count(w),
            "pos_variety": pos_variety(w),
        })
    return pd.DataFrame(rows)

def clarity_score(text: str) -> float:
    """
    간단한 명확성 점수: 토큰 길이 + 모호 패턴 수
    낮을수록 명확, 0~1 스케일
    """
    tokens = tokenize(text)
    length_penalty = min(len(tokens)/30, 1)  # 30토큰 이상문장은 불리하게
    vague_patterns = ["것 같다", "등등", "이런", "저런", "어느 정도", "사실상"]
    vague_hits = sum(1 for p in vague_patterns if p in text)
    score = min(length_penalty + vague_hits*0.2, 1.0)
    return round(score, 3)
