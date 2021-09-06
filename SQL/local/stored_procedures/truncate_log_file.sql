DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `truncate_log_file`()
BEGIN

	TRUNCATE TABLE log_file;

END$$
DELIMITER ;
