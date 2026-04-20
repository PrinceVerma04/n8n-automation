import streamlit as st
import requests
import os

st.set_page_config(
    page_title="Personal Assistant",
    page_icon="🤝",
    layout="wide",
)

DEFAULT_WEBHOOK_URL = "http://127.0.0.1:5678/webhook/6a793279-70ee-4c4b-a044-e1f53553ff02"
WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", DEFAULT_WEBHOOK_URL)
REQUEST_TIMEOUT_SECONDS = int(os.getenv("N8N_REQUEST_TIMEOUT", "60"))

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

with st.sidebar:
    st.markdown("### Control Center")
    st.session_state.dark_mode = st.toggle("Dark Mode", value=st.session_state.dark_mode)
    st.markdown('<span class="status-pill">Webhook Connected UI</span>', unsafe_allow_html=True)
    st.caption("Professional assistant experience with real-time chat flow.")
    st.caption(f"Webhook: {WEBHOOK_URL}")
    st.caption(f"Timeout: {REQUEST_TIMEOUT_SECONDS}s")
    st.divider()
    st.markdown("### Session")
    st.metric("Total Messages", len(st.session_state.get("messages", [])))

theme = {
    "page_bg": """
        radial-gradient(circle at 10% 20%, rgba(255, 163, 102, 0.30) 0%, transparent 35%),
        radial-gradient(circle at 90% 10%, rgba(74, 222, 128, 0.28) 0%, transparent 30%),
        radial-gradient(circle at 80% 80%, rgba(56, 189, 248, 0.30) 0%, transparent 30%),
        linear-gradient(145deg, #fdf2f8 0%, #eff6ff 45%, #ecfeff 100%)
    """ if not st.session_state.dark_mode else """
        radial-gradient(circle at 10% 20%, rgba(14, 165, 233, 0.24) 0%, transparent 35%),
        radial-gradient(circle at 90% 10%, rgba(16, 185, 129, 0.20) 0%, transparent 30%),
        radial-gradient(circle at 80% 80%, rgba(99, 102, 241, 0.24) 0%, transparent 30%),
        linear-gradient(145deg, #0b1220 0%, #111827 45%, #101a2d 100%)
    """,
    "text_primary": "#0f172a" if not st.session_state.dark_mode else "#f8fafc",
    "text_secondary": "#334155" if not st.session_state.dark_mode else "#cbd5e1",
    "subheader": "#0f172a" if not st.session_state.dark_mode else "#f1f5f9",
    "chat_user_bg": "rgba(255, 255, 255, 0.90)" if not st.session_state.dark_mode else "rgba(30, 41, 59, 0.88)",
    "chat_assistant_bg": "rgba(255, 255, 255, 0.98)" if not st.session_state.dark_mode else "rgba(15, 23, 42, 0.92)",
    "chat_user_border": "rgba(2, 132, 199, 0.35)" if not st.session_state.dark_mode else "rgba(56, 189, 248, 0.45)",
    "chat_assistant_border": "rgba(79, 70, 229, 0.25)" if not st.session_state.dark_mode else "rgba(129, 140, 248, 0.45)",
    "input_bg": "#f8fafc" if not st.session_state.dark_mode else "#1e293b",
    "input_text": "#0f172a" if not st.session_state.dark_mode else "#f8fafc",
    "input_border": "#7dd3fc" if not st.session_state.dark_mode else "#334155",
}

css_template = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

html, body, [class*="css"]  {
    font-family: 'Poppins', sans-serif;
    color: __TEXT_PRIMARY__;
}

.stApp {
    background: __PAGE_BG__;
}

.stMarkdown p, .stMarkdown li, .stCaption, .stText {
    color: __TEXT_SECONDARY__ !important;
    font-size: 1rem;
}

h1, h2, h3, h4, h5, h6, [data-testid="stMarkdownContainer"] h3 {
    color: __SUBHEADER__ !important;
    font-weight: 700 !important;
}

