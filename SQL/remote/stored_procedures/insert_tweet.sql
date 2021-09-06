DELIMITER $$
CREATE DEFINER=`tanniest_karla`@`%` PROCEDURE `insert_tweet`(
	tweet_id_ varchar(50) CHARSET utf8,
	created_at_ datetime,
	label_id_ int,
	label_ varchar(45),
	batch_name_ varchar(45),
    keywords_ varchar(300),
    keywords_pharm_ varchar(300),
	tweet_type_ varchar(45)
)
BEGIN

	IF NOT EXISTS(SELECT 1 FROM `tanniest_sentimentanalysis`.`tweet` WHERE `tweet`.`tweet_id` = tweet_id_) THEN
		INSERT INTO `tanniest_sentimentanalysis`.`tweet`
		(`tweet_id`,
		`created_at`,
		`label_id`,
		`label`,
		`batch_name`,
        `keywords`,
        `keywords_pharm`,
		`tweet_type`)
		VALUES
		(
		tweet_id_,
		created_at_,
		label_id_,
		label_,
		batch_name_,
        keywords_,
        keywords_pharm_,
		tweet_type_);
        
	END IF;

END$$
DELIMITER ;
