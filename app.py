import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import streamlit as st
from fastapi import FastAPI

app = FastAPI()  # <--- Vercel looks for this exact name "app"

@app.get("/")
def home():
    return {"status": "ok"}
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

#page setup file
#the tabs title and the page icon
st.set_page_config(
    page_title="Farmer Assistant",
    page_icon =":seedling:"
)


st.title("Farmer Assistant")
st.subheader("I am a farmer assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Render previous conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_message = st.chat_input("Ask your question")


if user_message:
    st.session_state.messages.append({"role": "user", "content": user_message})
    with st.chat_message("user"):
        st.markdown(user_message)


    contents = [
        types.Content(
            role="model" if m["role"] == "assistant" else "user",
            parts=[types.Part.from_text(text=m["content"])]
        )
        for m in st.session_state.messages
    ]


    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=(
                        "You are a helpful agriculture assistant. "
                        "Answer farmers in simple, easy-to-understand language. "
                        "If the user asks a question unrelated to agriculture, "
                        "you can still answer briefly."
                    )
                )
            )
            answer = response.text
            st.markdown(answer)


    st.session_state.messages.append({"role": "assistant", "content": answer})
