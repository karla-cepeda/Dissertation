DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `get_all_tweets`()
BEGIN

	SELECT `tweet`.`tweet_id`,
		`tweet`.`original_text`,
		`tweet`.`cleaned_text`,
		`tweet`.`normalized_text`,
		`tweet`.`author_id`,
		`tweet`.`conversation_id`,
		`tweet`.`in_reply_to_user_id`,
		`tweet`.`lang`,
		`tweet`.`created_at`,
		`tweet`.`place_id`,
		`tweet`.`batch_name`,
		`tweet`.`key_name`,
		`tweet`.`keywords`,
        `tweet`.`label_id`,
        `tweet`.`label`,
        `referenced_tweet`.type,
        `user`.`username`,
        `user`.`name`,
        user2.`username` AS in_replay_to_username,
        user2.`name` AS in_replay_to_name
	FROM `twitter`.`tweet`
	LEFT JOIN `twitter`.`referenced_tweet` on `tweet`.`tweet_id` = `referenced_tweet`.`tweet_id`
    LEFT JOIN `twitter`.`user` ON `user`.`author_id` = `tweet`.`author_id`
    LEFT JOIN `twitter`.`user` AS user2 ON user2.`author_id` = `tweet`.`in_reply_to_user_id`
	WHERE `tweet`.`batch_name` != 'covid_vaccine_global';
    
END$$
DELIMITER ;
