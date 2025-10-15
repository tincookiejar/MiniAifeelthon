import pandas as pd
import streamlit as st

from modules.corpus import load_freq_df
from modules.features import compute_features_for_words, clarity_score
from modules.scoring import compute_difficulty, extract_difficult_words
from modules.rewriter import rewrite_sentence_with_simple_words
from modules.tokenizer import tokenize
from modules.utils import show_highlighted_diff 

st.set_page_config(page_title="문장 명확성 & 단어 난이도 교정기", layout="wide")
st.title("문장 명확성 & 단어 난이도 교정기")

# ----------------------------
# 1) word_freq.csv 로드
# ----------------------------
with st.spinner("단어 빈도 사전 로드 중..."):
    try:
        freq_df = load_freq_df(min_count=3)
        st.success(f"빈도 사전 로드 완료 (단어 수: {len(freq_df):,})")
    except FileNotFoundError as e:
        st.error(str(e))
        freq_df = None

# ----------------------------
# 2) 텍스트 입력 및 분석/교정
# ----------------------------
text = st.text_area("문장을 입력하세요", height=140, placeholder="예) 일반적으로 형이상학적 개념은 난해하다.")

th = st.slider("어려운 단어 임계치 (높을수록 더 엄격)", 0.0, 1.0, 0.6, 0.05)

analyze_btn = st.button("분석")
rewrite_btn = st.button("교정(쉬운 단어로 바꾸기)")

if text and freq_df is not None and (analyze_btn or rewrite_btn):
    words = tokenize(text)
    if not words:
        st.warning("형태소를 추출할 수 없습니다.")
    else:
        df_feats = compute_features_for_words(words, freq_df)
        df_scored = compute_difficulty(df_feats)

        # 명확성 점수
        cscore = clarity_score(text)
        st.metric(label="Clarity (낮을수록 명확)", value=f"{cscore:.2f}")

        st.markdown("**단어 난이도 테이블** (difficulty_score가 높을수록 어려움)")
        show_cols = ["word", "difficulty_score", "raw_freq", "morph_count", "syllable_count", "pos_variety"]
        st.dataframe(df_scored[show_cols].sort_values(["difficulty_score","word"], ascending=[False, True]),
                     use_container_width=True, height=300)

        difficult_words = extract_difficult_words(df_scored, threshold=th)
        st.write(f"어려운 단어 ({len(difficult_words)}개): {', '.join(difficult_words) if difficult_words else '없음'}")

        if rewrite_btn:
            with st.spinner("쉬운 단어로 치환 중..."):
                try:
                    simplified = rewrite_sentence_with_simple_words(text, difficult_words)
                    st.subheader("③ 교정 결과")

                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**원문**")
                        st.info(text)
                    with col2:
                        st.markdown("**교정문**")
                        st.success(simplified)

                    # ✅ 하이라이트 비교
                    st.subheader("④ 하이라이트 비교")
                    show_highlighted_diff(text, simplified)

                except Exception as e:
                    st.error(f"LLM 호출 오류: {e}")
                    st.info("OPENAI_API_KEY 환경 변수가 설정되었는지 확인하세요.")
