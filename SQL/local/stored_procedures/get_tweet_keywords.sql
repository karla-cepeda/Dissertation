DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `get_tweet_keywords`()
BEGIN

	SELECT 
	`tweet`.`tweet_id`,
	`tweet`.`cleaned_text`
	FROM `twitter`.`tweet`
	WHERE `tweet`.`keywords` IS NULL;

END$$
DELIMITER ;
