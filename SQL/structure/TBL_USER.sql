CREATE TABLE `user` (
  `author_id` varchar(128) NOT NULL,
  `username` varchar(128) NOT NULL,
  `name` varchar(128) NOT NULL,
  `verifed` tinyint(4) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`author_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
