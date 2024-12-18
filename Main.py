from mycustomLLM import LLM
from langchain_ollama import OllamaLLM
from customagents import agents

model = OllamaLLM(model="llama3.2")
agent = LLM(model=model)
firstuser=agents(age=26,gender='male',nationality='Germany',job='computer science student',
                 interest='Skateboarding',location='Berlin',politicalcompass='leftliberal')
firstuser.setbackground()
test=firstuser.tweet()
print(test)
test=firstuser.tweet()
print(test)
