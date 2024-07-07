import streamlit as st
from src.helper.static_main import static_main
from main import dynamic_main_function

st.set_page_config(layout="centered", page_title="Wanderlust Baba.AI", page_icon="🌍")


# Apply custom CSS for fixed title
st.markdown(
    """
    <style>
    .fixed-title {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background: transparent;
        color: black;
        font-size: 24px;
        font-weight: bold;
        padding: 10px;
        z-index: 1000;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Define a function to handle the navigation
def navigate():
    st.sidebar.title('Navigation')
    pages = ['Static Wanderlust Baba Page', 'Dynamic Wanderlust Baba Page']
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'Static Wanderlust Baba Page'

    selection = st.sidebar.radio("Go to", pages, index=pages.index(st.session_state.current_page))
    st.session_state.current_page = selection

# Call the navigation function
navigate()

# Initialize session states for each page if not already present
if 'static_page_state' not in st.session_state:
    st.session_state.static_page_state = {}
if 'dynamic_page_state' not in st.session_state:
    st.session_state.dynamic_page_state = {}

# Save the current state of the app
current_state = {key: st.session_state[key] for key in st.session_state.keys()}

# Add the fixed title at the top left
st.markdown('<div class="fixed-title">Wanderlust Baba.AI</div>', unsafe_allow_html=True)

# Conditionally display pages based on selection
if st.session_state.current_page == 'Static Wanderlust Baba Page':
    st.session_state.update(st.session_state.static_page_state)
    static_main()
    st.session_state.static_page_state = {key: st.session_state[key] for key in st.session_state.keys()}
elif st.session_state.current_page == 'Dynamic Wanderlust Baba Page':
    st.session_state.update(st.session_state.dynamic_page_state)
    dynamic_main_function()
    st.session_state.dynamic_page_state = {key: st.session_state[key] for key in st.session_state.keys()}

# Restore the saved state
st.session_state.update(current_state)
