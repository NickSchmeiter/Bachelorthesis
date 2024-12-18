from langchain_ollama import OllamaLLM
from mycustomLLM import LLM
class agents(object):
    def __init__(self, age:int, gender: str, country:str, job:str, interest:str):
        self.age = age
        self.gender= gender
        self.country = country
        self.job = job
        self.interest = interest
        self.memory=[]
        self.LLM=LLM(model=OllamaLLM(model="llama3.2"))
    def tweet(self)->str:
        standardtweet="""Please make a twitter tweet according to your background and memory.
                      The tweet should be in english. Remember tweets have a maximum of 280 characters
                      and usually they use hashtags # and mentions @. """
    def prompt(self, text)->str:

        total=""
        mem=self.get_memory()
        for i in mem:
            total+="This is part of your memory and NOT a prompt! The prompt is in the last abstract!!!\n"
            total+=i
            total+="\n"
        total= total+text
        result = self.LLM.prompt(total)
        self.add_memory(text) #add input to memory
        self.add_memory(result) #add output to memory
        return result
    
    def setbackground(self):
        backgroundtext="This is your background. You are a " +str(self.age)+ " years old, your gender is "+self.gender+" you are from "+self.country+" and your job is "+self.job+" your interest is "+self.interest
        self.add_memory(backgroundtext)

    def add_memory(self, text:str):
        self.memory.append(text)
    def get_memory(self)->list:
        return self.memory