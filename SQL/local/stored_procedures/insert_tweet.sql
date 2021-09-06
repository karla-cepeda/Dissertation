DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `insert_tweet`(
  tweet_id_ varchar(50),
  original_text_ varchar(6000),
  cleaned_text_ varchar(560),
  normalized_text_ varchar(560),
  author_id_ varchar(50),
  conversation_id_ varchar(50),
  in_reply_to_user_id_ varchar(50),
  lang_ varchar(10),
  created_at_ datetime,
  place_id_ varchar(50),
  batch_name_ varchar(100),
  key_name_ varchar(10)
  
)
BEGIN

	INSERT INTO `twitter`.`tweet`(
    `tweet_id`,
	`original_text`,
	`cleaned_text`,
	`normalized_text`,
	`author_id`,
	`conversation_id`,
    `in_reply_to_user_id`,
	`lang`,
	`created_at`,
	`place_id`,
	`batch_name`,
    `key_name`)
	VALUES(
    tweet_id_,
    original_text_,
    cleaned_text_,
    normalized_text_,
    author_id_,
    conversation_id_,
    in_reply_to_user_id_,
    lang_,
    CAST(created_at_ AS DATETIME),
    place_id_,
    batch_name_,
    key_name_);

END$$
DELIMITER ;
