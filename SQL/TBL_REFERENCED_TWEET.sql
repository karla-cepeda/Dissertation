CREATE TABLE `referenced_tweet` (
  `tweet_id` varchar(128) NOT NULL,
  `referenced_id` varchar(128) NOT NULL,
  `type` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`tweet_id`,`referenced_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
