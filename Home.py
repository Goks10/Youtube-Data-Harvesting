import streamlit as st
page_by_img = """
<style>
[data-testid="stAppViewContainer"]{
background-color: #5d6fff;
opacity: 1;
background-image: radial-gradient(circle at center center, #f8f8f8, #5d6fff), repeating-radial-gradient(circle at center center, #f8f8f8, #f8f8f8, 9px, transparent 18px, transparent 9px);
background-blend-mode: multiply;
}
</style>
"""
st.markdown(page_by_img, unsafe_allow_html=True)
st.title('Youtube Data Harvesting and Warehousing')
if st.button('Click here to Viewproject'):
    st.switch_page(r'pages/Data.py')
