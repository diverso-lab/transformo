

-- -----------------------------------------------------
-- Transformation  CreateEntityAction
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `wordpress`.`wp_links` (
  `id` INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (id))
ENGINE = InnoDB
DEFAULT CHARACTER SET = UTF8MB4;

-- -----------------------------------------------------
-- Transformation  CreateEntityAction
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `wordpress`.`wp_posts` (
  `id` INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (id))
ENGINE = InnoDB
DEFAULT CHARACTER SET = UTF8MB4;