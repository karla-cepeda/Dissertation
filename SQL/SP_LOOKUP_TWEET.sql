CREATE PROCEDURE `lookup_tweet` (tweet_id TEXT, tweet_text TEXT)
BEGIN

	SELECT 1 
    FROM tweet t
    WHERE t.tweet_id = tweet_id OR t.tweet_text = tweet_text;

END
