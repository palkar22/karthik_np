import streamlit as st
import replicate
import os

# Set page configuration and title
st.set_page_config(page_title="🦙💬 Intel Product Sentimental Analyser")

# Function to clear chat history
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Enter review which has to be sentimentally analysed"}]

# Function for generating LLaMA2 response
def generate_llama2_response(prompt_input):
    string_dialogue = "You are a Sentimental analyser. You do not respond as 'User' or pretend to be 'User'. You will analyse the review which is given as input and respond whether it is positive negative or neutral in first line only.no other words are permitted in first line.First line syntax Sentiment : {Positive/negative/neutral}.in the second line write the reason why in not more than 20 words"
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
    output = replicate.run('a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5', 
                           input={"prompt": f"{string_dialogue} {prompt_input} Assistant: ",
                                  "temperature": temperature, "top_p": top_p, "max_length": max_length, "repetition_penalty": 1})
    return output

# Initialize or clear chat history
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Enter review which has to be sentimentally analysed"}]

# Sidebar with Replicate API credentials
with st.sidebar:
    st.title('🦙💬 Intel Product Sentimental Analyser')
    st.title("Click on 'Click here to go to chat page' to access chatbot                     ")

    st.write('Intel Unnati Industrial training 2024')
    st.write('Name : N Palani Karthik')
    st.write('email : palanikarthik.n2022@vitstudent.ac.in')



    replicate_api = "st.secrets.get('REPLICATE_API_TOKEN', '')"
    if replicate_api:
        st.success('API key already provided!', icon='✅')
    else:
        replicate_api = st.text_input('Enter Replicate API token:', type='password')
        if not (replicate_api.startswith('r8_') and len(replicate_api) == 40):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')
    os.environ['REPLICATE_API_TOKEN'] = replicate_api

    st.subheader('Models and parameters')
    selected_model = st.selectbox('Choose a Llama2 model', ['Llama2-7B', 'Llama2-13B'], key='selected_model')
    if selected_model == 'Llama2-7B':
        llm = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'
    elif selected_model == 'Llama2-13B':
        llm = 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5'
    
    temperature = 0.7
    top_p = 0.9
    max_length = 32
    st.write("\n Dataset used is Conclusions.xlsx (provided in github)")
    st.button('Clear Chat History', on_click=clear_chat_history)
    
# Custom CSS style for fixed-position buttons
st.markdown(
    """
    <style>
    .fixed-buttons {
        position: fixed;
        top: 20px;
        right: 20px;
        display: flex;
        flex-direction: row;
        gap: 10px;
    }
    .fixed-buttons a {
        background-color: black;
        color: white;
        padding: 10px 20px;
        border: none;
        cursor: pointer;
        font-size: 16px;
        text-decoration: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Fixed-position buttons for navigation
st.markdown('<div class="fixed-buttons">', unsafe_allow_html=True)
if st.button("Click here to go to Main Page", key='main_page'):
    st.session_state.chat_mode = False  # Ensure chat mode is set to False
    st.rerun()

if st.button("Click here to go to Chat Page", key='chat_page'):
    st.session_state.chat_mode = True
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
# Example content for the main page
if not st.session_state.get("chat_mode", False):

    # Main page content
    st.title("Intel Product Sentimental Analysis")
    st.markdown("<div style='text-align: right; font-size: 20px;'>By N Palani Karthik</div>", unsafe_allow_html=True)
    st.markdown("### Overall Sentiment Distribution ")
    st.image("download.png", use_column_width=True) 
    st.markdown("### Review Sources Distribution ")
    st.image("10.png", use_column_width=True) 
    st.markdown("### Sentiment Distribution for each site")
    st.image("9.png", use_column_width=True)
    st.markdown("### Sentiment Distribution for each product")
    st.image("big.png", use_column_width=True)
    st.markdown("### Sentiment Distribution for each Generation (bar)")
    st.image("2.png", use_column_width=True)
    st.markdown("### Sentiment Distribution for each Generation (pie)")
    st.image("3.png", use_column_width=True)

    st.markdown("### Conclusions \n")
    st.markdown("""
                (i)Majority of the user based reviews are positive (84.1%)\n
                (ii)The percentage of positive comments have increased as the genaration have also increased\n
                (iii)The Postive and neutral comments are majorly present across all e-commerce websites """)
else:
    # Chatbot interface page
    st.write('Chatbot Interface')

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User-provided prompt
    if prompt := st.chat_input(disabled=not replicate_api):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                response = generate_llama2_response(prompt)
                placeholder = st.empty()
                full_response = ''
                for item in response:
                    full_response += item
                    placeholder.markdown(full_response)
                placeholder.markdown(full_response)
        message = {"role": "assistant", "content": full_response}
        st.session_state.messages.append(message)
