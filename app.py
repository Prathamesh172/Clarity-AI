import streamlit as st
from llm_router import route_message
from emergency import check_for_emergency, make_emergency_call

st.set_page_config(page_title="Clarity AI Therapist", page_icon="🧠", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    body {
        background-color: #0d1117;
        color: #f0f6fc;
    }
    .chat-container {
        max-width: 800px;
        margin: auto;
    }
    .chat-message {
        padding: 12px 18px;
        border-radius: 16px;
        margin-bottom: 12px;
        max-width: 75%;
        font-size: 16px;
        line-height: 1.5;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        animation: fadeIn 0.4s ease-in-out;
        word-break: break-word;
    }
    .chat-message a {
        color: #00ff99; 
        text-decoration: underline;
    }
    .chat-message a:hover {
        color: #81D4FA;
    }
    .user-message {
        background: linear-gradient(135deg, #ff9966, #ff5e62);
        color: white;
        align-self: flex-end;
        border-bottom-right-radius: 4px;
    }
    .ai-message {
        background: linear-gradient(135deg, #00c6ff, #0072ff);
        color: white;
        align-self: flex-start;
        border-bottom-left-radius: 4px;
        box-shadow: 0 0 12px rgba(0, 198, 255, 0.5);
    }
    .chat-bubble-wrapper {
        display: flex;
        flex-direction: column;
    }
    .chat-bubble-row {
        display: flex;
        width: 100%;
    }
    .chat-bubble-row.user { justify-content: flex-end; }
    .chat-bubble-row.ai { justify-content: flex-start; }
    @keyframes fadeIn {
        from {opacity: 0; transform: translateY(5px);}
        to {opacity: 1; transform: translateY(0);}
    }
    </style>
""", unsafe_allow_html=True)

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pending_emergency_call" not in st.session_state:
    st.session_state.pending_emergency_call = False
if "waiting_for_phone" not in st.session_state:
    st.session_state.waiting_for_phone = False
if "user_phone" not in st.session_state:
    st.session_state.user_phone = None

st.markdown("<h1 style='text-align: center;'>🧠 Clarity AI - Your Personal AI Therapist</h1>", unsafe_allow_html=True)

# User input
user_input = st.chat_input("How are you feeling today?")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # 1. If waiting for phone number
    if st.session_state.waiting_for_phone:
        st.session_state.user_phone = user_input.strip()
        result = make_emergency_call(st.session_state.user_phone)
        st.session_state.chat_history.append({"role": "assistant", "content": result})
        st.session_state.waiting_for_phone = False
        st.session_state.pending_emergency_call = False

    # 2. If waiting for consent
    elif st.session_state.pending_emergency_call:
        if user_input.strip().lower() in ["yes", "y", "yeah", "yep", "sure"]:
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": "Please provide your phone number so I can connect you to the helpline."
            })
            st.session_state.waiting_for_phone = True
        else:
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": "Okay, I won’t call. I’m still here to listen and help."
            })
        st.session_state.pending_emergency_call = False

    # 3. Detect emergencies
    elif check_for_emergency(user_input):
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": "**I'm really concerned about your safety.**\n\nWould you like me to connect you directly to the suicide prevention helpline?"
        })
        st.session_state.pending_emergency_call = True

    # 4. Normal AI response
    else:
        response = route_message(user_input, st.session_state.chat_history)
        st.session_state.chat_history.append({"role": "assistant", "content": response})

# Display chat
st.markdown("<div class='chat-container chat-bubble-wrapper'>", unsafe_allow_html=True)
for message in st.session_state.chat_history:
    role_class = "user" if message["role"] == "user" else "ai"
    msg_class = "user-message" if role_class == "user" else "ai-message"
    st.markdown(f"""
        <div class='chat-bubble-row {role_class}'>
            <div class='chat-message {msg_class}'>{message["content"]}</div>
        </div>
    """, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
