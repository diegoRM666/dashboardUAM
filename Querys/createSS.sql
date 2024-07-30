-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`profesor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`profesor` (
  `idprofesor` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `reconocido` TINYINT NULL,
  `rfid` VARCHAR(45) NULL,
  `count` INT NULL,
  PRIMARY KEY (`idprofesor`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`salon`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`salon` (
  `idsalon` INT NOT NULL AUTO_INCREMENT,
  `edificio` VARCHAR(45) NULL,
  `salon` VARCHAR(45) NULL,
  PRIMARY KEY (`idsalon`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`condicion`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`condicion` (
  `idcondicion` INT NOT NULL AUTO_INCREMENT,
  `temperatura` FLOAT NULL,
  `humedad` FLOAT NULL,
  `luminosidad` FLOAT NULL,
  PRIMARY KEY (`idcondicion`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`visita`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`visita` (
  `idvisita` INT NOT NULL AUTO_INCREMENT,
  `fecha` DATE NULL,
  `hora` VARCHAR(45) NULL,
  `idsalon` INT NULL,
  `idprofesor` INT NULL,
  `idcondicion` INT NULL,
  PRIMARY KEY (`idvisita`),
  INDEX `fk_visita_profesor_idx` (`idprofesor` ASC) VISIBLE,
  INDEX `fk_visita_condicion_idx` (`idcondicion` ASC) VISIBLE,
  INDEX `fk_visita_salon_idx` (`idsalon` ASC) VISIBLE,
  CONSTRAINT `fk_visita_profesor`
    FOREIGN KEY (`idprofesor`)
    REFERENCES `mydb`.`profesor` (`idprofesor`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_visita_condicion`
    FOREIGN KEY (`idcondicion`)
    REFERENCES `mydb`.`condicion` (`idcondicion`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_visita_salon`
    FOREIGN KEY (`idsalon`)
    REFERENCES `mydb`.`salon` (`idsalon`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
