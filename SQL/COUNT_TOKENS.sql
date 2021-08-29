SELECT * FROM mydissertation.tweet where original_folder like '%media_2021%' and author_id = '91334232' order by id desc limit 50;

select * from mydissertation.tweet where conversation_id like '1387500648275582983'; #'1394722090654261253';
select * from mydissertation.`user` where author_id = '91334232';


select * from mydissertation.tweet where cleaned_text like '%rollout%' and (cleaned_text like '%vaccine%' or cleaned_text like '%vaccines%');

select count(1) from mydissertation.tweet;

select * from mydissertation.tweet where conversation_id = '1344373771201818624';

SELECT
ORIGINAL_text,
cleaned_text,
token_tweet,
CASE WHEN LENGTH(token_tweet) = 0 THEN 0 ELSE
 ROUND((LENGTH(token_tweet)-LENGTH( REPLACE (token_tweet, ",", ""))) / LENGTH(","))+1 
END AS COUNT,
conversation_id
FROM tweet 
ORDER BY COUNT ASC
limit 100;


SELECT * FROM TWEET T
WHERE TWEET_ID = '1360351742790148102';

SELECT * FROM REFERENCED_TWEET WHERE TWEET_ID = '1360356150504488963';

SELECT * FROM TWEET WHERE CONVERSATION_ID = '1360351742790148102';


SELECT * FROM `USER` WHERE AUTHOR_ID = '1182020039274323968';



SELECT DISTINCT CONVERSATION_ID FROM TWEET WHERE TWEET_ID NOT IN (SELECT DISTINCT CONVERSATION_ID FROM TWEET);


SELECT * FROM TWEET WHERE CONVERSATION_ID = '1294544424123469826';

SELECT * FROM referenced_tweet WHERE TWEET_ID IN ('1294544433019604994', '1294544431450914817');

SELECT * FROM USER WHERE AUTHOR_ID ='150246405';
