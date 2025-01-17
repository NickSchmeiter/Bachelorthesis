from mycustomLLM import LLM
from langchain_ollama import OllamaLLM
from customagents import agents
import database
import sqlite3
import pandas as pd


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

# Read data from Excel file
file_path = '/Users/nickschmeiter/Downloads/Bachelorthesis/Users.xlsx'
df = pd.read_excel(file_path)

# Fill lists with data from the Excel file
ageslist = df['age'].tolist()
usernamelist = df['username'].tolist()
genderlist = df['gender'].tolist()
nationalitylist = df['nationality'].tolist()
joblist = df['job'].tolist()
interestlist = df['interest'].tolist()
locationlist = df['location'].tolist()
politicalcompasslist = df['politicalcompass'].tolist()
agentlist = []

#create all users which are given in the lists
def createagents():
    conn = sqlite3.connect('twitter.db')
    c = conn.cursor()
    for i in range(len(ageslist)):
        
        agentlist.append(agents(userid=i,username=usernamelist[i],age=ageslist[i],gender=genderlist[i],nationality=nationalitylist[i],job=joblist[i],interest=interestlist[i],location=locationlist[i],politicalcompass=politicalcompasslist[i]))
        styles=agentlist[i].gettweetstyles()
        agentlist[i].setbackground()
        agentlist[i].settweetstyle(styles)
        #save agent data in database
        c.execute("INSERT INTO users Values (:userid, :username, :age, :gender, :nationality, :job, :interest, :location, :politicalcompass)",
                  {'userid':agentlist[i].userid,'username':agentlist[i].username,'age':agentlist[i].age,'gender':agentlist[i].gender,'nationality':agentlist[i].nationality,'job':agentlist[i].job,'interest':agentlist[i].interest,'location':agentlist[i].location,'politicalcompass':agentlist[i].politicalcompass})
        conn.commit()
    conn.close()                     


def main():
    database.createdatatables()
    createagents()
    days=1
    for day in range(3*days):
        for agent in agentlist:
            agent.decidesandtweets()
        for agent in agentlist:
            agent.showalltweetstoagent()
        print("1/3 Day finished")
    print("Simulation finished")


main()

    