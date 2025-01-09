import sqlite3
def createdatatables():
    
    #database creation test

    conn = sqlite3.connect('twitter.db')
    #conn = sqlite3.connect(':memory:')

    c = conn.cursor()

    # Enable foreign key support
    c.execute("PRAGMA foreign_keys = ON;")

    # create user table
    c.execute("""CREATE TABLE users (
            user_id integer primary key,
            username text,  
            age integer,
            gender text,
            nationality text,
            job text,
            interest text,
            location text,
            politicalcompass text
            )""")
    
    #create follower table
    c.execute("""CREATE TABLE followers (
            follower_id integer,
            follower_username text,  
            followered_id integer,
            followered_username text,  
            FOREIGN KEY (follower_id) REFERENCES users (user_id),
            FOREIGN KEY (followered_id) REFERENCES users (user_id)
            PRIMARY KEY (follower_id, followered_id)
            )""")
    
    # create tweets table
    c.execute("""CREATE TABLE tweets (
            tweet_id integer primary key,
            username text,  
            user_id integer,  
            tweettext text,
            likes integer,
            FOREIGN KEY (user_id) REFERENCES users (user_id)  
            )""")
    
    # create comments table

    c.execute("""CREATE TABLE comments (
            comment_id integer primary key,
            username text,  
            user_id integer,
            tweet_id integer,
            tweet_author_id integer,            
            commenttext text,
            FOREIGN KEY (tweet_author_id) REFERENCES users (user_id),  
            FOREIGN KEY (user_id) REFERENCES users (user_id),
            FOREIGN KEY (tweet_id) REFERENCES tweets (tweet_id)    
            )""")

    # commit and close connection

    conn.commit()
    conn.close()