.hero-card {
    background: linear-gradient(120deg, #0f766e 0%, #0284c7 55%, #4f46e5 100%);
    border-radius: 20px;
    padding: 1.4rem 1.6rem;
    color: #ffffff;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.20);
    margin-bottom: 1rem;
}

.hero-title {
    font-size: 2rem;
    font-weight: 700;
    margin: 0 0 0.2rem 0;
}

.hero-subtitle {
    font-size: 1rem;
    opacity: 0.95;
    margin: 0;
}

.feature-card {
    border-radius: 16px;
    padding: 1.05rem;
    color: #0f172a;
    min-height: 120px;
    box-shadow: 0 10px 20px rgba(15, 23, 42, 0.09);
    border: 1px solid rgba(255, 255, 255, 0.7);
    margin-bottom: 0.6rem;
}

.feature-card h4 {
    margin: 0 0 0.35rem 0;
    font-size: 1.18rem;
    font-weight: 700;
    color: #111827 !important;
}

.feature-card p {
    margin: 0;
    font-size: 1rem;
    color: #1f2937 !important;
    line-height: 1.5;
}

.bg-orange { background: linear-gradient(135deg, #ffedd5 0%, #fed7aa 100%); }
.bg-blue { background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); }
.bg-green { background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%); }
.bg-pink { background: linear-gradient(135deg, #fce7f3 0%, #fbcfe8 100%); }
.bg-cyan { background: linear-gradient(135deg, #cffafe 0%, #a5f3fc 100%); }
.bg-violet { background: linear-gradient(135deg, #ede9fe 0%, #ddd6fe 100%); }

[data-testid="stChatMessage"] {
    border-radius: 14px;
    padding: 0.6rem 0.75rem;
    backdrop-filter: blur(4px);
}

[data-testid="stChatMessage"]:has([aria-label="Chat message from user"]) {
    background: __CHAT_USER_BG__;
    border: 1px solid __CHAT_USER_BORDER__;
}

[data-testid="stChatMessage"]:has([aria-label="Chat message from assistant"]) {
    background: __CHAT_ASSISTANT_BG__;
    border: 1px solid __CHAT_ASSISTANT_BORDER__;
}

[data-testid="stChatMessage"] p {
    color: __TEXT_PRIMARY__ !important;
    font-size: 1.03rem !important;
    line-height: 1.55 !important;
}

[data-testid="stChatInput"] textarea,
[data-testid="stChatInput"] input {
    background: __INPUT_BG__ !important;
    color: __INPUT_TEXT__ !important;
    border: 1px solid __INPUT_BORDER__ !important;
    font-size: 1rem !important;
}

[data-testid="stChatInput"] textarea::placeholder,
[data-testid="stChatInput"] input::placeholder {
    color: __TEXT_SECONDARY__ !important;
    opacity: 1 !important;
}

.status-pill {
    background: linear-gradient(90deg, #14b8a6, #22c55e);
    color: #ffffff;
    font-weight: 600;
    font-size: 0.8rem;
    border-radius: 999px;
    padding: 0.25rem 0.8rem;
    display: inline-block;
    margin-top: 0.25rem;
}
</style>
"""

css = (
    css_template
    .replace("__TEXT_PRIMARY__", theme["text_primary"])
    .replace("__PAGE_BG__", theme["page_bg"])
    .replace("__TEXT_SECONDARY__", theme["text_secondary"])
    .replace("__SUBHEADER__", theme["subheader"])
    .replace("__CHAT_USER_BG__", theme["chat_user_bg"])
    .replace("__CHAT_USER_BORDER__", theme["chat_user_border"])
    .replace("__CHAT_ASSISTANT_BG__", theme["chat_assistant_bg"])
    .replace("__CHAT_ASSISTANT_BORDER__", theme["chat_assistant_border"])
    .replace("__INPUT_BG__", theme["input_bg"])
    .replace("__INPUT_TEXT__", theme["input_text"])
    .replace("__INPUT_BORDER__", theme["input_border"])
)

st.markdown(css, unsafe_allow_html=True)

st.markdown(
    """
    <div class="hero-card">
        <p class="hero-title">🤝 Your Personal Assistant</p>
        <p class="hero-subtitle">Ask, plan, summarize, and execute faster with a smart n8n-powered assistant.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.subheader("What can your personal assistant do?")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        '<div class="feature-card bg-orange"><h4>Knowledge Answers</h4><p>Get concise responses on diverse topics in seconds.</p></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="feature-card bg-blue"><h4>Calendar Planning</h4><p>Prepare schedules, meetings, and reminders with clear structure.</p></div>',
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        '<div class="feature-card bg-green"><h4>Email Intelligence</h4><p>Read, summarize, and craft thoughtful replies efficiently.</p></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="feature-card bg-pink"><h4>Task Management</h4><p>Turn goals into to-do lists and next-action priorities.</p></div>',
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        '<div class="feature-card bg-cyan"><h4>Quick Notes</h4><p>Capture ideas and decisions for easy follow-up and recall.</p></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="feature-card bg-violet"><h4>Expense Tracking</h4><p>Organize spending insights and budgeting updates instantly.</p></div>',
        unsafe_allow_html=True,
    )

st.subheader("💬 Chat with your assistant")

# create a session state for message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# show the messages in chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# create a chat input box
user_message = st.chat_input()

def extract_ai_response(payload):
    """Support both n8n response styles: list[{"output": "..."}] or {"output": "..."}."""
    if isinstance(payload, list):
        if not payload:
            return None
        first_item = payload[0]
        if isinstance(first_item, dict):
            return first_item.get("output")

    if isinstance(payload, dict):
        return payload.get("output")

    return None


# if user sends a message
if user_message:
    with st.chat_message("user"):
        st.markdown(user_message)
        # append the user message to message history
        st.session_state.messages.append({"role": "user", "content": user_message})
    
    try:
        # send the user message to the n8n webhook
        response = requests.post(
            WEBHOOK_URL,
            json={"message": user_message},
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        payload = response.json()
        ai_response = extract_ai_response(payload)

        if not ai_response:
            st.error(f"Webhook returned unexpected JSON format: {payload}")
        else:
            # display the AI response in chat
            with st.chat_message("assistant"):
                st.markdown(ai_response)
                # append the AI response to message history
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
    except requests.exceptions.ConnectionError:
        st.error(
            "Could not connect to n8n webhook. "
            "Make sure n8n is running and N8N_WEBHOOK_URL points to a reachable host/port."
        )
    except requests.exceptions.ReadTimeout:
        st.error(
            f"Webhook timed out after {REQUEST_TIMEOUT_SECONDS}s. "
            "Your n8n workflow is taking longer than the client timeout."
        )
    except requests.RequestException as e:
        st.error(f"Failed to call webhook: {e}")
    except ValueError:
        st.error(f"Webhook did not return valid JSON. Raw response: {response.text}")
