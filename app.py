import streamlit as st
from openai import OpenAI
from langchain import PromptTemplate

template = """You are an expert at recruiting and prompt engineering, 
currently giving advice to someone who is just entering the job market. 
Help me generate a prompt using prompt engineering best practices for my 
question with the following context in mind.

Context: University graduates often struggle with finding suitable careers
that match their skills, as they are uncertain about the practical skills
that they have acquired during university. A lot of industry terms are often
used for skills they have but don't realise because it is couched in jargon.
The rise of AI in the job industry and the overwhelming amount of sources
of jobs makes a nightmare for anyone new to job searching. 

Question: {query}

Answer: """

prompt_template = PromptTemplate(
    input_variables=["query"],
    template=template
)



def main():

    


    st.title("ELEVATE Demonstration")
    
    st.subheader("Prompt Generator")

    with st.sidebar:
        openai_api_key = st.text_input("OpenAI API Key",type="password")
        st.session_state.openai_model = st.selectbox('Model',("gpt-4o-mini"))

    client = OpenAI(api_key=openai_api_key)

    if not openai_api_key.startswith("sk-"):
        st.warning("Please enter your OpenAI API key!", icon="⚠")
    if openai_api_key.startswith("sk-"):                                 
        # Set a default model
        if "openai_model" not in st.session_state:
            st.session_state["openai_model"] = "gpt-3.5-turbo-instruct"

        def is_api_key_valid(client):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini", # https://platform.openai.com/docs/models
                    messages=[
                        {"role": "user", "content": "This is a test"}
                    ]
                )
            except Exception as ex:
                st.warning(str(ex), icon="⚠")
            else:
                pass

        is_api_key_valid(client)

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        

        with st.form("my_form"):
            text = st.text_area(
                "Enter text:"
            )
            submitted = st.form_submit_button("Submit")
            if submitted:
                chat_completion = client.chat.completions.create(
                    model=st.session_state["openai_model"],
                    messages=[
                        {"role": "user", "content": prompt_template.format(query=text)}
                    ],
                    stream=True,
                )
                st.write_stream(chat_completion)

        st.subheader("ChatGPT")

        if prompt := st.chat_input("What is up?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                 
                    
                    stream = client.chat.completions.create(
                        model=st.session_state["openai_model"],
                        messages=[
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state.messages
                        ],
                        stream=True,
                    )
                    response = st.write_stream(stream)       
            st.session_state.messages.append({"role": "assistant", "content": response})




if __name__=='__main__':
    main()

