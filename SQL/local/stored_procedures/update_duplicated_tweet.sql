DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `update_duplicated_tweet`(
	tweet_id_ VARCHAR(50)
)
BEGIN

	UPDATE `twitter`.`tweet`
	SET
	`duplicated` = 1
	WHERE `tweet_id` = tweet_id_;
    
END$$
DELIMITER ;
