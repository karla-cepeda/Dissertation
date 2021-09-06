DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `clean_tables`()
BEGIN
    TRUNCATE TABLE twitter.hashtag;
    TRUNCATE TABLE twitter.referenced_tweet;
    TRUNCATE TABLE twitter.place;
    TRUNCATE TABLE twitter.tweet;
    TRUNCATE TABLE twitter.tweet_hashtag;
	TRUNCATE TABLE twitter.`user`;
    UPDATE twitter.log_file SET preprocessed = 0, preprocessed_at = NULL;
END$$
DELIMITER ;
