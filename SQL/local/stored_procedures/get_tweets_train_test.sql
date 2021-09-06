DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `get_tweets_train_test`()
BEGIN

	SELECT 
    `tweet`.`cleaned_text`, 
    `tweet`.`normalized_text`, 
    `tweet`.`keywords`, 
    `tweet`.`label_id`, 
    `tweet`.`label`, 
    `referenced_tweet`.type
    FROM `twitter`.`tweet`
    LEFT JOIN `twitter`.`referenced_tweet` on `tweet`.`tweet_id` = `referenced_tweet`.`tweet_id`
	where `tweet`.`batch_name` = 'covid_vaccine_global' and
	`tweet`.`keywords` != '';

END$$
DELIMITER ;
