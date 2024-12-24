from langchain_ollama import OllamaLLM
from mycustomLLM import LLM
import sqlite3
import random
class agents(object):
    def __init__(self,userid:int, age:int, gender: str, nationality:str, job:str, interest:str, location:str, politicalcompass:str):
        self.userid=userid
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
        backgroundtext="Imagine you are a Twitter user with the following background. This is your background. You are a " +str(self.age)+ " years old, your gender is "+self.gender+" youre nationality is "+self.nationality+" and your job is "+self.job+" your interest is "+self.interest
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
        
        total="This is part of your memory and NOT a prompt! The prompt is in the last abstract!!!\n"
        mem=self.get_memory()
        for i in mem:
            total+=i
            total+="\n"
        total+="This was the end of your memory now follows the prompt\n"
        total= total+text
        result = self.LLM.prompt(total)
        self.add_memory(text) #add input to memory
        self.add_memory(result) #add output to memory
        return result
    
    # #almost no tweets with this prompt so adapting: According to your background and your recent twitter behavior, decide if you want to tweet something or not. 
    #             The likelyhood of tweeting should be around 10%.
    #             The more often you dont tweet the more likely you should tweet.
    #             If you decide to tweet, just answer with 'tweet' if you decide not to tweet answer with 'dont tweet'
    #             Dont return anything else your answer should really just be 'tweet' or 'dont tweet'.


    def decidesandtweets(self):
        conn = sqlite3.connect('twitter.db')
        c = conn.cursor()

        if random.random()<=0.4:
            tweet=self.tweet()
            #get the highest tweetid and add 1 to it to get the new tweetid
            tweetid=c.execute("SELECT MAX(tweet_id) FROM tweets").fetchone()[0]
            if tweetid==None:
                tweetid=-1
            tweetid+=1
            #add tweet to database
            c.execute("INSERT INTO tweets Values (:tweet_id, :user_id, :tweettext, :likes)",{'tweet_id':tweetid,'user_id':self.userid,'tweettext':tweet,'likes':0})
        conn.commit()
        
        
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