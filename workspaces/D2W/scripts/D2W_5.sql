

-- -----------------------------------------------------
-- Transformation  InsertReferenceAction
-- -----------------------------------------------------

INSERT INTO `wordpress`.`wp_users` (`ID`)
  SELECT MIN(`uid`) FROM `drupal`.`users_field_data`
  GROUP BY `uid`
  ORDER BY `uid`;


-- -----------------------------------------------------
-- Transformation  UpdateFromFieldAction
-- -----------------------------------------------------

UPDATE `wordpress`.`wp_users` table_target
       INNER JOIN `drupal`.`users_field_data` table_source
       ON table_source.`uid` = table_target.`ID`


    
    SET table_target.`user_nicename` = table_source.`name`
    


WHERE table_source.`uid` = table_target.`ID`;





-- -----------------------------------------------------
-- Transformation  UpdateFromFieldAction
-- -----------------------------------------------------

UPDATE `wordpress`.`wp_users` table_target
       INNER JOIN `drupal`.`users_field_data` table_source
       ON table_source.`uid` = table_target.`ID`


    
    SET table_target.`user_login` = table_source.`name`
    


WHERE table_source.`uid` = table_target.`ID`;





-- -----------------------------------------------------
-- Transformation  UpdateFromFieldAction
-- -----------------------------------------------------

UPDATE `wordpress`.`wp_users` table_target
       INNER JOIN `drupal`.`users_field_data` table_source
       ON table_source.`uid` = table_target.`ID`


    
    SET table_target.`display_name` = table_source.`name`
    


WHERE table_source.`uid` = table_target.`ID`;





-- -----------------------------------------------------
-- Transformation  UpdateFromFieldAction
-- -----------------------------------------------------

UPDATE `wordpress`.`wp_users` table_target
       INNER JOIN `drupal`.`users_field_data` table_source
       ON table_source.`uid` = table_target.`ID`


    
    SET table_target.`user_email` = table_source.`mail`
    


WHERE table_source.`uid` = table_target.`ID`;





-- -----------------------------------------------------
-- Transformation  UpdateFromFieldAction
-- -----------------------------------------------------

UPDATE `wordpress`.`wp_users` table_target
       INNER JOIN `drupal`.`users_field_data` table_source
       ON table_source.`uid` = table_target.`ID`


    
    SET table_target.`user_pass` = table_source.`pass`
    


WHERE table_source.`uid` = table_target.`ID`;





-- -----------------------------------------------------
-- Transformation  InsertReferenceAction
-- -----------------------------------------------------

INSERT INTO `wordpress`.`wp_posts` (`ID`)
  SELECT MIN(`nid`) FROM `drupal`.`node_field_data`
  WHERE `drupal`.`node_field_data`.`type` IN ('article')
  GROUP BY `nid`
  ORDER BY `nid`;


-- -----------------------------------------------------
-- Transformation  UpdateFromFieldAction
-- -----------------------------------------------------

UPDATE `wordpress`.`wp_posts` table_target
       INNER JOIN `drupal`.`node_field_data` table_source
       ON table_source.`nid` = table_target.`ID`


    
    SET table_target.`post_author` = table_source.`uid`
    


WHERE table_source.`nid` = table_target.`ID`;





-- -----------------------------------------------------
-- Transformation  UpdateFromFieldAction
-- -----------------------------------------------------

UPDATE `wordpress`.`wp_posts` table_target
       INNER JOIN `drupal`.`node_field_data` table_source
       ON table_source.`nid` = table_target.`ID`

    SET table_target.`post_date` = FROM_UNIXTIME(table_source.`created`)

WHERE table_source.`nid` = table_target.`ID`;





-- -----------------------------------------------------
-- Transformation  UpdateFromFieldAction
-- -----------------------------------------------------

UPDATE `wordpress`.`wp_posts` table_target
       INNER JOIN `drupal`.`node_field_data` table_source
       ON table_source.`nid` = table_target.`ID`

    SET table_target.`post_date_gmt` = FROM_UNIXTIME(table_source.`created`)

WHERE table_source.`nid` = table_target.`ID`;





-- -----------------------------------------------------
-- Transformation  UpdateFromFieldAction
-- -----------------------------------------------------

UPDATE `wordpress`.`wp_posts` table_target
       INNER JOIN `drupal`.`node_field_data` table_source
       ON table_source.`nid` = table_target.`ID`

    SET table_target.`post_modified` = FROM_UNIXTIME(table_source.`created`)

WHERE table_source.`nid` = table_target.`ID`;





-- -----------------------------------------------------
-- Transformation  UpdateFromFieldAction
-- -----------------------------------------------------

UPDATE `wordpress`.`wp_posts` table_target
       INNER JOIN `drupal`.`node_field_data` table_source
       ON table_source.`nid` = table_target.`ID`

    SET table_target.`post_modified_gmt` = FROM_UNIXTIME(table_source.`created`)

WHERE table_source.`nid` = table_target.`ID`;





-- -----------------------------------------------------
-- Transformation  UpdateFromFieldAction
-- -----------------------------------------------------

UPDATE `wordpress`.`wp_posts` table_target
       INNER JOIN `drupal`.`node_field_data` table_source
       ON table_source.`nid` = table_target.`ID`


    
    SET table_target.`post_title` = table_source.`title`
    


WHERE table_source.`nid` = table_target.`ID`;





-- -----------------------------------------------------
-- Transformation  UpdateFromFieldAction
-- -----------------------------------------------------

UPDATE `wordpress`.`wp_posts` table_target
       INNER JOIN `drupal`.`node_field_data` table_source
       ON table_source.`nid` = table_target.`ID`


    
    SET table_target.`post_name` = REPLACE(table_source.`title`, ' ', '-')
    


WHERE table_source.`nid` = table_target.`ID`;





-- -----------------------------------------------------
-- Transformation  UpdateFromFieldAction
-- -----------------------------------------------------

UPDATE `wordpress`.`wp_posts` table_target
       INNER JOIN `drupal`.`node__body` table_source
       ON table_source.`entity_id` = table_target.`ID`


    
    SET table_target.`post_content` = table_source.`body_value`
    


WHERE table_source.`entity_id` = table_target.`ID`;





-- -----------------------------------------------------
-- Transformation  InsertReferenceAction
-- -----------------------------------------------------

INSERT INTO `wordpress`.`wp_comments` (`comment_ID`)
  SELECT MIN(`entity_id`) FROM `drupal`.`node_revision__field_summary`
  GROUP BY `entity_id`
  ORDER BY `entity_id`;


-- -----------------------------------------------------
-- Transformation  UpdateFromFieldAction
-- -----------------------------------------------------

UPDATE `wordpress`.`wp_comments` table_target
       INNER JOIN `drupal`.`node_revision__field_summary` table_source
       ON table_source.`entity_id` = table_target.`comment_ID`


    
    SET table_target.`comment_post_ID` = table_source.`entity_id`
    


WHERE table_source.`entity_id` = table_target.`comment_ID`;





-- -----------------------------------------------------
-- Transformation  UpdateFromFieldAction
-- -----------------------------------------------------

UPDATE `wordpress`.`wp_comments` table_target
       INNER JOIN `drupal`.`node_revision__field_summary` table_source
       ON table_source.`entity_id` = table_target.`comment_ID`


    
    SET table_target.`comment_content` = table_source.`field_summary_value`
    


WHERE table_source.`entity_id` = table_target.`comment_ID`;



