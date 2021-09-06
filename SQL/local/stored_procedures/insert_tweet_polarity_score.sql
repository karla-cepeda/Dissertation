DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `insert_tweet_polarity_score`(
	tweet_id_ varchar(50),
	tem_ INT(11),
	label_ varchar(10)
)
BEGIN

	UPDATE `twitter`.`tweet`
	SET
	`label_id` = tem_,
	`label` = label_
	WHERE `tweet_id` = tweet_id_;

END$$
DELIMITER ;
