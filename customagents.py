from langchain_ollama import OllamaLLM
from mycustomLLM import LLM
class agents(object):
    def __init__(self, age:int, gender: str, nationality:str, job:str, interest:str, location:str, politicalcompass:str):
        self.age = age
        self.gender= gender
        self.nationality = nationality
        self.job = job
        self.interest = interest
        self.location = location
        self.politicalcompass = politicalcompass    
        self.memory=[]
        self.LLM=LLM(model=OllamaLLM(model="llama3.2"))


    #sets background for the agent so agent get context for what he can tweet about 
    # and adds it to memory of the agent
    def setbackground(self):
        backgroundtext="This is your background. You are a " +str(self.age)+ " years old, your gender is "+self.gender+" youre nationality is "+self.nationality+" and your job is "+self.job+" your interest is "+self.interest
        backgroundtext=backgroundtext+" You are currently located in "+self.location+" and your political compass is "+self.politicalcompass
        self.add_memory(backgroundtext)


    #adds string to memorylist so agent can recall it later
    def add_memory(self, text:str):
        self.memory.append(text)


    #returns memorylist
    def get_memory(self)->list:
        return self.memory
    

    #recalls memory and then adds the text and prompts this to the LLM and returns an answer
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
    
    #prompts a generic tweet
    def tweet(self)->str:
        standardtweet="""This is your prompt: Please make a twitter tweet according to your background and memory.
                      Your tweet should be as realistic as possible so dont overestimate your background.  
                      The tweet should be in english. The tweet should make sense according to your memory.
                      Tweet like you are a heavy twitter user so dont focus too much on your background in each single tweet.

                      Remember tweets have a maximum of 280 characters
                      and usually they use hashtags # and mentions @. 
                      Just post the tweet and nothing else. Nothing preeceding or following the tweet."""
        return self.prompt(standardtweet)
    
    def evaluatetweet(self,tweet)->str:
        prompt="""This is your prompt: Please evaluate the tweet which will follow after this prompt.
                  You should evaluate if you would give the tweet a like from a twitter user perspective.
                  remember your background and memory and evaluate the tweet according to that.
                  If you would like the tweet, just return 'like' if you would not like the tweet return 'dislike'
                  Dont return anything else your answer should really just be 'like' or 'dislike'.
                  HERE COMES THE TWEET: \n"""
        prompt=prompt+tweet
        return self.prompt(prompt)