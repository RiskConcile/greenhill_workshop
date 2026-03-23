import streamlit as st

st.set_page_config(
    page_title="Greenhill Robo-Advisor",
    page_icon="📈",
    layout="centered",
)

st.title("Greenhill Robo-Advisor")
st.caption("An educational prototype — not financial advice.")

st.markdown("""
Use the sidebar to navigate:

- **Investor Form** — submit your investment profile
- **Portfolio** — view your generated portfolio suggestion
""")
