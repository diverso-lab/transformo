

-- -----------------------------------------------------
-- Transformation  CopyAttributeAction
-- -----------------------------------------------------

INSERT INTO `wordpress`.`wp_postmeta` (`meta_key`)
  SELECT `langcode` FROM `drupal`.`node__field_preparation_time`;

-- -----------------------------------------------------
-- Transformation  CopyAttributeAction
-- -----------------------------------------------------

INSERT INTO `wordpress`.`wp_termmeta` (`bundle`)
  SELECT `bundle` FROM `drupal`.`node__field_preparation_time`;

-- -----------------------------------------------------
-- Transformation  CopyAttributeAction
-- -----------------------------------------------------

INSERT INTO `wordpress`.`wp_termmeta` (`bundle`)
  SELECT `bundle` FROM `drupal`.`node__field_preparation_time`;