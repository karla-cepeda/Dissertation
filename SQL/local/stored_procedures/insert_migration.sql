DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `insert_migration`(
	tweet_id_ varchar(50)
)
BEGIN

	INSERT INTO `twitter`.`migration`
	(`tweet_id`)
	VALUES
	(tweet_id_);


END$$
DELIMITER ;
