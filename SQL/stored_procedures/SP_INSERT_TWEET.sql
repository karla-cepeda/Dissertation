DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `insert_tweet`(
  tweet_id varchar(250),
  original_text varchar(3000),
  cleaned_text varchar(1000),
  token_tweet varchar(1000),
  author_id varchar(250),
  conversation_id varchar(250),
  lang varchar(10),
  created_at datetime,
  place_id varchar(250),
  original_folder varchar(100),
  key_name varchar(45)
)
BEGIN

	INSERT INTO `mydissertation`.`tweet`(
    `tweet_id`,
	`original_text`,
	`cleaned_text`,
    `token_tweet`,
	`author_id`,
	`conversation_id`,
	`lang`,
	`created_at`,
	`place_id`,
	`original_folder`,
    `key_name`)
	VALUES(
    tweet_id,
    original_text,
    cleaned_text,
    token_tweet,
    author_id,
    conversation_id,
    lang,
    CAST(created_at AS DATETIME),
    place_id,
    original_folder,
    key_name);

END$$
DELIMITER ;
