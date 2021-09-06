DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `get_tweets_for_migration`()
BEGIN

	SELECT 
	t.`tweet_id`,
	t.`created_at`,
	t.`label_id`,
	t.`label`,
	CASE WHEN u.author_id IS NULL THEN 'other' ELSE u.`username` END author,
    t.`conversation_id`,
	t.`batch_name`,
	t.`keywords`,
	t.`keywords_pharma`,
	CASE WHEN rt.`type` IS NULL THEN 'post' ELSE rt.`type` END AS tweet_type,
	t.`active`
	FROM `twitter`.`tweet` t
	LEFT JOIN `twitter`.`referenced_tweet` rt ON t.tweet_id = rt.tweet_id
    LEFT JOIN `twitter`.`user` u ON u.author_id = t.author_id
	LEFT JOIN `twitter`.`migration` m ON m.tweet_id = t.tweet_id
	WHERE t.batch_name != 'covid_vaccine_global' AND m.tweet_id IS NULL;

END$$
DELIMITER ;
