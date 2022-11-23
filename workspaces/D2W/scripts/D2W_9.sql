

-- -----------------------------------------------------
-- Transformation  CopyAttributeAction
-- -----------------------------------------------------

INSERT INTO `wordpress`.`wp_users` (`user_nicename`)
  SELECT `name` FROM `drupal`.`users_field_data` ORDER BY `uid`;

-- -----------------------------------------------------
-- Transformation  UpdateAttributeAction
-- -----------------------------------------------------

UPDATE `wordpress`.`wp_users` table_target
       INNER JOIN `drupal`.`users_field_data` table_source
       ON table_source.`uid` = table_target.`ID`
SET table_target.`user_email` = table_source.`mail`
WHERE table_source.`uid` = table_target.`ID`;

-- -----------------------------------------------------
-- Transformation  UpdateAttributeAction
-- -----------------------------------------------------

UPDATE `wordpress`.`wp_users` table_target
       INNER JOIN `drupal`.`users_field_data` table_source
       ON table_source.`uid` = table_target.`ID`
SET table_target.`user_pass` = table_source.`pass`
WHERE table_source.`uid` = table_target.`ID`;