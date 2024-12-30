-- MySQL dump 10.16  Distrib 10.1.48-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: wheelie_dynamic
-- ------------------------------------------------------
-- Server version	10.1.48-MariaDB-0ubuntu0.18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `address`
--

DROP TABLE IF EXISTS `address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `address` (
  `address_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `address` varchar(50) DEFAULT NULL,
  `address2` varchar(50) DEFAULT NULL,
  `city_id` int(10) unsigned DEFAULT NULL,
  `postal_code` varchar(10) DEFAULT NULL,
  `last_update` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`address_id`),
  UNIQUE KEY `address_address_IDX` (`address`,`city_id`,`postal_code`) USING BTREE,
  KEY `address_FK` (`city_id`),
  CONSTRAINT `address_FK` FOREIGN KEY (`city_id`) REFERENCES `city` (`city_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=506879 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `car`
--

DROP TABLE IF EXISTS `car`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `car` (
  `car_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `producer` varchar(50) DEFAULT NULL,
  `model` varchar(50) CHARACTER SET utf8 COLLATE utf8_polish_ci DEFAULT NULL,
  `rental_rate` decimal(12,2) DEFAULT NULL,
  `create_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_update` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`car_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `city`
--

DROP TABLE IF EXISTS `city`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `city` (
  `city_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `city` varchar(50) NOT NULL,
  `country_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`city_id`),
  UNIQUE KEY `city_unique` (`city`,`country_id`),
  KEY `city_FK` (`country_id`),
  CONSTRAINT `city_FK` FOREIGN KEY (`country_id`) REFERENCES `country` (`country_id`)
) ENGINE=InnoDB AUTO_INCREMENT=386047 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `country`
--

DROP TABLE IF EXISTS `country`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `country` (
  `country_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `country` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`country_id`),
  UNIQUE KEY `country_country_IDX` (`country`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=372008 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer` (
  `customer_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `address_id` int(10) unsigned DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `birth_date` date DEFAULT NULL,
  `create_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_update` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`customer_id`),
  UNIQUE KEY `customer_first_name_IDX` (`first_name`,`last_name`,`address_id`) USING BTREE,
  KEY `customer_FK` (`address_id`),
  CONSTRAINT `customer_FK` FOREIGN KEY (`address_id`) REFERENCES `address` (`address_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=506776 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `equipment`
--

DROP TABLE IF EXISTS `equipment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `equipment` (
  `equipment_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `version` varchar(50) DEFAULT NULL,
  `create_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_update` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`equipment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `inventory`
--

DROP TABLE IF EXISTS `inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inventory` (
  `inventory_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `car_id` int(10) unsigned DEFAULT NULL,
  `production_year` int(4) DEFAULT NULL,
  `fuel_type` varchar(15) DEFAULT NULL,
  `store_id` int(10) unsigned DEFAULT NULL,
  `purchase_price` decimal(18,2) DEFAULT NULL,
  `sell_price` decimal(18,2) DEFAULT NULL,
  `create_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_update` datetime DEFAULT CURRENT_TIMESTAMP,
  `license_plates` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`inventory_id`),
  KEY `inventory_FK` (`car_id`),
  KEY `inventory_FK_1` (`store_id`),
  CONSTRAINT `inventory_FK` FOREIGN KEY (`car_id`) REFERENCES `car` (`car_id`),
  CONSTRAINT `inventory_FK_1` FOREIGN KEY (`store_id`) REFERENCES `store` (`store_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1195 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `inventory_equipment`
--

DROP TABLE IF EXISTS `inventory_equipment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inventory_equipment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `inventory_id` int(10) unsigned DEFAULT NULL,
  `equipment_id` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `inventory_equipment_FK` (`inventory_id`),
  KEY `inventory_equipment_FK_1` (`equipment_id`),
  CONSTRAINT `inventory_equipment_FK` FOREIGN KEY (`inventory_id`) REFERENCES `inventory` (`inventory_id`),
  CONSTRAINT `inventory_equipment_FK_1` FOREIGN KEY (`equipment_id`) REFERENCES `equipment` (`equipment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13124 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `payment`
--

DROP TABLE IF EXISTS `payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `payment` (
  `payment_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `customer_id` int(10) unsigned DEFAULT NULL,
  `rental_id` int(10) unsigned DEFAULT NULL,
  `amount` decimal(12,2) DEFAULT NULL,
  `payment_date` date DEFAULT NULL,
  `last_update` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`payment_id`),
  KEY `payment_FK` (`rental_id`),
  KEY `payment_FK_1` (`customer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1538878 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rental`
--

DROP TABLE IF EXISTS `rental`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rental` (
  `rental_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `rental_rate` decimal(12,2) DEFAULT NULL,
  `customer_id` int(10) unsigned DEFAULT NULL,
  `inventory_id` int(10) unsigned DEFAULT NULL,
  `staff_id` int(10) unsigned DEFAULT NULL,
  `rental_date` date DEFAULT NULL,
  `return_date` date DEFAULT NULL,
  `payment_deadline` date DEFAULT NULL,
  `create_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `technical_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`rental_id`),
  KEY `rental_FK` (`customer_id`),
  KEY `rental_FK_1` (`inventory_id`),
  KEY `rental_FK_2` (`staff_id`),
  CONSTRAINT `rental_FK` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`) ON DELETE CASCADE,
  CONSTRAINT `rental_FK_1` FOREIGN KEY (`inventory_id`) REFERENCES `inventory` (`inventory_id`),
  CONSTRAINT `rental_FK_2` FOREIGN KEY (`staff_id`) REFERENCES `staff` (`staff_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2782062 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary table structure for view `rows_by_insert_date`
--

DROP TABLE IF EXISTS `rows_by_insert_date`;
/*!50001 DROP VIEW IF EXISTS `rows_by_insert_date`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `rows_by_insert_date` (
  `insert_date` tinyint NOT NULL,
  `days_ago` tinyint NOT NULL,
  `days_generated` tinyint NOT NULL,
  `rowcount` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `service`
--

DROP TABLE IF EXISTS `service`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `service` (
  `service_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `inventory_id` int(10) unsigned NOT NULL,
  `service_type` varchar(100) NOT NULL,
  `service_date` date NOT NULL,
  `service_cost` decimal(18,4) NOT NULL,
  PRIMARY KEY (`service_id`),
  UNIQUE KEY `service_inventory_id_IDX` (`inventory_id`,`service_type`,`service_date`) USING BTREE,
  CONSTRAINT `service_FK` FOREIGN KEY (`inventory_id`) REFERENCES `inventory` (`inventory_id`)
) ENGINE=InnoDB AUTO_INCREMENT=35564 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `staff`
--

DROP TABLE IF EXISTS `staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `staff` (
  `staff_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `store_id` int(10) unsigned DEFAULT NULL,
  `address_id` int(10) unsigned DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `manager_id` int(10) unsigned DEFAULT NULL,
  `hired_date` date DEFAULT NULL,
  `last_update` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`staff_id`),
  KEY `staff_FK` (`store_id`),
  KEY `staff_FK_1` (`manager_id`),
  KEY `staff_FK_2` (`address_id`),
  CONSTRAINT `staff_FK` FOREIGN KEY (`store_id`) REFERENCES `store` (`store_id`),
  CONSTRAINT `staff_FK_2` FOREIGN KEY (`address_id`) REFERENCES `address` (`address_id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `store`
--

DROP TABLE IF EXISTS `store`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `store` (
  `store_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `store_manager_id` int(10) unsigned DEFAULT NULL,
  `address_id` int(10) unsigned DEFAULT NULL,
  `last_update` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`store_id`),
  KEY `store_FK` (`address_id`),
  KEY `store_FK_1` (`store_manager_id`),
  CONSTRAINT `store_FK` FOREIGN KEY (`address_id`) REFERENCES `address` (`address_id`),
  CONSTRAINT `store_FK_1` FOREIGN KEY (`store_manager_id`) REFERENCES `staff` (`staff_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Final view structure for view `rows_by_insert_date`
--

/*!50001 DROP TABLE IF EXISTS `rows_by_insert_date`*/;
/*!50001 DROP VIEW IF EXISTS `rows_by_insert_date`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`ilia`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `rows_by_insert_date` AS select cast(`rental`.`technical_timestamp` as date) AS `insert_date`,(to_days(now()) - to_days(`rental`.`technical_timestamp`)) AS `days_ago`,count(distinct `rental`.`rental_date`) AS `days_generated`,count(0) AS `rowcount` from `rental` group by cast(`rental`.`technical_timestamp` as date) desc */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-30 11:06:14
