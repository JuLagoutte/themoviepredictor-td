-- Adminer 4.7.3 MySQL dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

DROP TABLE IF EXISTS `companies`;
CREATE TABLE `companies` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS `movies`;
CREATE TABLE `movies` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `original_title` varchar(255) NOT NULL,
  `synopsis` text,
  `duration` int(11) NOT NULL,
  `release_date` date NOT NULL,
  `rating` enum('TP','-12','-16','-18') NOT NULL,
  `prod_budget` int(11) DEFAULT NULL,
  `marketing_budget` int(11) DEFAULT NULL,
  `3D` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS `movies_companies_roles`;
CREATE TABLE `movies_companies_roles` (
  `movie_id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL,
  `company_id` int(11) NOT NULL,
  KEY `movies_companies_roles_fk0` (`movie_id`),
  KEY `movies_companies_roles_fk1` (`role_id`),
  KEY `movies_companies_roles_fk2` (`company_id`),
  CONSTRAINT `movies_companies_roles_fk0` FOREIGN KEY (`movie_id`) REFERENCES `movies` (`id`),
  CONSTRAINT `movies_companies_roles_fk1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`),
  CONSTRAINT `movies_companies_roles_fk2` FOREIGN KEY (`company_id`) REFERENCES `companies` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS `movies_origin_countries`;
CREATE TABLE `movies_origin_countries` (
  `movie_id` int(11) NOT NULL,
  `country_iso2` char(2) NOT NULL,
  KEY `movies_origin_countries_fk0` (`movie_id`),
  CONSTRAINT `movies_origin_countries_fk0` FOREIGN KEY (`movie_id`) REFERENCES `movies` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS `movies_people_roles`;
CREATE TABLE `movies_people_roles` (
  `movie_id` int(11) NOT NULL,
  `people_id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL,
  KEY `movies_people_roles_fk0` (`movie_id`),
  KEY `movies_people_roles_fk1` (`people_id`),
  KEY `movies_people_roles_fk2` (`role_id`),
  CONSTRAINT `movies_people_roles_fk0` FOREIGN KEY (`movie_id`) REFERENCES `movies` (`id`),
  CONSTRAINT `movies_people_roles_fk1` FOREIGN KEY (`people_id`) REFERENCES `people` (`id`),
  CONSTRAINT `movies_people_roles_fk2` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS `people`;
CREATE TABLE `people` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS `roles`;
CREATE TABLE `roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- 2019-10-08 08:18:53
