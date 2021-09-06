DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `insert_user`(
  author_id_ varchar(128),
  username_ varchar(128),
  name_ varchar(128),
  verifed_ tinyint(4),
  created_at_ datetime
)
BEGIN

	IF NOT EXISTS(SELECT 1 FROM user u WHERE u.author_id = author_id_) THEN
		INSERT INTO `twitter`.`user`(
		`author_id`,
		`username`,
		`name`,
		`verifed`,
		`created_at`)
		VALUES(
		author_id_,
		username_,
		name_,
		verifed_,
		CAST(created_at_ AS DATETIME));
        
	END IF;

END$$
DELIMITER ;
