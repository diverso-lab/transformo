

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



