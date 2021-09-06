DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `lookup_sentiment_tweet`(
	tweet_id_ VARCHAR(128)
)
BEGIN

	SELECT 1 AS THIS_EXISTS
    FROM tweet t
    WHERE t.tweet_id = tweet_id_ AND label IS NOT NULL;

END$$
DELIMITER ;
