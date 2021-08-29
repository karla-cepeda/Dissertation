CREATE TABLE `tweet` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tweet_id` varchar(250) NOT NULL,
  `original_text` varchar(3000) NOT NULL,
  `cleaned_text` varchar(1000) NOT NULL,
  `token_tweet` varchar(1000) NOT NULL,
  `author_id` varchar(250) DEFAULT NULL,
  `conversation_id` varchar(250) NOT NULL,
  `lang` varchar(10) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `place_id` varchar(250) DEFAULT NULL,
  `original_folder` varchar(100) NOT NULL,
  `key_name` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tweet_id_UNIQUE` (`tweet_id`)
) ENGINE=InnoDB AUTO_INCREMENT=26088 DEFAULT CHARSET=utf8 COMMENT='Tweets collected from Twitter API.';
