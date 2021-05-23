CREATE DEFINER=`root`@`localhost` PROCEDURE `insert_user`(
  author_id varchar(128),
  username varchar(128),
  `name` varchar(128),
  verifed tinyint(4),
  created_at datetime
)
BEGIN

	IF NOT EXISTS(SELECT 1 FROM user u WHERE u.author_id = author_id) THEN
		INSERT INTO `mydissertation`.`user`(
		`author_id`,
		`username`,
		`name`,
		`verifed`,
		`created_at`)
		VALUES(
		author_id,
		username,
		`name`,
		verifed,
		CAST(created_at AS DATETIME));
        
	END IF;

END