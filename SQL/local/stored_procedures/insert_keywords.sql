DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `insert_keywords`(
	tweet_id_ varchar(50),
    keywords_ varchar(300),
    keywords_pharma_ varchar(300)
)
BEGIN

	UPDATE `twitter`.`tweet`
	SET
	`keywords` = keywords_,
	`keywords_pharma` = keywords_pharma_
	WHERE `tweet_id` = tweet_id_;


END$$
DELIMITER ;
