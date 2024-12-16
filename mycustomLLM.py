
from langchain_ollama import OllamaLLM
#this is the first file for my bachelorthesis
class LLM(object):
    def __init__(self, model):
        self.model = model

    def prompt(self, text)->str:
        result = self.model.invoke(text)
        return result
