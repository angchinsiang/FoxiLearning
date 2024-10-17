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
    
    