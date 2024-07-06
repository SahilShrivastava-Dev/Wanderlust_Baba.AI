import streamlit as st
from static_main import static_main
from dynamic_main import dynamic_main_function

st.set_page_config(layout="centered",page_title="Wanderlust Baba.AI",page_icon= "🌍")

# Define a function to handle the navigation
def navigate():
    st.sidebar.title('Navigation')
    pages =  ['Static Wanderlust Baba Page', 'Dynamic Wanderlust Baba Page']
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'Static Wanderlust Baba Page'

    selection = st.sidebar.radio("Go to", pages, index=pages.index(st.session_state.current_page))
    st.session_state.current_page = selection

# Call the navigation function
navigate()

# Conditionally display pages based on selection
if st.session_state.current_page == 'Static Wanderlust Baba Page':
    static_main()
elif st.session_state.current_page == 'Dynamic Wanderlust Baba Page':
    dynamic_main_function()

