import streamlit as st
from aiagent import AIAgent

from streamlit.web.server.websocket_headers import _get_websocket_headers
import streamlit as st

headers = _get_websocket_headers()

session_id = headers.get("Sec-Websocket-Key")

@st.cache_resource
def get_agent(session_id):
    agent = AIAgent(model='gpt-3.5-turbo')
    print('creating the ai agent')
    agent.reponse = 'Philosophers are waiting patiently, possibly smoking a cigar or pipe'
    return agent

def format_history(history):
    report = ''
    for message in history[1:]:
        if message['role'] == 'user':
            report += (f"\n\nYOU: {message['content'].replace(agent.prefix, '')}")
        else:
            report += (f"\n\nPHILOSOPHER: {message['content']}")
    return report
 
def query_agent():
    if prompt:
        try:      
            current_response.write("The forum is considering your query and will send a representative soon.")
            agent.query(prompt, 
                        temperature=temperature
                                )
            # print("agent response is: ", response)
        except Exception as e:
            agent.response = "I'm sorry, all philosophers are busy helping other wisdom seekers.  Please try again later."
            print(e)
    else:
        print('no prompt')

st.title('Chat with a Philosopher!')

prompt = st.text_input(label="Please ask your question and the next available philosopher will answer",
                       max_chars=1000,
                       value='',
                       help="If your philosopher is currently life-impaired, they will be temporarily resurrected for this conversation",
                       key='user_query',
                       placeholder="Enter your burning question here")

agent = get_agent(session_id)

st.button('Submit your question to the Forum of Wisdom',
          on_click=query_agent
          )

temperature = st.sidebar.slider('Creativity', min_value=0.0, max_value=1.0, step=0.1, value=0.1)

st.sidebar.button('New conversation', on_click=agent.clear_history,
                   use_container_width=False)

st.sidebar.markdown(f'The conversation so far: {format_history(agent.history)}')

current_response = st.markdown(agent.response)