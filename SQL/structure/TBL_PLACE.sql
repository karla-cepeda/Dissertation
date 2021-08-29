CREATE TABLE `place` (
  `place_id` varchar(128) NOT NULL,
  `name` varchar(200) NOT NULL,
  `country` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`place_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
