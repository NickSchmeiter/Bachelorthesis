from mycustomLLM import LLM
from langchain_ollama import OllamaLLM
from customagents import agents

# Fragen an Hochstein: 

# Wie und welche Datenbank am besten einbinden? 

# Llama lokal dumm, gut oder soll ich selber weiter recherschieren ? 

# Scope des Projekts (wie viele user simulieren ?)
                    
# Welche funktionen (tweet, like, comment) genug ? 

tulfirstuser={}
tulseconduser={}


def showtweettoagent(tweet:str,agent:agents,tweetandlikes:dict):
    if agent.evaluatetweet(tweet)=="like":
        tweetandlikes[tweet]+=1

firstuser=agents(age=26,gender='male',nationality='Germany',job='computer science student',
                 interest='Skateboarding',location='Berlin',politicalcompass='leftliberal')
firstuser.setbackground()

seconduser=agents(age=27,gender='female',nationality='half italian, quarter japanese, quarter peruvian',
                  job='marketing at edgless systems(Berliner startup for cybersecurity)',
                 interest='books, food, photography, drugs',location='Berlin',politicalcompass='leftliberal')
seconduser.setbackground()




# tweet1=firstuser.tweet()
# tulfirstuser[tweet1]=0
# print(tweet1)
# tweet2=firstuser.tweet()
# tulfirstuser[tweet2]=0
# print(tweet2)

tweet1=seconduser.tweet()
tulseconduser[tweet1]=0
print(tweet1)
tweet2=seconduser.tweet()
tulseconduser[tweet2]=0
print(tweet2)

# for key in tulfirstuser.keys():
#     showtweettoagent(key,seconduser,tulfirstuser)
#     print(tulfirstuser[key])

#show all tweets to first user and get likes or dislikes
for key in tulseconduser.keys():
    showtweettoagent(key,firstuser,tulseconduser)
    print(tulseconduser[key])


    