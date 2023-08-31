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
t = AnnoyIndex(f, 'angular')
idx = 0
text_dict = {}
for i in range(2001, 2023):
    with open(f'/app/queens_speeches/speeches/{i}.txt') as f:
        total_text = f"År {i}"
        for line_idx, line in enumerate(f.readlines()):
            total_text += '\n' + line
            line = line.strip()
            if len(line)>0:
                line = f'År: {i}\n Linjenummer: {line_idx} \n' +  line
                embedding = openai.Embedding.create(input=line, engine='text-embedding-ada-002')['data'][0]['embedding']
                embedding = np.array(embedding, dtype=EMBEDDING_DTYPE)
                t.add_item(idx, embedding)
                text_dict[idx] = line
                idx += 1
    selected_conversation_hist = [
        {"role": "system",
         "content": f"""
            Your job is to summarize the Danish Queens new years speeches.
            Please include information such as but not limited to 
            themes, people, countries, facts, events and minorities.
            Please do so in Danish.
             """},
    ]
    modified_question = "Opsummer følgende tale: \n" + \
                        total_text
    # Add question to conversation
    messages = selected_conversation_hist + [{"role": "user", "content": modified_question}]

    raw_answer = openai.ChatCompletion.create(
        engine="gpt-35-turbo",
        messages=messages
    )
    answer = raw_answer["choices"][0]["message"]["content"]
    embedding = openai.Embedding.create(input=answer, engine='text-embedding-ada-002')['data'][0]['embedding']
    embedding = np.array(embedding, dtype=EMBEDDING_DTYPE)
    t.add_item(i, embedding)
    text_dict[idx] = answer
    idx += 1
    print(i)
t.build(10) # 10 trees
t.save('queen_speeches.ann')

with open('processed_speeches.json', 'w') as fp:
    json.dump(text_dict, fp)