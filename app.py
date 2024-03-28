import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# Function to get Groq completions
def get_groq_completions(user_content):
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    completion = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {
                "role": "system",
                "content": "You are a christain Bible scholar or expert who likes to "
                           "write bible verses for every human life challenges. \nYou "
                           "will provide 3 bible verse to every human "
                           "challenges written by the user and give a explanation "
                           "how those bible verse can bring solutions to the human life "
                           "challenges specified by the users."
            },
            {
                "role": "user",
                "content": user_content
            }
        ],
        temperature=0.5,
        max_tokens=9096,
        top_p=1,
        stream=True,
        stop=None,
    )

    result = ""
    for chunk in completion:
        result += chunk.choices[0].delta.content or ""

    return result

# Streamlit interface


def main():
    # Display the Groq logo
    spacer, col = st.columns([8, 3])
    with col:
        st.image('groqcloud_darkmode.png')


    st.title("Bible Assistant using Groq and Mistral")
    user_content = st.text_input("Enter the challenges you are experiencing in your life:")

    if st.button("Generate Titles"):
        if not user_content:
            st.warning("Please enter a keyword before generating titles.")
            return
        st.info("Generating Bible verses... Please wait.")
        generated_bible_verses = get_groq_completions(user_content)
        st.success("Bible verse generated successfully!")

        # Display the generated titles
        st.markdown("### Bible verses:")
        st.text_area("", value=generated_bible_verses, height=700)

if __name__ == "__main__":
    main()