DELIMITER $$
CREATE DEFINER=`tanniest_karla`@`%` PROCEDURE `insert_tweet_date`()
BEGIN

	INSERT INTO tweet_date
	SELECT t.tweet_id, d.id
	FROM `tanniest_sentimentanalysis`.`tweet` t
	INNER JOIN `tanniest_sentimentanalysis`.`date` d ON CAST(t.created_at AS DATE) = d.date 
	LEFT JOIN `tanniest_sentimentanalysis`.`tweet_date` td ON td.tweet_id = t.tweet_id AND td.event_id = d.id
	WHERE td.tweet_id IS NULL;

END$$
DELIMITER ;
