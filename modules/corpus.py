import os
import pandas as pd

FREQ_PATH = os.path.join("data", "word_freq.csv")

def load_freq_df(min_count=3) -> pd.DataFrame:
    """
    data/word_freq.csv 로부터 빈도 사전 로드
    """
    if not os.path.exists(FREQ_PATH):
        raise FileNotFoundError("data/word_freq.csv 파일이 없습니다")
    df = pd.read_csv(FREQ_PATH)
    df = df[df["raw_freq"] >= min_count].reset_index(drop=True)
    return df
