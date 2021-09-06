DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `get_log_file`(
	preprocessed_ TINYINT,
    labelled_ TINYINT    
)
BEGIN

	SELECT id, path, filename, extention
    FROM twitter.log_file
    WHERE (`preprocessed` = preprocessed_ OR preprocessed_ = -1);

END$$
DELIMITER ;
