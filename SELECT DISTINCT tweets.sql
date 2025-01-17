SELECT DISTINCT tweets.tweettext, comments.commenttext 
FROM tweets 
RIGHT JOIN comments ON tweets.tweet_id = comments.tweet_id 
WHERE tweets.tweet_id = 6;