DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `insert_log_file`(
	path_ varchar(500),
    filename_ varchar(100),
    extention_ varchar(10),
    total_tweets_ int
)
BEGIN

	INSERT INTO `twitter`.`log_file`
	(`path`,
	`filename`,
    `extention`,
	`total_tweets`)
	VALUES
	(path_,
	filename_,
    extention_,
	total_tweets_);
        
END$$
DELIMITER ;
