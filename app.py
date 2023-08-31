import streamlit as st
from streamlit_chat import message

def _submit():
    st.session_state['question'] = st.session_state.input_field
    st.session_state.input_field = ''

def app():
    # Build Streamlit App
    st.image("twoday kapacity logo.png")
    st.title("Kapacity LLM Hackathon")

    st.write("This is group X's submission for the LLM Hackathon.")

    if 'question' not in st.session_state:
        st.session_state['question'] = ''

    placeholder = st.empty()

    if 'conversation' not in st.session_state:
        st.session_state['conversation'] = [{"message": "Hi! How may I help you today?", "is_user": False}]
        with placeholder.container():
            message(st.session_state['conversation'][0]["message"], is_user=False, key="start")

    st.text_input("you:", key="input_field", on_change=_submit)

    count = 0
    if st.session_state['question']:
        with placeholder.container():
            for message_ in st.session_state['conversation']:
                message(message_["message"], is_user=message_["is_user"], key=count)
                count += 1

        with st.spinner(f"Generate answer for question: {st.session_state['question']}"):
            # This is where your locig goes
            answer = "Det er ikke godt at vide."
        
        # Save new question and answer in the session state
        st.session_state['conversation'].append({"message": st.session_state['question'], "is_user": True})
        st.session_state['conversation'].append({"message": answer, "is_user": False})

        # Show new question and answer
        with placeholder.container():
            for message_ in st.session_state['conversation']:
                message(message_["message"], is_user=message_["is_user"], key=count)
                count += 1

        # Reset question state
        st.session_state['question'] = ''

if __name__ == "__main__":
    app()