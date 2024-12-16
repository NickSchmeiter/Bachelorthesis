import torch
from transformers import pipeline
from langchain_ollama import OllamaLLM
#this is the first file for my bachelorthesis
'''
model_path = "/Users/nickschmeiter/Library/Application Support/Ollama"

pipe = pipeline("text-generation",
                model=model_path,
                model_kwargs={'torch_dtype': 'float32'},)
messages=[{"role":"user","content":"Hello, how are you?"}]
output = pipe(messages)
assistant_response = output[0]['generated_text']
print(assistant_response)'''


model = OllamaLLM(model="llama3.2")
result=model.invoke("Hello, how are you?")
print(result)