from kiwipiepy import Kiwi
import streamlit as st

@st.cache_resource
def get_kiwi():
    return Kiwi()

def tokenize(text: str):
    kiwi = get_kiwi()
    return [t.form for t in kiwi.tokenize(text)]

def pos_variety(word: str) -> int:
    kiwi = get_kiwi()
    return len(set([t.tag for t in kiwi.tokenize(word)]))
