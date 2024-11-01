-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema sensor
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema sensor
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `sensor` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `sensor` ;

-- -----------------------------------------------------
-- Table `sensor`.`salon`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sensor`.`salon` (
  `idsalon` INT NOT NULL AUTO_INCREMENT,
  `edificio` VARCHAR(45) NULL DEFAULT NULL,
  `salon` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`idsalon`))
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `sensor`.`condicion`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sensor`.`condicion` (
  `idcondicion` INT NOT NULL AUTO_INCREMENT,
  `temperatura` FLOAT NULL DEFAULT NULL,
  `humedad` FLOAT NULL DEFAULT NULL,
  `luminosidad` FLOAT NULL DEFAULT NULL,
  `timestamp` DATETIME NULL DEFAULT NULL,
  `idsalon` INT NULL DEFAULT NULL,
  PRIMARY KEY (`idcondicion`),
  INDEX `fk_condicion_salon_idx` (`idsalon` ASC) VISIBLE,
  CONSTRAINT `fk_condicion_salon`
    FOREIGN KEY (`idsalon`)
    REFERENCES `sensor`.`salon` (`idsalon`))
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `sensor`.`profesor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sensor`.`profesor` (
  `idprofesor` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL DEFAULT NULL,
  `reconocido` TINYINT NULL DEFAULT NULL,
  `rfid` VARCHAR(45) NULL DEFAULT NULL,
  `count` INT NULL DEFAULT NULL,
  PRIMARY KEY (`idprofesor`))
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `sensor`.`preferencias_atmosfericas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sensor`.`preferencias_atmosfericas` (
  `idpreferatmo` INT NOT NULL AUTO_INCREMENT,
  `temperatura` FLOAT NULL DEFAULT NULL,
  `humedad` FLOAT NULL DEFAULT NULL,
  `luminosidad` FLOAT NULL DEFAULT NULL,
  `idprofesor` INT NOT NULL,
  PRIMARY KEY (`idpreferatmo`),
  INDEX `fk_preferencias_atmosfericas_profesor1_idx` (`idprofesor` ASC) VISIBLE,
  CONSTRAINT `fk_preferencias_atmosfericas_profesor1`
    FOREIGN KEY (`idprofesor`)
    REFERENCES `sensor`.`profesor` (`idprofesor`))
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `sensor`.`visita`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sensor`.`visita` (
  `idvisita` INT NOT NULL AUTO_INCREMENT,
  `fecha` DATE NULL DEFAULT NULL,
  `hora` VARCHAR(45) NULL DEFAULT NULL,
  `idsalon` INT NULL DEFAULT NULL,
  `idprofesor` INT NULL DEFAULT NULL,
  PRIMARY KEY (`idvisita`),
  INDEX `fk_visita_profesor_idx` (`idprofesor` ASC) VISIBLE,
  INDEX `fk_visita_salon_idx` (`idsalon` ASC) VISIBLE,
  CONSTRAINT `fk_visita_profesor`
    FOREIGN KEY (`idprofesor`)
    REFERENCES `sensor`.`profesor` (`idprofesor`),
  CONSTRAINT `fk_visita_salon`
    FOREIGN KEY (`idsalon`)
    REFERENCES `sensor`.`salon` (`idsalon`))
ENGINE = InnoDB
AUTO_INCREMENT = 7
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
