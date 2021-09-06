DELIMITER $$
CREATE DEFINER=`tanniest_karla`@`%` PROCEDURE `insert_reference`(	
	id_ int,
	description_ varchar(2000),
	date_ date,
	url_ varchar(2100),
	retrieved_date_ date
)
BEGIN

	IF NOT EXISTS(SELECT 1 FROM `tanniest_sentimentanalysis`.`reference` WHERE `reference`.id = id_) THEN
		INSERT INTO `tanniest_sentimentanalysis`.`reference`(
			`id`,
			`description`,
			`date`,
			`url`,
			`retrieved_date`)
			VALUES(
			id_,
			description_,
			date_,
			url_,
			retrieved_date_);
	END IF;
    
END$$
DELIMITER ;
