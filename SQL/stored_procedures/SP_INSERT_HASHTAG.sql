DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `insert_hashtag`(hashtag VARCHAR(100), tweet_id VARCHAR(45))
BEGIN

	DECLARE hashtag_id INT;
    
	IF NOT EXISTS(SELECT 1 FROM mydissertation.hashtag h WHERE LOWER(h.`name`) = LOWER(hashtag)) THEN
		INSERT INTO `mydissertation`.`hashtag`(`name`)
		VALUES(hashtag);
	END IF;
	
	SET hashtag_id = (SELECT id FROM mydissertation.hashtag h WHERE LOWER(h.`name`) = LOWER(hashtag));
	
	INSERT INTO `mydissertation`.`tweet_hashtag`
	(`tweet_id`,
	`hashtag_id`)
	VALUES
	(tweet_id,
	hashtag_id);

END$$
DELIMITER ;
