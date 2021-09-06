DELIMITER $$
CREATE DEFINER=`tanniest_karla`@`%` PROCEDURE `insert_date`(
	id_ int,
	date_ date,
	description_ varchar(2000),
	from_ireland_ tinyint
)
BEGIN

	IF NOT EXISTS(SELECT 1 FROM `tanniest_sentimentanalysis`.`date` WHERE `date`.id = id_) THEN
		INSERT INTO `tanniest_sentimentanalysis`.`date`(
			`id`,
			`date`,
			`description`,
			`from_ireland`)
		VALUES(
			id_,
			date_,
			description_,
			from_ireland_);
	END IF;

END$$
DELIMITER ;
