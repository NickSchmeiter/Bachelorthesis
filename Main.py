from mycustomLLM import LLM
from langchain_ollama import OllamaLLM
from customagents import agents
import database
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

ageslist=[26,27]
genderlist=["male","female"]
nationalitylist=["Germany","half italian, quarter japanese, quarter peruvian"]
joblist=["computer science student","marketing at edgless systems(Berliner startup for cybersecurity)"]
interestlist=["Skateboarding","books, food, photography"]
locationlist=["Berlin","Berlin"]
politicalcompasslist=["leftliberal","leftliberal"]
agentlist=[]

#create all users which are given in the lists
def createagents():
    conn = sqlite3.connect('twitter.db')
    c = conn.cursor()
    for i in range(len(ageslist)):
        
        agentlist.append(agents(userid=i,age=ageslist[i],gender=genderlist[i],nationality=nationalitylist[i],job=joblist[i],interest=interestlist[i],location=locationlist[i],politicalcompass=politicalcompasslist[i]))
        agentlist[i].setbackground()
        #safe agent data in database
        c.execute("INSERT INTO users Values (:userid, :age, :gender, :nationality, :job, :interest, :location, :politicalcompass)",
                  {'userid':agentlist[i].userid,'age':agentlist[i].age,'gender':agentlist[i].gender,'nationality':agentlist[i].nationality,'job':agentlist[i].job,'interest':agentlist[i].interest,'location':agentlist[i].location,'politicalcompass':agentlist[i].politicalcompass})
        conn.commit()
    conn.close()                     




def showalltweetstoagentandlikes(agent:agents):
    conn = sqlite3.connect('twitter.db')
    c = conn.cursor()
    tweetlist = c.execute("SELECT tweet_id, tweettext, likes FROM tweets WHERE user_id != :user_id", {'user_id': agent.userid}).fetchall()
    for tweet in tweetlist:
        tweet_id, tweettext, likes = tweet
        if agent.evaluatetweet(tweettext) == "like":
            new_likes = likes + 1
            c.execute("UPDATE tweets SET likes = :new_likes WHERE tweet_id = :tweet_id", {'new_likes': new_likes, 'tweet_id': tweet_id})
            conn.commit()
    conn.close()

def main():
    database.createdatatables()
    createagents()
    days=2
    for agent in agentlist:
        for i in range(5*days):
            agent.decidesandtweets()
    for agent in agentlist:
        agent.showalltweetstoagentandlikes()


main()

    