from mycustomLLM import LLM
from langchain_ollama import OllamaLLM
from customagents import agents
import sqlite3



# Fragen an Hochstein: 

# Wie und welche Datenbank am besten einbinden?
# SQlite oder postgres  

# Llama lokal dumm, gut oder soll ich selber weiter recherschieren ?
# model ist plug and play und das is gut. in der arbeit llama 3.2 begründen. 

# Scope des Projekts (wie viele user simulieren ?)
# erstmal implementieren und dann gucken wie realistisch das wird 
                    
# Welche funktionen (tweet, like, comment) genug ?
# erstmal implementieren und dann eventuell funktionen nachbauen wenn es unrealistisch klingt  

#memory function selber implementieren oder nicht ?
#eventuell mit relevanz lösen oder mit vektordatenbank mit embeddings von tweets dann nimmt man nur tweets die vom vektor nah drin sind. chroma db in langchain drinnen
# 
# prompt engineering ?
# sowohl mehr research als auch frei schnautze probieren. 
#  

#database creation test

conn = sqlite3.connect('twitter.db')

c = conn.cursor()

"""c.execute(""CREATE TABLE tweets (
            tweet_id integer primary key,
            user_id integer,
            tweet text,
            likes integer
            )"")"""

c.execute("""INSERT INTO tweets VALUES ('1','2','This is a test tweet', '0')""")
conn.commit()
conn.close()


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


    