DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `insert_hashtag`(
	hashtag_ VARCHAR(280), 
    cleaned_ VARCHAR(560), 
    tweet_id_ VARCHAR(45)
)
BEGIN

	DECLARE hashtag_id_ INT;
    
	IF NOT EXISTS(SELECT 1 FROM twitter.hashtag h WHERE LOWER(h.`name`) = LOWER(hashtag_)) THEN
		INSERT INTO `twitter`.`hashtag`(`name`, `cleaned`)
		VALUES(hashtag_, cleaned_);
	END IF;
	
	SET hashtag_id_ = (SELECT id FROM twitter.hashtag h WHERE LOWER(h.`name`) = LOWER(hashtag_));
	
    IF NOT EXISTS(SELECT 1 FROM twitter.tweet_hashtag h WHERE `tweet_id` = tweet_id_ AND `hashtag_id`= hashtag_id_) THEN
		INSERT INTO `twitter`.`tweet_hashtag`
		(`tweet_id`,
		`hashtag_id`)
		VALUES
		(tweet_id_,
		hashtag_id_);
	END IF;
END$$
DELIMITER ;
