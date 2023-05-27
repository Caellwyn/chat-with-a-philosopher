import streamlit as st
from aiagent import AIAgent

@st.cache_resource
def get_agent():
    agent = AIAgent(model='gpt-3.5-turbo-0301')
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
        
    
agent, cost = get_agent()

st.title('Chat with a Philosopher!')

st.sidebar.button('Press to start new conversation', on_click=agent.clear_history)

prompt = st.text_input(label="Please ask your question and the next available philosopher will answer",
                       max_chars=1000,
                       help="If your philosopher is currently life-impaired, they will be temporarily resurrected for this conversation",
                      key='user_query')

current_response = st.text('Philosophers are waiting patiently, possibly smoking a cigar or pipe')

if prompt:
    try:
        reply = agent.query(prompt)
        cost += reply['cost']
        content = reply['content']
        current_response.write(content)
        total_cost = st.text(f'The total cost of this conversation is: ${cost}')
                
        st.write(format_history(agent.history))
    except:
        current_response.write("I'm sorry, all philosophers are busy helping other wisdom seekers.  Please try again later.")
