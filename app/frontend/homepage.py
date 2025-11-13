import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from app.utils.state import SupervisorState
from app.backend.utils.replier import answer
from app.backend.utils.error_handling import safe_fallback
import time

st.title("💬 InvestiSense AI")
role_map = {
    "📊 Pro Analyst": "analyst",
    "💼 Executive View": "executive",
    "👤 Everyday Investor": "investor"
}
if 'role' not in st.session_state:
    st.session_state.role = "analyst"
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

selected_label = st.radio(
"Select your role:",
    ["📊 Pro Analyst", "💼 Executive View", "👤 Everyday Investor"],
    index = list(role_map.values()).index(st.session_state.role),
    horizontal = True
)
selected_role = role_map[selected_label]
if selected_role == st.session_state.role:
    st.session_state.role = selected_role
    st.session_state.role_changed = True
else:
    st.session_state.role_changed = False

user_query = st.chat_input('Ask anything finance...')
if user_query and len(str(user_query).strip()) != 0:
    st.session_state.chat_history.append({"User": "You", "Message": user_query})
    length_of_history = len(st.session_state.chat_history)
    state = SupervisorState(query =  user_query, role = st.session_state.role, memory = st.session_state.chat_history[:10 if length_of_history > 10 else length_of_history])
    # response = requests.post( 'http://127.0.0.1:8000/chat', json=payload)
    # result = json.loads(response.content.decode('utf-8'))
    result = safe_fallback(answer,state = state)
    print(result)
    st.session_state.chat_history.append({"User": "Assistant", "Message": result['response']})

for chat in st.session_state.chat_history:
    if chat['User'] == 'You':
        with st.chat_message(name = 'user',width = 'stretch'):
            st.write(chat['Message'])
    else:
        with st.chat_message(name = 'ai',width = 'stretch'):
            st.write(chat['Message'])
