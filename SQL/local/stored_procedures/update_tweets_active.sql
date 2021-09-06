DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `update_tweets_active`(
	tweet_id_ VARCHAR(50), 
    active_ TINYINT
)
BEGIN

	UPDATE `twitter`.`tweet`
	SET
	`active` = active_
	WHERE `tweet_id` = tweet_id_;

END$$
DELIMITER ;
