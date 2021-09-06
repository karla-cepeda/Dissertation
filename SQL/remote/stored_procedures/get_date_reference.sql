DELIMITER $$
CREATE DEFINER=`tanniest_karla`@`%` PROCEDURE `get_date_reference`()
BEGIN

	SELECT 
		`date_reference`.`date_id`,
        `reference`.`id`,
		`reference`.`description`,
		`reference`.`date`,
		`reference`.`url`,
		`reference`.`retrieved_date`
	FROM `tanniest_sentimentanalysis`.`reference` 
    INNER JOIN `tanniest_sentimentanalysis`.`date_reference` ON `reference`.`id` = `date_reference`.`reference_id`;


END$$
DELIMITER ;
