DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `truncate_log_file_label`()
BEGIN

	UPDATE `twitter`.`log_file`
	SET
	`labelled` = 0,
	`labelled_at` = NULL;

END$$
DELIMITER ;
