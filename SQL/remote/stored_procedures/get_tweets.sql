DELIMITER $$
CREATE DEFINER=`tanniest_karla`@`%` PROCEDURE `get_tweets`()
BEGIN

	SELECT `tweet`.`tweet_id`,
		`tweet`.`created_at`,
		`tweet`.`label_id`,
		`tweet`.`label`,
		`tweet`.`author`,
		`tweet`.`conversation_id`,
		`tweet`.`batch_name`,
		`tweet`.`keywords`,
		`tweet`.`keywords_pharma`,
		`tweet`.`tweet_type`,
		`tweet`.`active`
	FROM `tanniest_sentimentanalysis`.`tweet`;



END$$
DELIMITER ;
