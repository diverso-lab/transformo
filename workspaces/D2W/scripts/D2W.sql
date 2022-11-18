

-- -----------------------------------------------------
-- Transformation  CreateEntityAction
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `wordpress`.`wp_postmeta` (
  `id` INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (id))
ENGINE = InnoDB
DEFAULT CHARACTER SET = UTF8MB4;

-- -----------------------------------------------------
-- Transformation  CreateEntityAction
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `wordpress`.`wp_usermeta` (
  `id` INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (id))
ENGINE = InnoDB
DEFAULT CHARACTER SET = UTF8MB4;

-- -----------------------------------------------------
-- Transformation  CreateEntityAction
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `wordpress`.`wp_options` (
  `id` INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (id))
ENGINE = InnoDB
DEFAULT CHARACTER SET = UTF8MB4;

-- -----------------------------------------------------
-- Transformation  CreateEntityAction
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `wordpress`.`wp_term_relationships` (
  `id` INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (id))
ENGINE = InnoDB
DEFAULT CHARACTER SET = UTF8MB4;

-- -----------------------------------------------------
-- Transformation  CreateEntityAction
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `wordpress`.`wp_terms` (
  `id` INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (id))
ENGINE = InnoDB
DEFAULT CHARACTER SET = UTF8MB4;

-- -----------------------------------------------------
-- Transformation  CreateEntityAction
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `wordpress`.`wp_postmeta` (
  `id` INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (id))
ENGINE = InnoDB
DEFAULT CHARACTER SET = UTF8MB4;

-- -----------------------------------------------------
-- Transformation  CreateAttributeAction
-- -----------------------------------------------------

ALTER TABLE `wordpress`.`wp_options`
  ADD COLUMN `autoload` VARCHAR(20);