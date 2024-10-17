import streamlit as st
import os
from openai import OpenAI
import json
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from youtube_transcript_api import YouTubeTranscriptApi
import webbrowser
import requests
#only to wrap the colab output
#from IPython.display import HTML, display
import random

client = OpenAI(api_key=st.secrets['OpenAI_API_KEY'])
choice=''

def Quiz():
  response = client.chat.completions.create(
      model='gpt-4o',
      messages=[{
          "role":
          "system",
          "content":
          "You are a quiz genetator that generate proper, suitable quiz questions based on input subject given. The format of question is in 'multiple choice format e.g. a), b), c), d)'. You will breakdown and solve the question on your own knowledge, and provide the answer in a JSON format. Do not mention 'JSON' in your response"
      }, {
          "role": "user",
          "content": "primary school math multiplication"
      }, {
          "role":
          "assistant",
          "content":
          """{{
    "question": "What is the product of 6 multiplied by 8?",
    "options": {
      "a": 14,
      "b": 48,
      "c": 54,
      "d": 62
    },
    "answer": 48
  }
  """
      }, {
          "role": "user",
          "content": "primary school math multiplication"
      }],
      max_tokens=1000,
      temperature=1.2)
  st.write(response.choices[0].message.content)
  if isinstance(response.choices[0].message.content, dict):
    st.write("This is a valid Python dictionary.")
  return response.choices[0].message.content

 


def Layout(response):
  st.write("Select your best answer:")

  choice = st.radio(f"{response[0]}", [
      f"{response[1][0]}", f"{response[1][1]}", f"{response[1][2]}",
      f"{response[1][3]}"
  ])


# store = json.loads(response.choices[0].message.content)
# print("\n", store['question'])

# Col init
col1, col2 = st.columns([2, 1])

with col1:
  with st.form(key="FoxiLearn"):
    st.markdown("##  Enter your topic below:")

    Layout(Quiz())
    submit = st.form_submit_button(label="Check", type="primary")

    # topic = st.text_input("Topic")
    # st.markdown("## 📝 Enter the video link below:")
    # videoUrl = st.text_input("Video Link")
    # submit = st.form_submit_button(label="Check", type="primary")

with col2.container(height=400):
  # Create a scrollable container
  with st.chat_message("user"):
    if submit:
      with st.spinner(f"Checking video at {videoUrl}"):
        time.sleep(3)
      st.write(
          f"Assistant: {check_transcript(topic, extract_video_id(videoUrl))}")

css = '''
<style>
section.main > div:has(~ footer ) {
  padding-bottom: 5px;
}
</style>
'''
st.markdown(css, unsafe_allow_html=True)
