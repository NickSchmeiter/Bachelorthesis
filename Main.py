from mycustomLLM import LLM
from langchain_ollama import OllamaLLM
from customagents import agents

model = OllamaLLM(model="llama3.2")
agent = LLM(model=model)
firstuser=agents(age=26,gender='male',country='Germany',job='computer science student',interest='Skateboarding')
test=firstuser.prompt("Please make a twitter tweet in english which is funny")
print(test)
test=firstuser.prompt("Please make another twitter tweet in english which is funny just answer with a tweet not Sentence before and no Sentence after!")
print(test)
