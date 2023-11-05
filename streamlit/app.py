import streamlit as st
import openai
from prompt_prep import prepare_prompt
import db
import markdown
import os
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import os
import streamlit_components
from redshift_query import query_top_installs

def ask_question(question):
    try:
        prompt = prepare_prompt(question)
        response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo-16k',
        messages = [{"role":"user", "content": prompt}],
        max_tokens = 1300
        )
        # Extract the text from the OpenAI response
        # Convert markdown-style links to HTML hyperlinks
        
        md_answer = response.choices[0].message.content if response.choices else "No response received."        
        html_answer = markdown.markdown(md_answer)
        output = {"md": md_answer, "html":html_answer}
        return output
    except Exception as e:
        st.error("An error occurred: {}".format(e))
        return None

# Function to create horizontal buttons
import streamlit as st


    

openai.api_key = os.environ.get('OPENAI_API_KEY')
conn = db.create_connection()
db.create_table(conn)

# Streamlit page configuration
st.set_page_config(page_title='Tulip Library App Finder', layout='centered')
# Define your password
correct_password = os.environ.get('LIB_SEARCH_PASSWORD')

# Ask for the password
password = st.text_input("Enter the password", type='password')

# Check the password
if password == correct_password:
    st.success('Password Correct!')

    # Initialize session state
    if 'last_question' not in st.session_state:
        st.session_state['last_question'] = None
    if 'answer' not in st.session_state:
        st.session_state['answer'] = None


    # Generate the navbar with buttons
    cols = st.columns(6)
    with cols[0]:
        if st.button('Search'):
            st.session_state['page'] = 'Search'
    with cols[1]:
        if st.button('Top Installs'):
            st.session_state['page'] = 'Top Installs'


    # Set default page if not selected
    if 'page' not in st.session_state:
        st.session_state['page'] = 'Search'

    # Render page based on navigation selection
    if st.session_state['page'] == 'Search':

        st.title('Tulip Library App Finder')

        # Initialize session state if not already present
        if 'last_question' not in st.session_state:
            st.session_state['last_question'] = None
        if 'answer' not in st.session_state:
            st.session_state['answer'] = None

        # Function to handle changes in the question input
        def on_question_change():
            user_question = st.session_state.user_question
            if user_question and user_question != st.session_state.get('last_question', ''):
                st.session_state['last_question'] = user_question
                query_id = db.insert_query(conn, user_question)
                st.session_state['answer'] = ask_question(user_question)
                st.session_state['query_id'] = query_id

        # Use the first column for the text input
        user_question = st.text_input('What Tulip apps are you looking for?',
                                        key='user_question',
                                        on_change=on_question_change)

        if not('answer' in st.session_state and st.session_state['answer']):
            st.write("Try asking about performance visibility or andon apps!")
        col1, col2 = st.columns([3, 1])
        # Use the second column for the feedback buttons
        with col1:
            if ('answer' in st.session_state and st.session_state['answer']):
                st.markdown(st.session_state['answer']['md'])
        with col2:
            if 'answer' in st.session_state and st.session_state['answer']:
                st.markdown('How do you feel about the results?')  # Title for the feedback buttons
                # Replace the horizontal_radio with your implementation of horizontal buttons
                # Assuming streamlit_components.horizontal_radio is already defined elsewhere
                selected_feedback = streamlit_components.vertical_radio(
                    options=['🙂 Happy', '😐 Neutral', '🙁 Sad'],
                    key='feedback'
                )
                if selected_feedback:
                    feedback_text = selected_feedback[2:]
                    db.update_feedback(conn=conn, feedback=feedback_text, query_id=st.session_state['query_id'])

    elif st.session_state['page'] == 'Top Installs':
        st.title('Top Installed Content')

        top_installs = query_top_installs()

        # Convert URLs to clickable links
        def make_clickable(link, name):
            # Return the hyperlink HTML tag with the URL
            return f'<a href="{link}" target="_blank">{name}</a>'

        # Apply the function to the 'link' column
        top_installs['link'] = top_installs.apply(lambda row: make_clickable(row['link'], row['name']), axis=1)
        top_installs = top_installs[['link','content type', 'summary']]

        top_installs = top_installs.rename(columns={
            'link': 'name'
        })

        # Convert the entire DataFrame to an HTML table with links
        df_html = top_installs.to_html(escape=False, index=True)

        # Use Streamlit's markdown to display the DataFrame as HTML
        st.markdown(df_html, unsafe_allow_html=True)


else:
    st.error('Password incorrect. Try again.')

