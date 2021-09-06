DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `get_unlabelled_tweets`(
	global_ TINYINT
)
BEGIN

	SELECT 
    `tweet`.`tweet_id`,
    `tweet`.`original_text`,
    `tweet`.`normalized_text`
    FROM `twitter`.`tweet`
    WHERE `tweet`.`label_id` is NULL AND 
    ((global_ = 0 AND batch_name != 'covid_vaccine_global') OR (global_ = 1 AND batch_name = 'covid_vaccine_global'));

END$$
DELIMITER ;
