CREATE DEFINER=`root`@`localhost` PROCEDURE `insert_place`(
  place_id varchar(128),
  `name` varchar(200),
  country varchar(200)

)
BEGIN

	IF NOT EXISTS(SELECT 1 FROM place p WHERE p.place_id = place_id) THEN
		INSERT INTO `mydissertation`.`place`
		(`place_id`,
		`name`,
		`country`)
		VALUES
		(place_id,
		`name`,
		country);
        
	END IF;

END