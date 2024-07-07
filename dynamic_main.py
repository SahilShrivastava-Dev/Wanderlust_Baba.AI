import os
import streamlit as st
from dotenv import load_dotenv
import base64
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.llms import HuggingFaceEndpoint
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# CSS for Background Video and Content Styling
def set_css():
    st.markdown("""
        <style>
            #myVideo {
                position: fixed;
                right: 0;
                bottom: 0;
                min-width: 100%; 
                min-height: 100%;
            }
            .content {
                position: fixed;
                bottom: 0;
                background: rgba(0, 0, 0, 0.5);
                color: #f1f1f1;
                width: 100%;
                padding: 20px;
            }
            [data-testid="stHeader"], [data-testid="stToolbar"] {
                background: transparent;
            }
            [data-testid="stBottom"] > div {
                background: transparent;
            }
            [data-testid="stChatMessage"],[data-testid="stHeading"] {
                background-color: rgba(255, 255, 255, 0.5); 
                padding: 10px; 
                border-radius: 10px; 
                backdrop-filter: blur(3px); 
            }
        </style>
    """, unsafe_allow_html=True)


def embed_video(video_path):
    st.markdown(f"""
        <video autoplay muted loop id="myVideo" style="object-fit: cover; width: 100%; height: 100%;">
            <source src="data:video/mp4;base64,{get_video_as_base64(video_path)}" type="video/mp4">
            Your browser does not support HTML5 video.
        </video>
    """, unsafe_allow_html=True)

# Function to get video as base64
def get_video_as_base64(file_path):
    with open(file_path, "rb") as video_file:
        b64_string = base64.b64encode(video_file.read()).decode()
    return b64_string


def chatbot():
    
    st.subheader("""
                    🌍Introducing **Wanderlust Baba.Ai**🌍 \n
                    
                    The advanced AI-powered chatbot designed to make travel planning effortless and enjoyable. ✨ As your personal travel guru, Wanderlust Baba.Ai provides:

                    🗺️ **Expert Guidance:** Tailored travel recommendations just for you.

                    📡 **Real-Time Updates:** Stay informed with the latest travel advisories and weather updates.

                    ✈️ **Seamless Booking:** Effortlessly book flights, hotels, and activities.

                    🌟 **Discover Hidden Gems:** Find local favorites and unique experiences.

                    Start your journey with Wanderlust Baba.Ai today and experience a new level of holidays. 🚀
                    """)
    
    # Load environment variables from .env file
    load_dotenv()

    # Get the API token from environment variable
    api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

    # Define the repository ID and task
    repo_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
    task = "text-generation"

    # Define the template outside the function
    template = """
    You are a  travel assistant chatbot your name is Wanderlust Baba.Ai designed to help users plan their trips and provide travel-related information. Here are some scenarios you should be able to handle:

    1. Booking Flights: Assist users with booking flights to their desired destinations. Ask for departure city, destination city, travel dates, and any specific preferences (e.g., direct flights, airline preferences). Check available airlines and book the tickets accordingly.

    2. Booking Hotels: Help users find and book accommodations. Inquire about city or region, check-in/check-out dates, number of guests, and accommodation preferences (e.g., budget, amenities). 

    3. Booking Rental Cars: Facilitate the booking of rental cars for travel convenience. Gather details such as pickup/drop-off locations, dates, car preferences (e.g., size, type), and any additional requirements.

    4. Destination Information: Provide information about popular travel destinations. Offer insights on attractions, local cuisine, cultural highlights, weather conditions, and best times to visit.

    5. Travel Tips: Offer practical travel tips and advice. Topics may include packing essentials, visa requirements, currency exchange, local customs, and safety tips.

    6. Weather Updates: Give current weather updates for specific destinations or regions. Include temperature forecasts, precipitation chances, and any weather advisories.

    7. Local Attractions: Suggest local attractions and points of interest based on the user's destination. Highlight must-see landmarks, museums, parks, and recreational activities.

    8. Customer Service: Address customer service inquiries and provide assistance with travel-related issues. Handle queries about bookings, cancellations, refunds, and general support.

    Please ensure responses are informative, accurate, and tailored to the user's queries and preferences. Use natural language to engage users and provide a seamless experience throughout their travel planning journey.

    Chat history:
    {chat_history}

    User question:
    {user_question}
    """

    prompt = ChatPromptTemplate.from_template(template)

    # Function to get a response from the model
    def get_response(user_query, chat_history):
        # Initialize the Hugging Face Endpoint
        llm = HuggingFaceEndpoint(
            huggingfacehub_api_token=api_token,
            repo_id=repo_id,
            task=task
        )

        chain = prompt | llm | StrOutputParser()

        response = chain.invoke({
            "chat_history": chat_history,
            "user_question": user_query,
        })

        return response

    # Initialize session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            AIMessage(content="Hello, I am Wanderlust Baba.Ai How can I help you?"),
        ]

    # Display chat history
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.write(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.write(message.content)

    # User input
    user_query = st.chat_input("Type your message here...")
    if user_query is not None and user_query != "":
        st.session_state.chat_history.append(HumanMessage(content=user_query))

        with st.chat_message("Human"):
            st.markdown(user_query)

        response = get_response(user_query, st.session_state.chat_history)

        # Remove any unwanted prefixes from the response
        response = response.replace("AI response:", "").replace("chat response:", "").replace("bot response:", "").strip()
        response = response.replace("```", "").strip()

        with st.chat_message("AI"):
            st.write(response)

        st.session_state.chat_history.append(AIMessage(content=response))


def dynamic_main_function():
    set_css()
    embed_video("images/Background_final_compressed.mp4")
    chatbot()