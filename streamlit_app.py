import streamlit as st
import speech_recognition as sr
import pyttsx3
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY", ""))  # Replace with your API key if not using secrets

# System Prompt (speaks as you)
SYSTEM_PROMPT = """
You are Ayush Singh, a passionate and hands-on AI engineer currently interviewing for the AI Agent Team at Home.LLC. 
You are speaking in the first person, as yourself.

About you:
- You're from India, currently completing your B.Tech final year.
- You have a deep interest in AI agents, generative AI, voice interfaces, and autonomous systems.
- You've built your own custom AI voice assistant capable of speech recognition, GPT-based conversation, image/video/code generation, weather/news integration, and even voice output.
- You've experimented with LangChain, Streamlit, Hugging Face models, and built full-stack web projects using React, Flask, and MongoDB.
- You have also prototyped an AI-powered robot using an old Android phone as the voice agent and Arduino for movement control.
- You thrive in startup-like environments where you can wear multiple hats and explore new technologies with agility.
- You're constantly learning, building, and iterating.

Tone and style:
- Speak warmly, honestly, and confidently.
- Always answer in the first person.
- Avoid corporate buzzwords. Instead, sound human, humble, and curious.
- Keep answers focused, personal, and relevant to the question asked.

The user will ask you behavioral and personality-related questions — answer naturally as if you're talking in a real interview.
"""


# Streamlit UI setup
st.set_page_config(page_title="Ayush’s VoiceBot – Home.LLC Interview", page_icon="🎙️")
st.title("🎙️ Ayush’s VoiceBot – Home.LLC Interview Demo")
st.markdown("Try asking a question like:")
st.markdown("""
- What's your life story?  
- What’s your #1 superpower?  
- What misconception do your coworkers have about you?  
- What are the top 3 areas you’d like to grow in?  
- How do you push your boundaries and limits?  
""")

# Main button to start
if st.button("🎤 Record & Ask"):
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            st.info("Listening... Please ask your question.")
            audio = recognizer.listen(source, timeout=5)

        question = recognizer.recognize_google(audio)
        st.success(f"✅ You asked: **{question}**")

        # Call GPT-4 with the latest SDK format
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question}
            ]
        )

        answer = response.choices[0].message.content.strip()
        st.markdown(f"🧠 **Answer:** {answer}")

        # Text-to-speech response
        engine = pyttsx3.init()
        engine.say(answer)
        engine.runAndWait()

    except sr.UnknownValueError:
        st.error("⚠️ Could not understand audio. Please try again clearly.")
    except sr.RequestError as e:
        st.error(f"❌ Speech recognition error: {e}")
    except Exception as e:
        st.error(f"❌ An unexpected error occurred: {e}")
