

-- -----------------------------------------------------
-- Transformation  CopyAttributeAction
-- -----------------------------------------------------

INSERT INTO `wordpress`.`wp_postmeta` (`meta_key`)
  SELECT `langcode` FROM `drupal`.`node__field_preparation_time`;