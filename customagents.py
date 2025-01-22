from langchain_ollama import OllamaLLM
from mycustomLLM import LLM
import sqlite3
import random
class agents(object):
    def __init__(self,userid:int,username:str, age:int, gender: str, nationality:str, job:str, interest:str, location:str, politicalcompass:str):
        self.userid=userid
        self.username=username
        self.age = age
        self.gender= gender
        self.nationality = nationality
        self.job = job
        self.interest = interest
        self.location = location
        self.politicalcompass = politicalcompass    
        self.memory={"followings":["Users you follow:"],
                    "tweets":["Your Tweets:"],
                    "likes": ["Tweets Liked:"],
                    "comments":["Your Comments:"],
                    "background":["Your Background:"],
                    "tweetstyle":["Your Tweetstyle:"]
                    }
        self.LLM=LLM(model=OllamaLLM(model="llama3.2"))


    #sets background for the agent so agent get context for what he can tweet about 
    # and adds it to memory of the agent
    def setbackground(self):
        backgroundtext="Imagine you are a Twitter user with the following background. This is your background. Your Username is " +self.username+ "You are a " +str(self.age)+ " years old, your gender is "+self.gender+" youre nationality is "+self.nationality+" and your occupation is "+self.job+" your interest is "+self.interest
        backgroundtext=backgroundtext+" You are currently located in "+self.location+" and your political compass is "+self.politicalcompass
        self.add_memory("background",backgroundtext)
    
    def gettweetstyles(self)->str:
        return self.prompt("Please provide 5 different styles of tweets. Just give back the different styles with one example each nothing else.")
    
    #tweetstyle set and decision
    def settweetstyle(self,givenstyles:str):
        decideonstyle="Please decide on a tweetstyle. Use your background and think what would make the most sense. Answer with the tweetstyle and two example tweets according to the style"
        style=self.prompt(givenstyles+decideonstyle)
        self.add_memory("tweetstyle",style)


    #adds string to memorydictionary so agent can recall it later
    def add_memory(self, key, text):
        self.memory[key].append(text)


    #returns memorydictionary
    def get_memory(self)->dict:
        return self.memory
    

    #recalls memory and then adds the text and prompts this to the LLM and returns an answer
    def prompt(self, text)->str:
        
        total="This is part of your memory:"
        mem=self.get_memory()
        for key in mem.keys():
            for i in mem[key]:
                total+=str(i)
                total+="\n"
        total+="This was your memory\n"
        total= total+text
        result = self.LLM.prompt(total)
        return result
    
    # #almost no tweets with this prompt so adapting: According to your background and your recent twitter behavior, decide if you want to tweet something or not. 
    #             The likelyhood of tweeting should be around 10%.
    #             The more often you dont tweet the more likely you should tweet.
    #             If you decide to tweet, just answer with 'tweet' if you decide not to tweet answer with 'dont tweet'
    #             Dont return anything else your answer should really just be 'tweet' or 'dont tweet'.

    """
    old promt function which threw errors bc of memory integration
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
    """

    def decidesandtweets(self):
        conn = sqlite3.connect('twitter.db')
        c = conn.cursor()
        q="Do you wanna tweet anything? If yes just return 'yes' if you dont want to tweet return 'no' Think about your background and your recent twitter behavior."
        res=self.prompt(q)
        #if random.random()<0.4:
        if res=="yes":
            tweet=self.tweet()
            #get the highest tweetid and add 1 to it to get the new tweetid
            tweetid=c.execute("SELECT MAX(tweet_id) FROM tweets").fetchone()[0]
            if tweetid==None:
                tweetid=-1
            tweetid+=1
            #add tweet to database
            c.execute("INSERT INTO tweets Values (:tweet_id, :username, :user_id, :tweettext, :likes)",{'tweet_id':tweetid, 'username':self.username, 'user_id':self.userid,'tweettext':tweet,'likes':0})
        conn.commit()
        
        
    #prompts a generic tweet
    def tweet(self)->str:
        standardtweet="""This is your prompt: Please make a twitter tweet according to your background and memory.
                      Your tweet should be as realistic as possible so just refer to your background slightly.  
                      The tweet should be in english. The tweet should make sense according to your memory.
                      Focus on the tweetstyle you decided on. Tweet according to that style.
                      If you refer to a topic from your background just focus on one topic not multiple.
                      Also try that every tweet is distinct. The tweets should look different from the ones in your memory.
                      Here are some examples of tweets:
                      "No one is born hating another person because of the color of his skin or his background or his religion..."
                      "I hope that even my worst critics remain on Twitter, because that is what free speech means"
                      "Teamwork makes the dream work."
                      Remember tweets have a maximum of 280 characters
                      and usually they use hashtags # and mentions @. 
                      Just post the tweet and nothing else. Nothing preeceding or following the tweet."""
        res=self.prompt(standardtweet)
        self.add_memory("tweets",res)
        return res
    
    def evaluatetweettolike(self,tweet)->str:
        prompt="""Please evaluate the tweet which will follow after this prompt.
                  You should evaluate if you would give the tweet a like from a twitter user perspective.
                  remember your background and memory and evaluate the tweet according to that.
                  You can like each tweet just once.
                  This means if the tweet is in your memory as a like dont like it again.
                  If you would like the tweet, just return 'like' if you would not like the tweet return 'dislike'
                  HERE COMES THE TWEET: \n"""
        prompt=prompt+tweet
        res=self.prompt(prompt)
        count=0 
        while res!="like" and res!="dislike":
            res=self.prompt(prompt+'your answer was too long please return just "like" or "dislike"')
            count+=1
            if count>3:
                res="dislike"
        if res=="like":
            self.add_memory("likes",tweet)
        return res
    
    def showalltweetstoagent(self):
        conn = sqlite3.connect('twitter.db')
        c = conn.cursor()
        tweetlist = c.execute("""
            SELECT tweet_id, tweettext, likes, user_id, username 
            FROM tweets 
            WHERE user_id IN (
            SELECT followered_id 
            FROM followers 
            WHERE follower_id = :user_id
            )
            ORDER BY tweet_id DESC
            LIMIT 10
        """, {'user_id': self.userid}).fetchall()

        if len(tweetlist) < 10:
            additional_tweets = c.execute("""
            SELECT tweet_id, tweettext, likes, user_id, username 
            FROM tweets 
            WHERE user_id NOT IN (
                SELECT followered_id 
                FROM followers 
                WHERE follower_id = :user_id
            ) AND user_id != :user_id
            ORDER BY tweet_id DESC
            LIMIT :limit
            """, {'user_id': self.userid, 'limit': 10 - len(tweetlist)}).fetchall()
            tweetlist.extend(additional_tweets)
        for tweet in tweetlist:
            tweet_id, tweettext, likes, tweetauthor , tweetauthorusername = tweet
            if self.evaluatetweettolike(tweettext) == "like":
                new_likes = likes + 1
                c.execute("UPDATE tweets SET likes = :new_likes WHERE tweet_id = :tweet_id", {'new_likes': new_likes, 'tweet_id': tweet_id})
            if tweet_id not in self.memory['comments'] and self.evaluatetweettocomment(tweettext) == "comment":
                comment = self.getcomment(tweet_id, tweetauthorusername, tweettext)
                commentid = c.execute("SELECT MAX(comment_id) FROM comments").fetchone()[0]
                if commentid == None:
                    commentid = -1
                c.execute("INSERT INTO comments VALUES (:comment_id,:username, :user_id, :tweet_id, :tweet_author_id, :commenttext)", {'comment_id': commentid+1, 'username': self.username, 'user_id': self.userid, 'tweet_id': tweet_id, 'tweet_author_id': tweetauthor, 'commenttext': comment})
            if tweetauthorusername not in self.memory["followings"] and self.evaluatetweettofollow(tweettext, tweetauthorusername) == "follow":
               c.execute("INSERT INTO followers VALUES (:follower_id, :follower_username, :followered_id, :followered_username)", {'follower_id': self.userid, 'follower_username': self.username, 'followered_id': tweetauthor,'followered_username': tweetauthorusername})

            conn.commit()
        conn.close()
    
    def evaluatetweettocomment(self,tweet)->str:
        prompt="""Please evaluate the tweet which will follow after this prompt.
                    You should evaluate if you would give the tweet a comment from a twitter user perspective.
                    remember your background and memory and evaluate the tweet according to that.
                    If you would like to comment on the tweet, just return 'comment' if you would not like to comment the tweet return 'not comment'
                    Dont return anything else your answer should really just be 'comment' or 'not comment'.
                    HERE COMES THE TWEET: \n"""
        prompt=prompt+tweet
        res=self.prompt(prompt)
        count=0
        while res!="comment" and res!="not comment":
            res=self.prompt('your answer was not "comment" or "not comment" Please try again and just send an answer which is "comment" or "not comment"')
            count+=1
            if count>3:
                res="not comment"
        return res
    
    def getcomment(self,tweetid, tweetauthor,tweet)->str:
        prompt="""Please write your comment now. Your comment should be in english and should make sense according to the tweet. The comment should be realistic and not too long.
          It doesnt make sense to comment the same comment under multiple tweets. So if the comment is in your memory already dont comment the same one.
          Just post the comment and nothing else. Nothing preeceding or following the comment. Also you can mention the username of the tweet if you want.
          HERE COMES THE TWEET:\n"""
        prompt=prompt+tweet+"This is the username of the tweet author: "+tweetauthor
        res=self.prompt(prompt)
        self.add_memory("comments",tweetid)
        self.add_memory("comments",res)
        return res

    def evaluatetweettofollow(self,tweet, tweetauthorusername)->str:
        prompt="""Please evaluate the tweet which will follow after this prompt.
                  You should evaluate if you would want to follow this user who made the tweet from a twitter user perspective.
                  If you follow this user you will see more tweets from this user in the future.
                  remember your background and memory and evaluate the tweet according to that.
                  You can follow each user just once if you follow this user already please ignore the evaluation.
                  If you want to follow the user, just return 'follow' if you do not want to follow the user return 'not follow'
                  Dont return anything else your answer should really just be 'follow' or 'not follow'.
                  HERE COMES THE TWEET: \n"""
        prompt=prompt+tweet
        res=self.prompt(prompt)
        count=0
        while res!="follow" and res!="not follow":
            res=self.prompt('your answer was not "follow" or "not follow" Please try again and just send an answer which is "follow" or "not follow"')
            count+=1
            if count>3:
                res="not follow"
        if res=="follow":
            self.add_memory("followings",tweetauthorusername)
        return res