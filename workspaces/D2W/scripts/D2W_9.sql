

-- -----------------------------------------------------
-- Transformation  CopyAttributeAction
-- -----------------------------------------------------

INSERT INTO `wordpress`.`wp_users` (`user_nicename`)
  SELECT `name` FROM `drupal`.`users_field_data`;

-- -----------------------------------------------------
-- Transformation  CopyAttributeAction
-- -----------------------------------------------------

INSERT INTO `wordpress`.`wp_users` (`user_email`)
  SELECT `mail` FROM `drupal`.`users_field_data`;