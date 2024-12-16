from mycustomLLM import LLM
from langchain_ollama import OllamaLLM

model = OllamaLLM(model="llama3.2")
agent = LLM(model=model)
studentintro=agent.prompt("DONT SPEAK ITALIAN!!! imagine you are a italian economics student and approach a stranger please answer in english")
print(studentintro)
agent2 = LLM(model=model)

print(agent2.prompt(studentintro+"answer in english"))
