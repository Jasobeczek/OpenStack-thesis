-- MySQL Script generated by MySQL Workbench
-- Fri Jun 14 18:01:47 2019
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema reservation_service
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema reservation_service
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `reservation_service` DEFAULT CHARACTER SET utf8 ;
USE `reservation_service` ;

-- -----------------------------------------------------
-- Table `reservation_service`.`laboratory`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `reservation_service`.`laboratory` (
  `id` BIGINT(8) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `duration` TIME NOT NULL,
  `group` VARCHAR(33) NOT NULL COMMENT 'group - OpenStack group id\n',
  `moderator` VARCHAR(45) NOT NULL,
  `limit` INT(8) NOT NULL DEFAULT 1,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `reservation_service`.`team`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `reservation_service`.`team` (
  `id` BIGINT(8) NOT NULL AUTO_INCREMENT,
  `team_id` VARCHAR(33) NULL,
  `owner_id` VARCHAR(33) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `reservation_service`.`reservation`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `reservation_service`.`reservation` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `start` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'When reservation start being active',
  `tenat_id` VARCHAR(45) NULL COMMENT 'ID of tenat when laboratory is created for this reservation',
  `status` ENUM('active', 'nonactive', 'building') NULL DEFAULT 'nonactive' COMMENT 'One of the status depending of state\nBuilding when teant is creating for this reservation\nAtive when tenat is ready and reservation is after the start before start + lab.duration',
  `user` VARCHAR(33) NULL COMMENT 'User id (openstack) who is connected with this resrvation',
  `team_id` BIGINT(8) NULL COMMENT 'Team id (mysql) which is connected with this reservation',
  `laboratory_id` BIGINT(8) NOT NULL COMMENT 'Lab id (mysql) which is responding for creating tenat for this reservation',
  PRIMARY KEY (`id`),
  INDEX `fk_reservation_laboratory1_idx` (`laboratory_id` ASC),
  UNIQUE INDEX `tenat_id_UNIQUE` (`tenat_id` ASC),
  INDEX `fk_reservation_laboratory2_idx` (`team_id` ASC),
  CONSTRAINT `fk_reservation_laboratory1`
    FOREIGN KEY (`laboratory_id`)
    REFERENCES `reservation_service`.`laboratory` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_reservation_laboratory2`
    FOREIGN KEY (`team_id`)
    REFERENCES `reservation_service`.`team` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `reservation_service`.`template`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `reservation_service`.`template` (
  `id` BIGINT(8) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(250) NOT NULL,
  `data` TEXT NOT NULL,
  `laboratory_id` BIGINT(8) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC),
  INDEX `fk_template_laboratory1_idx` (`laboratory_id` ASC),
  CONSTRAINT `fk_template_laboratory1`
    FOREIGN KEY (`laboratory_id`)
    REFERENCES `reservation_service`.`laboratory` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `reservation_service`.`periods`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `reservation_service`.`periods` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `start` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `stop` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `laboratory_id` BIGINT(8) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_periods_laboratory1_idx` (`laboratory_id` ASC),
  CONSTRAINT `fk_periods_laboratory1`
    FOREIGN KEY (`laboratory_id`)
    REFERENCES `reservation_service`.`laboratory` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `reservation_service`.`system`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `reservation_service`.`system` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `project` VARCHAR(45) NULL,
  `role_lab` VARCHAR(45) NULL,
  `role_student` VARCHAR(45) NULL,
  `role_moderator` VARCHAR(45) NULL,
  `group_student` VARCHAR(45) NULL,
  `group_moderator` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
