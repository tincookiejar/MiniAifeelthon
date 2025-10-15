import difflib
import streamlit as st

def highlight_diff(original: str, corrected: str):
    """
    원문과 교정문을 비교하여 바뀐 부분에 색깔을 입힘.
    - 삭제된 단어: 빨간색
    - 추가된 단어: 초록색
    - 동일 단어: 검정색
    """
    diff = difflib.ndiff(original.split(), corrected.split())
    result = []
    for token in diff:
        if token.startswith("- "):
            result.append(f"<span style='color:red;background-color:#ffecec'>{token[2:]}</span>")
        elif token.startswith("+ "):
            result.append(f"<span style='color:green;background-color:#eaffea'>{token[2:]}</span>")
        elif token.startswith("  "):
            result.append(token[2:])
    return " ".join(result)

def show_highlighted_diff(original: str, corrected: str):
    """
    Streamlit에서 원문 vs 교정문을 하이라이트해서 보여줌
    """
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**원문 (하이라이트)**")
        st.markdown(highlight_diff(corrected, original), unsafe_allow_html=True)
    with col2:
        st.markdown("**교정문 (하이라이트)**")
        st.markdown(highlight_diff(original, corrected), unsafe_allow_html=True)
