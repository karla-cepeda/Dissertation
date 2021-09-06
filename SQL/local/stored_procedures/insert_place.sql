DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `insert_place`(
  place_id_ varchar(128),
  name_ varchar(200),
  country_ varchar(200)

)
BEGIN

	IF NOT EXISTS(SELECT 1 FROM place p WHERE p.place_id = place_id_) THEN
		INSERT INTO `twitter`.`place`
		(`place_id`,
		`name`,
		`country`)
		VALUES
		(place_id_,
		name_,
		country_);
        
	END IF;

END$$
DELIMITER ;
