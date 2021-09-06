DELIMITER $$
CREATE DEFINER=`tanniest_karla`@`%` PROCEDURE `insert_date_reference`(
	date_id_ int,
	reference_id_ int)
BEGIN

	IF NOT EXISTS(SELECT 1 FROM `tanniest_sentimentanalysis`.`date_reference` WHERE `date_reference`.date_id = date_id_ AND `date_reference`.reference_id = reference_id_) THEN

		INSERT INTO `tanniest_sentimentanalysis`.`date_reference`(
		`date_id`,
		`reference_id`)
		VALUES
		(date_id_,
		reference_id_);
    
    END IF;
    
END$$
DELIMITER ;
