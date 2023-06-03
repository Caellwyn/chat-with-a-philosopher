from copyreg import clear_extension_cache
import streamlit as st
from aiagent import AIAgent

@st.cache_resource
def get_agent():
    agent = AIAgent(model='gpt-3.5-turbo-0301')
    global cost
    cost = 0
    print('creating the ai agent')
    return agent, cost

def format_history(history):
    report = []
    for message in history[1:]:
        if message['role'] == 'user':
            report.append(f"YOU: {message['content']}")
        else:
            report.append(f"PHILOSOPHER: {message['content']}")
    return report
        
def clear_history():
    agent.clear_history()
    new_philosopher()

def new_philosopher():
    del st.session_state['prefix']

def query_agent():
    if prompt:
        try:
            current_response.write("The forum is considering your query and will send a representative soon.")
            reply = agent.query(prompt)
            st.session_state['response'] = reply['content']
            st.session_state['prefix'] = "Please continue to respond as the previous philosopher"
        except Exception as e:
            st.session_state['response'] = "I'm sorry, all philosophers are busy helping other wisdom seekers.  Please try again later."
            print(e)
    else:
        print('no prompt')

agent, cost = get_agent()

st.title('Chat with a Philosopher!')

st.sidebar.button('New conversation', on_click=clear_history,
                   use_container_width=False)

st.sidebar.markdown(f'The conversation so far: {format_history(agent.history)}')

prompt = st.text_input(label="Please ask your question and the next available philosopher will answer",
                       max_chars=1000,
                       value='',
                       help="If your philosopher is currently life-impaired, they will be temporarily resurrected for this conversation",
                       key='user_query',
                       placeholder="Enter your burning question here")

if 'prefix' in st.session_state:
    prompt = st.session_state.prefix + prompt

st.button('Submit your question to the Forum of Wisdom',
          on_click=query_agent)

if 'response' not in st.session_state:
    st.session_state["response"] = 'Philosophers are waiting patiently, possibly smoking a cigar or pipe'

current_response = st.markdown(st.session_state.response)