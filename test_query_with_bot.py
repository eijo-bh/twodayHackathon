from annoy import AnnoyIndex
import openai
import numpy as np
import json

EMBEDDING_DTYPE = np.float32
import os

openai.api_type = "azure"
openai.api_base = "https://cs-openai-us-jml.openai.azure.com/"
openai.api_version = "2023-05-15"
openai.api_key = "ff9de7d753b5443b9846bfb3de8e6edb"
f = 1536
u = AnnoyIndex(f, 'angular')
u.load('queen_speeches.ann')
with open('processed_speeches.json') as fp:
    text_dict = json.load(fp)
question = "Opsumer talen fra 2015"
embedding = openai.Embedding.create(input=question,
                                    engine='text-embedding-ada-002')['data'][0]['embedding']
embedding = np.array(embedding, dtype=EMBEDDING_DTYPE)
vectors = u.get_nns_by_vector(embedding, 100, search_k=-1, include_distances=True)
texts = [text_dict[str(i)] for i in vectors[0]]
selected_conversation_hist = [
    {"role": "system",
     "content": f"""
        You are a polite and helpful assistant having a conversation with a human. 
         You are answering questions to the best of your ability. 
         You are not trying to be funny or clever. You are trying to be helpful. 
         You are not trying to show off.
         """},
]
modified_question = "Brugeren spurgte: \n" + \
                    question + \
                    '\n Du har nu følgende fra dronningens nytårstaler fra 2001-2022 at svare ud fra: \n' + \
                    '\n '.join(texts) + \
                    '\n Besvar spørgsmålet.'
# Add question to conversation
messages = selected_conversation_hist + [{"role": "user", "content": modified_question}]

raw_answer = openai.ChatCompletion.create(
    engine="gpt-35-turbo",
    messages=messages
)
print(raw_answer["choices"][0]["message"]["content"])
print('hej')
