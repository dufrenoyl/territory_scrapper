-- -----------------------------------------------------
-- Security - Creation of users
-- -----------------------------------------------------
CREATE USER 'bostonweb'@'localhost' IDENTIFIED BY 'mathieu2414';
GRANT ALL 
ON TerritoryManager.*
TO 'bostonweb'@'localhost';

-- -----------------------------------------------------
-- SCHEMA - Creation
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `TerritoryManager` ;
CREATE SCHEMA IF NOT EXISTS `TerritoryManager` DEFAULT CHARACTER SET utf8 ;
USE `TerritoryManager` ;

-- -----------------------------------------------------
-- Table `Territory`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `TerritoryManager`.`Users` ;

CREATE TABLE IF NOT EXISTS `TerritoryManager`.`Users` (
  `iduser` SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `login` VARCHAR(8) NOT NULL ,
  `password` VARCHAR(500) NULL ,
  `congregation_language` VARCHAR(45) NULL ,
  `congregation_name` VARCHAR(45) NULL ,
  `congregation_address` VARCHAR(45) NULL ,
  `email` VARCHAR(100) NULL ,
  PRIMARY KEY (`iduser`) )
ENGINE = InnoDB
AUTO_INCREMENT = 1
COMMENT = 'Login for users';

CREATE UNIQUE INDEX `login_UNIQUE` ON `TerritoryManager`.`Users` (`login` ASC) ;


-- -----------------------------------------------------
-- Table `Territory`.`Territory`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `TerritoryManager`.`Territory` ;

CREATE  TABLE IF NOT EXISTS `TerritoryManager`.`Territory` (
  `idterritory` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `idterritory_user` SMALLINT UNSIGNED NOT NULL ,
  `title` VARCHAR(10) NOT NULL ,
  `location` VARCHAR(45) NOT NULL ,
  `state` ENUM('MA','NH') NULL ,
  `prospection` TINYINT(1) NULL ,
  `assignee` VARCHAR(45) NULL ,
  `date` DATE NULL ,
  `log` TEXT NULL ,
  PRIMARY KEY (`idterritory`) ,
  CONSTRAINT `fk_user`
    FOREIGN KEY (`idterritory_user`)
    REFERENCES `TerritoryManager`.`Users` (`iduser`))
ENGINE = InnoDB
AUTO_INCREMENT = 1
COMMENT = 'Territory of the Congregation';

CREATE UNIQUE INDEX `idterritory_INDEX` ON `TerritoryManager`.`Territory` (`idterritory` ASC) ;
CREATE UNIQUE INDEX `title_INDEX` ON `TerritoryManager`.`Territory` (`title` ASC) ;
CREATE INDEX `fk_user_INDEX` ON `TerritoryManager`.`Territory` (`idterritory_user` ASC) ;


-- -----------------------------------------------------
-- Table `Territory`.`Person`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `TerritoryManager`.`Person` ;

CREATE  TABLE IF NOT EXISTS `TerritoryManager`.`Person` (
  `idperson` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `idperson_territory` INT UNSIGNED NOT NULL ,
  `firstname` VARCHAR(45) NULL ,
  `middlename` VARCHAR(45) NULL ,
  `lastname` VARCHAR(45) NULL ,
  `address` VARCHAR(45) NOT NULL ,
  `state` ENUM('MA','NH') NULL ,
  `city` VARCHAR(45) NOT NULL ,
  `zipcode` INT(5) ZEROFILL NULL ,
  `phone` CHAR(10) NULL ,
  `date` DATE NULL ,
  `notes` TEXT NULL ,
  `notfrench` TINYINT(1) NULL ,
  `returnvisit` TINYINT(1) NULL ,
  `iswitness` TINYINT(1) NULL ,
  `moved` TINYINT(1) NULL ,
  `donotdisturb` TINYINT(1) NULL ,
  `log` TEXT NULL ,
  PRIMARY KEY (`idperson`) ,
  CONSTRAINT `fk_Territory`
    FOREIGN KEY (`idperson_territory` )
    REFERENCES `TerritoryManager`.`Territory` (`idterritory` ))
ENGINE = InnoDB
AUTO_INCREMENT = 1
COMMENT = 'Person of a congregation';

CREATE UNIQUE INDEX `idPerson_INDEX` ON `TerritoryManager`.`Person` (`idperson` ASC) ;
CREATE INDEX `fk_Territory_INDEX` ON `TerritoryManager`.`Person` (`idperson_territory` ASC) ;
