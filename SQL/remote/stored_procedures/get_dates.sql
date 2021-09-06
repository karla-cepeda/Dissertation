DELIMITER $$
CREATE DEFINER=`tanniest_karla`@`%` PROCEDURE `get_dates`()
BEGIN
	SELECT `date`.`id`,
		`date`.`date`,
		`date`.`description`
	FROM `tanniest_sentimentanalysis`.`date`;

END$$
DELIMITER ;
