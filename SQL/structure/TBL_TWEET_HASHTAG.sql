CREATE TABLE `tweet_hashtag` (
  `tweet_id` varchar(128) NOT NULL,
  `hashtag_id` varchar(128) NOT NULL,
  PRIMARY KEY (`tweet_id`,`hashtag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Hashtag in tweet.';
