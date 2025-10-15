import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

FEATURES = ["log_freq", "morph_count", "syllable_count", "pos_variety"]

WEIGHTS = {
    "log_freq_norm": -0.5,   # 빈도 높을수록 쉽다 → 음의 가중치
    "morph_count_norm": 0.3,
    "syllable_count_norm": 0.15,
    "pos_variety_norm": 0.05,
}

def normalize_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    scaler = MinMaxScaler()
    norm_cols = [f + "_norm" for f in FEATURES]
    out[norm_cols] = scaler.fit_transform(out[FEATURES])
    return out

def compute_difficulty(df_feats: pd.DataFrame) -> pd.DataFrame:
    df = normalize_features(df_feats)
    score = np.zeros(len(df))
    for k, w in WEIGHTS.items():
        score += df[k] * w
    score = (score - score.min()) / (score.max() - score.min() + 1e-12)
    df["difficulty_score"] = score
    return df

def extract_difficult_words(df_with_scores: pd.DataFrame, threshold: float) -> list[str]:
    return df_with_scores[df_with_scores["difficulty_score"] > threshold]["word"].tolist()
