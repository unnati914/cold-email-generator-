import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
import json

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-1.5-flash" 
model = genai.GenerativeModel(MODEL)


def build_prompt(mode, tone, recipient, sender, company, goal, extra):
    return f"""
You are an expert cold-email copywriter. Improve and produce the best possible email given:

- Mode: {mode}
- Tone: {tone}
- Recipient: {recipient}
- Sender: {sender}
- Company: {company}
- Goal: {goal}
- Extra context: {extra}

Requirements:
- Write a concise, high-converting cold email with a clear CTA.
- Start with a compelling subject line.
- Keep the body skimmable (short paragraphs, optional bullets).
- Suggest 3 quick personalization ideas at the end.
- Output as clean Markdown only. Do not include JSON.

Markdown structure:
## Subject
<strong, concise subject>

## Email
<final refined email body>

## Personalization ideas
- <idea 1>
- <idea 2>
- <idea 3>
"""


def generate_email(mode, tone, recipient, sender, company, goal, extra):
    prompt = build_prompt(mode, tone, recipient, sender, company, goal, extra)
    response = model.generate_content(prompt)
    return response.text or ""


# ---------- Streamlit UI ----------
st.set_page_config(page_title="ColdEmailGenie", page_icon="📧", layout="wide")
st.title("📧 ColdEmailGenie")
st.write("Generate smart, personalized cold emails with Gemini.")

with st.sidebar:
    st.header("Email Settings")
    mode = st.selectbox(
        "Mode", ["Investor Pitch", "Partnership", "Sales Outreach", "Job Networking", "General"]
    )
    tone = st.selectbox(
        "Tone", ["Professional", "Friendly", "Witty", "Bold", "Casual"]
    )
    recipient = st.text_input("Recipient (Name or Title)", "")
    sender = st.text_input("Sender (Your Name)", "")
    company = st.text_input("Your Company/Org", "")
    goal = st.text_area("Goal / Pitch", "")
    extra = st.text_area("Extra Context (optional)", "")

if st.button("✨ Generate Email"):
    with st.spinner("Crafting your improved email..."):
        content_md = generate_email(mode, tone, recipient, sender, company, goal, extra)

    if not content_md.strip():
        st.error("⚠️ No content was generated. Please try again.")
    else:
        st.subheader("📬 Your refined draft")
        st.markdown(content_md)

        st.download_button(
            label="⬇️ Download as Markdown",
            data=content_md,
            file_name="cold_email.md",
            mime="text/markdown",
        )

