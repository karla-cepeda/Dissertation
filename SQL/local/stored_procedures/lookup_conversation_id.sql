DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `lookup_conversation_id`(
	conversation_id_ VARCHAR(128)
)
BEGIN

	SELECT 1 AS THIS_EXISTS
    FROM twitter.tweet t
    WHERE t.conversation_id = conversation_id_;

END$$
DELIMITER ;
