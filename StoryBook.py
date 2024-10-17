import os
from openai import OpenAI
#from google.colab import userdata
#rom IPython.display import Image
import streamlit as st

client = OpenAI(api_key=st.secrets['OpenAI_API_KEY'])


def story_gen(prompt):
    system_prompt = """
  You are a world renowned author for young adults fiction short stories.
  Given a concept, generate a short story relevant to the themes of the concept with a twist ending.
  Total length of story is kept in 100 words.
  """

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{
            'role': 'system',
            'content': system_prompt
        }, {
            'role': 'user',
            'content': prompt
        }],
        temperature=1.2,
        max_tokens=1000,
    )

    return response.choices[0].message.content


def art_gen(prompt):
    response = client.images.generate(
        model='dall-e-3',
        prompt=prompt,
        size='1024x1024',
        n=1,
    )

    return response.data[0].url


    #Cover prompt design
def design_gen(prompt):
    system_prompt = """
      You will be given a short story. Generate a prompt for a cover art that is suitable for the story. The prompt is for dall-e-3.

      """
    response = client.chat.completions.create(model='gpt-4o-mini', messages=[{
     "role":
                             "system",
                      "content":
                                                  system_prompt
                                              }, {
                                                  "role": "user",
                                                  "content": prompt
                                              }],
                                              temperature=1.2,
                                              max_tokens=2000)
    return response.choices[0].message.content


prompt = st.text_input("Enter a prompt")
if st.button("Generate"):
    story = story_gen(prompt)
    design = design_gen(story)
    art = art_gen(design)
    original = art_gen(story)

    st.caption(design)    
    st.divider()
    st.write(story)
    st.divider()
    st.image(art)
    st.divider()
    st.image(original)

#testing
    
    import time
    import streamlit as st
    from youtube_transcript_api import YouTubeTranscriptApi
    from openai import OpenAI
    import os

    st.set_page_config(page_title="FoxiLearn|Login", page_icon="🤖", layout="wide")

    client = OpenAI(api_key=os.environ['OPEN_API_KEY'])


    # Function init()
    ## To extract video ID from the video link
    def extract_video_id(url):
        # Find the index of 'v=' in the URL and get the substring after it
        if "v=" in url:
            start = url.index(
                "v=") + 2  # Start of the video ID (2 characters after 'v=')
            return url[start:start + 11]  # Video IDs are 11 characters long
        else:
            return None


    def check_transcript(topic, inputVideoID):
        inputTranscript = YouTubeTranscriptApi.get_transcript(inputVideoID)
        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[{
                'role':
                'assistant',
                'content':
                f"""You will help the user to check whether the input fit the topic of ONLY {topic}. Please mention at which timeline in the video in the form of hours:minutes:seconds it is related and how it is related in the format of line by line. Otherwise if it is not related, output 'This video is unrelated to the topic'"""
            }, {
                'role': 'user',
                'content': f'{inputTranscript}'
            }],
        )
        return response.choices[0].message.content


    st.title("FoxiLearn|Your Learning Assistant App")

    # Col init
    col1, col2 = st.columns([2, 1])

    with col1:
        with st.form(key="FoxiLearn"):
            st.markdown("##  Enter your topic below:")
            topic = st.text_input("Topic")
            st.markdown("## 📝 Enter the video link below:")
            videoUrl = st.text_input("Video Link")
            submit = st.form_submit_button(label="Check", type="primary")

    with col2.container(height=400):
        # Create a scrollable container
        with st.chat_message("user"):
            if submit:
                with st.spinner(f"Checking video at {videoUrl}"):
                    time.sleep(3)
                st.write(
                    f"Assistant: {check_transcript(topic, extract_video_id(videoUrl))}"
                )

    css = '''
    <style>
    section.main > div:has(~ footer ) {
        padding-bottom: 5px;
    }
    </style>
    '''
    st.markdown(css, unsafe_allow_html=True)