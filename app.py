import streamlit as st
from src.helper import get_pdf_text, get_text_chunks, get_conversational_chain, get_vector_store

def user_input(user_question):
    # Check if a conversation chain exists and use it for the query
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chatHistory = response['chatHistory']

    # Display the chat history
    for i, message in enumerate(st.session_state.chatHistory):
        if i % 2 == 0:
            st.write(f"User: {message.content}")
        else:
            st.write(f"Reply: {message.content}")


def main():
    # Set up the page
    st.set_page_config(page_title='Information Retrieval', layout='wide')
    st.header('Information-Retrieval-Sys')

    # Get the user's question
    user_question = st.text_input("Ask a Question from the PDF Files")

    # Initialize session state variables if not already done
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chatHistory" not in st.session_state:
        st.session_state.chatHistory = []

    # If user has entered a question, call user_input function
    if user_question:
        user_input(user_question)

    # Sidebar for PDF upload
    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Upload your PDF File and click the submit & Process Button", accept_multiple_files=True)
        if st.button("Submit & Process"):
            if pdf_docs:
                with st.spinner("Processing..."):
                    # Get the raw text from the uploaded PDFs
                    raw_text = get_pdf_text(pdf_docs)

                    # Split the text into chunks
                    text_chunks = get_text_chunks(raw_text)

                    # Create vector store
                    vector_store = get_vector_store(text_chunks)

                    # Set up the conversational chain
                    st.session_state.conversation = get_conversational_chain(vector_store)

                    st.success("Processing complete!")
            else:
                st.warning("Please upload PDF files to proceed.")

if __name__ == "__main__":
    main()
