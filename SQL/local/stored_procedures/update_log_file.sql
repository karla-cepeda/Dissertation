DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `update_log_file`(
	id_ INT(11), 
    path_ VARCHAR(100), 
    filename_ VARCHAR(50), 
    preprocessed_ TINYINT,
    labelled_ TINYINT
)
BEGIN
	IF preprocessed_ != -1 THEN
		IF NOT EXISTS(SELECT 1 FROM twitter.log_file lf WHERE lf.id = id_ AND lf.filename = filename_ AND lf.preprocessed = 1) THEN
			UPDATE `twitter`.`log_file` 
			SET `preprocessed` = 1, `preprocessed_at` = CURRENT_TIMESTAMP() 
			WHERE `id` = id_ AND `path` = path_ AND `filename` = filename_;
			
		END IF;
	END IF;
    
    IF labelled_ != -1 THEN
		IF NOT EXISTS(SELECT 1 FROM twitter.log_file lf WHERE lf.id = id_ AND lf.filename = filename_ AND lf.labelled = 1) THEN
			UPDATE `twitter`.`log_file` 
			SET `labelled` = 1, `labelled_at` = CURRENT_TIMESTAMP() 
			WHERE `id` = id_ AND `path` = path_ AND `filename` = filename_;
			
		END IF;
	END IF;

END$$
DELIMITER ;
