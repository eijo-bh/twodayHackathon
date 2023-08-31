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
        for line in f.readlines():
            line = line.strip()
            if len(line)>0:
                line = f'År: {i}\n' +  line
                embedding = openai.Embedding.create(input=line, engine='text-embedding-ada-002')['data'][0]['embedding']
                embedding = np.array(embedding, dtype=EMBEDDING_DTYPE)
                t.add_item(idx, embedding)
                text_dict[idx] = line
                idx += 1
    print(i)
t.build(10) # 10 trees
t.save('queen_speeches.ann')

with open('processed_speeches.json', 'w') as fp:
    json.dump(text_dict, fp)