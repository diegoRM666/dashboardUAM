SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- Esquema
CREATE SCHEMA IF NOT EXISTS `sensor` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `sensor` ;

-- ============================
-- Tablas
-- ============================

-- 1) SALON
DROP TABLE IF EXISTS `salon`;
CREATE TABLE `salon` (
  `idsalon` INT NOT NULL AUTO_INCREMENT,
  `edificio` VARCHAR(45) NULL,
  `salon` VARCHAR(45) NULL,
  PRIMARY KEY (`idsalon`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 2) PROFESOR
DROP TABLE IF EXISTS `profesor`;
CREATE TABLE `profesor` (
  `idprofesor` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `reconocido` TINYINT NULL,
  `rfid` VARCHAR(45) NULL,
  PRIMARY KEY (`idprofesor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 3) PREFERENCIAS_ATMOSFERICAS (1:1 con UNIQUE en idprofesor)
DROP TABLE IF EXISTS `preferencias_atmosfericas`;
CREATE TABLE `preferencias_atmosfericas` (
  `idpreferatmo` INT NOT NULL AUTO_INCREMENT,
  `temperatura` FLOAT NULL,
  `humedad` FLOAT NULL,
  `luminosidad` FLOAT NULL,
  `idprofesor` INT NOT NULL,
  PRIMARY KEY (`idpreferatmo`),
  CONSTRAINT `uq_preferencias_atmosfericas_idprofesor` UNIQUE (`idprofesor`), -- <== fuerza 1:1
  CONSTRAINT `fk_preferencias_atmosfericas_profesor1`
    FOREIGN KEY (`idprofesor`) REFERENCES `profesor` (`idprofesor`)
    ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 4) CONDICION
DROP TABLE IF EXISTS `condicion`;
CREATE TABLE `condicion` (
  `idcondicion` INT NOT NULL AUTO_INCREMENT,
  `temperatura` FLOAT NULL,
  `humedad` FLOAT NULL,
  `luminosidad` FLOAT NULL,
  `time_condicion` DATETIME NULL,
  `idsalon` INT NULL,
  PRIMARY KEY (`idcondicion`),
  KEY `fk_condicion_salon_idx` (`idsalon`),
  CONSTRAINT `fk_condicion_salon`
    FOREIGN KEY (`idsalon`) REFERENCES `salon` (`idsalon`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 5) VISITA
DROP TABLE IF EXISTS `visita`;
CREATE TABLE `visita` (
  `idvisita` INT NOT NULL AUTO_INCREMENT,
  `visita_entrada` DATETIME NULL,
  `visita_salida` DATETIME NULL,
  `idsalon` INT NULL,
  `idprofesor` INT NULL,
  PRIMARY KEY (`idvisita`),
  KEY `fk_visita_profesor_idx` (`idprofesor`),
  KEY `fk_visita_salon_idx` (`idsalon`),
  CONSTRAINT `fk_visita_profesor` FOREIGN KEY (`idprofesor`) REFERENCES `profesor` (`idprofesor`),
  CONSTRAINT `fk_visita_salon` FOREIGN KEY (`idsalon`) REFERENCES `salon` (`idsalon`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;