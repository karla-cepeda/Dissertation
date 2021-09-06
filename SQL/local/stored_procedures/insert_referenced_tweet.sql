DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `insert_referenced_tweet`(
	tweet_id_ varchar(250),
    referenced_tweet_id_ varchar(250),
    type_ varchar(45)
)
BEGIN

	IF NOT EXISTS(SELECT 1 FROM `twitter`.`referenced_tweet` WHERE  `tweet_id` = tweet_id_ AND `referenced_id` = referenced_tweet_id_) THEN
		INSERT INTO `twitter`.`referenced_tweet`(
		`tweet_id`,
		`referenced_id`,
		`type`)
		VALUES(
		tweet_id_,
		referenced_tweet_id_,
		type_);
	
    END IF;

END$$
DELIMITER ;
