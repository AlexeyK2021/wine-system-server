-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: 192.168.1.113    Database: IusDb4
-- ------------------------------------------------------
-- Server version	5.5.5-10.6.16-MariaDB-0ubuntu0.22.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `actuator`
--

DROP TABLE IF EXISTS `actuator`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `actuator` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `model` varchar(128) DEFAULT NULL,
  `type_id` int(11) NOT NULL,
  `tank_id` int(11) NOT NULL,
  `ip` varchar(15) NOT NULL,
  `port` int(11) NOT NULL,
  `state_node_id` varchar(128) NOT NULL,
  `cmnd_node_id` varchar(128) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `actuator_actuator_type_FK` (`type_id`),
  KEY `actuator_tank_FK` (`tank_id`),
  CONSTRAINT `actuator_actuator_type_FK` FOREIGN KEY (`type_id`) REFERENCES `actuator_type` (`id`),
  CONSTRAINT `actuator_tank_FK` FOREIGN KEY (`tank_id`) REFERENCES `tank` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `actuator`
--

LOCK TABLES `actuator` WRITE;
/*!40000 ALTER TABLE `actuator` DISABLE KEYS */;
INSERT INTO `actuator` VALUES (1,'Впускной клапан',NULL,2,1,'127.0.0.1',4841,'ns=2;i=20','ns=2;i=21'),(2,'Впускной клапан теплообмена',NULL,8,1,'127.0.0.1',4841,'ns=2;i=30','ns=2;i=31'),(3,'Выпускной клапан теплообмена',NULL,3,1,'127.0.0.1',4841,'ns=2;i=32','ns=2;i=33'),(4,'Клапан угл.газа',NULL,4,1,'127.0.0.1',4841,'ns=2;i=28','ns=2;i=29'),(5,'Выпускной клапан',NULL,5,1,'127.0.0.1',4841,'ns=2;i=26','ns=2;i=27'),(6,'Насос теплообмена',NULL,6,1,'127.0.0.1',4841,'ns=2;i=24','ns=2;i=25'),(7,'Сливной насос',NULL,7,1,'127.0.0.1',4841,'ns=2;i=22','ns=2;i=23');
/*!40000 ALTER TABLE `actuator` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `actuator_type`
--

DROP TABLE IF EXISTS `actuator_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `actuator_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `actuator_type`
--

LOCK TABLES `actuator_type` WRITE;
/*!40000 ALTER TABLE `actuator_type` DISABLE KEYS */;
INSERT INTO `actuator_type` VALUES (2,'Впускной клапан',NULL),(3,'Выпускной клапан теплообменника',NULL),(4,'Выпускной клапан угл.газ',NULL),(5,'Выпускной клапан',NULL),(6,'Насос теплообменника',NULL),(7,'Сливной насос',NULL),(8,'Впускной клапан теплообменника',NULL);
/*!40000 ALTER TABLE `actuator_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `param_type`
--

DROP TABLE IF EXISTS `param_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `param_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `param_type`
--

LOCK TABLES `param_type` WRITE;
/*!40000 ALTER TABLE `param_type` DISABLE KEYS */;
INSERT INTO `param_type` VALUES (1,'Температура',NULL),(2,'Давление',NULL);
/*!40000 ALTER TABLE `param_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `parameter`
--

DROP TABLE IF EXISTS `parameter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `parameter` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `min_value` float NOT NULL,
  `max_value` float NOT NULL,
  `type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `parameter_param_type_FK` (`type_id`),
  CONSTRAINT `parameter_param_type_FK` FOREIGN KEY (`type_id`) REFERENCES `param_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parameter`
--

LOCK TABLES `parameter` WRITE;
/*!40000 ALTER TABLE `parameter` DISABLE KEYS */;
INSERT INTO `parameter` VALUES (1,'Температура бурного брожения',18,24,1),(2,'Давление бурного брожения',95,105,2);
/*!40000 ALTER TABLE `parameter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `process`
--

DROP TABLE IF EXISTS `process`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `process` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  `execution_time` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `process`
--

LOCK TABLES `process` WRITE;
/*!40000 ALTER TABLE `process` DISABLE KEYS */;
INSERT INTO `process` VALUES (1,'Инициализация танка',NULL,NULL),(3,'Забраживание',NULL,72000),(4,'Бурное брожение',NULL,864000),(7,'Тихое брожение',NULL,2592000),(9,'Ожидание введения в эксплуатацию',NULL,NULL),(11,'Наполнение танка',NULL,NULL),(12,'Опорожнение танка',NULL,NULL);
/*!40000 ALTER TABLE `process` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `process_log`
--

DROP TABLE IF EXISTS `process_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `process_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `start` datetime NOT NULL DEFAULT current_timestamp(),
  `end` datetime DEFAULT NULL,
  `description` varchar(256) DEFAULT NULL,
  `tank_id` int(11) NOT NULL,
  `result_id` int(11) DEFAULT NULL,
  `process_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `process_log_tank_FK` (`tank_id`),
  KEY `process_log_result_code_FK` (`result_id`),
  KEY `process_log_process_FK` (`process_id`),
  CONSTRAINT `process_log_process_FK` FOREIGN KEY (`process_id`) REFERENCES `process` (`id`),
  CONSTRAINT `process_log_result_code_FK` FOREIGN KEY (`result_id`) REFERENCES `result_code` (`id`),
  CONSTRAINT `process_log_tank_FK` FOREIGN KEY (`tank_id`) REFERENCES `tank` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=106 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `process_log`
--

LOCK TABLES `process_log` WRITE;
/*!40000 ALTER TABLE `process_log` DISABLE KEYS */;
INSERT INTO `process_log` VALUES (100,'2024-05-09 09:50:56',NULL,NULL,1,NULL,9);
/*!40000 ALTER TABLE `process_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `result_code`
--

DROP TABLE IF EXISTS `result_code`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `result_code` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `result_code`
--

LOCK TABLES `result_code` WRITE;
/*!40000 ALTER TABLE `result_code` DISABLE KEYS */;
INSERT INTO `result_code` VALUES (1,'ОК',NULL),(2,'Экстренная остановка',NULL);
/*!40000 ALTER TABLE `result_code` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sensor`
--

DROP TABLE IF EXISTS `sensor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sensor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `model` varchar(128) DEFAULT NULL,
  `type_id` int(11) NOT NULL,
  `tank_id` int(11) NOT NULL,
  `parameter_id` int(11) DEFAULT NULL,
  `ip` varchar(15) NOT NULL,
  `port` int(11) NOT NULL,
  `node_id` varchar(128) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `sensor_tank_FK` (`tank_id`),
  KEY `sensor_parameter_FK` (`parameter_id`),
  KEY `sensor_sensor_type_FK` (`type_id`),
  CONSTRAINT `sensor_parameter_FK` FOREIGN KEY (`parameter_id`) REFERENCES `parameter` (`id`),
  CONSTRAINT `sensor_sensor_type_FK` FOREIGN KEY (`type_id`) REFERENCES `sensor_type` (`id`),
  CONSTRAINT `sensor_tank_FK` FOREIGN KEY (`tank_id`) REFERENCES `tank` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sensor`
--

LOCK TABLES `sensor` WRITE;
/*!40000 ALTER TABLE `sensor` DISABLE KEYS */;
INSERT INTO `sensor` VALUES (1,'Датчик температуры',NULL,1,1,1,'127.0.0.1',4841,'ns=2;i=13'),(2,'Датчик давления',NULL,2,1,2,'127.0.0.1',4841,'ns=2;i=15'),(3,'Датчик верхнего уровня',NULL,3,1,NULL,'127.0.0.1',4841,'ns=2;i=17'),(4,'Датчик нижнего уровня',NULL,4,1,NULL,'127.0.0.1',4841,'ns=2;i=19');
/*!40000 ALTER TABLE `sensor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sensor_check`
--

DROP TABLE IF EXISTS `sensor_check`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sensor_check` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  `sensor_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `sensor_check_sensor_FK` (`sensor_id`),
  CONSTRAINT `sensor_check_sensor_FK` FOREIGN KEY (`sensor_id`) REFERENCES `sensor` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sensor_check`
--

LOCK TABLES `sensor_check` WRITE;
/*!40000 ALTER TABLE `sensor_check` DISABLE KEYS */;
/*!40000 ALTER TABLE `sensor_check` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sensor_type`
--

DROP TABLE IF EXISTS `sensor_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sensor_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sensor_type`
--

LOCK TABLES `sensor_type` WRITE;
/*!40000 ALTER TABLE `sensor_type` DISABLE KEYS */;
INSERT INTO `sensor_type` VALUES (1,'Датчик температуры',NULL),(2,'Датчик давления',NULL),(3,'Датчик верхнего уровня\r жидкости',NULL),(4,'Датчик нижнего уровня жидкости',NULL);
/*!40000 ALTER TABLE `sensor_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tank`
--

DROP TABLE IF EXISTS `tank`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tank` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tank_tank_type_FK` (`type_id`),
  CONSTRAINT `tank_tank_type_FK` FOREIGN KEY (`type_id`) REFERENCES `tank_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tank`
--

LOCK TABLES `tank` WRITE;
/*!40000 ALTER TABLE `tank` DISABLE KEYS */;
INSERT INTO `tank` VALUES (1,'ББ1',1);
/*!40000 ALTER TABLE `tank` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'IGNORE_SPACE,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`%`*/ /*!50003 TRIGGER add_tank
AFTER INSERT
ON tank FOR EACH ROW
BEGIN
	INSERT INTO process_log(tank_id, process_id) VALUES (NEW.id,9);
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `tank_type`
--

DROP TABLE IF EXISTS `tank_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tank_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tank_type`
--

LOCK TABLES `tank_type` WRITE;
/*!40000 ALTER TABLE `tank_type` DISABLE KEYS */;
INSERT INTO `tank_type` VALUES (1,'Емкость бурного брожения',NULL),(2,'Емкость тихого брожения',NULL);
/*!40000 ALTER TABLE `tank_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `login` varchar(64) NOT NULL,
  `password` varchar(64) NOT NULL,
  `type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_user_type_FK` (`type_id`),
  CONSTRAINT `user_user_type_FK` FOREIGN KEY (`type_id`) REFERENCES `user_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'admin','admin','8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918',1),(3,'alexey','alexey','d217e1716cb7b36f8be65117f625a1e39d22fd585528632391bb74310a4f255d',2),(4,'test','test','03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4',2);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_action`
--

DROP TABLE IF EXISTS `user_action`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_action` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_action`
--

LOCK TABLES `user_action` WRITE;
/*!40000 ALTER TABLE `user_action` DISABLE KEYS */;
INSERT INTO `user_action` VALUES (1,'Успешный вход',NULL),(2,'Неудачная попытка входа',NULL),(3,'Экстренная остановка',NULL),(4,'Изменение состояния',NULL);
/*!40000 ALTER TABLE `user_action` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_log`
--

DROP TABLE IF EXISTS `user_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `datetime` datetime NOT NULL DEFAULT current_timestamp(),
  `description` varchar(256) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `action_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_log_user_FK` (`user_id`),
  KEY `user_log_user_action_FK` (`action_id`),
  CONSTRAINT `user_log_user_FK` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `user_log_user_action_FK` FOREIGN KEY (`action_id`) REFERENCES `user_action` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_log`
--

LOCK TABLES `user_log` WRITE;
/*!40000 ALTER TABLE `user_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_type`
--

DROP TABLE IF EXISTS `user_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  `is_admin` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_type`
--

LOCK TABLES `user_type` WRITE;
/*!40000 ALTER TABLE `user_type` DISABLE KEYS */;
INSERT INTO `user_type` VALUES (1,'Инженер',NULL,1),(2,'Оператор',NULL,0);
/*!40000 ALTER TABLE `user_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'IusDb4'
--
/*!50003 DROP FUNCTION IF EXISTS `check_auth` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'IGNORE_SPACE,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ius`@`%` FUNCTION `check_auth`(login_in VARCHAR(64), passwd_in VARCHAR(64)) RETURNS tinyint(1)
BEGIN

	DECLARE passwd VARCHAR(64);
	DECLARE user_id INT;


	SET passwd = (SELECT password FROM user WHERE login=login_in LIMIT 1);
	SET user_id = (SELECT id FROM user WHERE login=login_in LIMIT 1);

	IF user_id is NULL THEN
		RETURN FALSE;
	END IF;

	IF passwd=passwd_in THEN
		BEGIN
			INSERT INTO user_log(`user_id`, action_id) VALUES (user_id, 1);
			RETURN TRUE;
		END;
	ELSE
		BEGIN
			INSERT INTO user_log(`user_id`, action_id) VALUES (user_id, 2);
			RETURN FALSE;
		END;
	END IF;


	RETURN FALSE;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `get_tank_last_state` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'IGNORE_SPACE,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ius`@`%` PROCEDURE `get_tank_last_state`(IN tankId INT)
BEGIN
	SELECT pl.id, pl.result_id, pl.process_id, p.name FROM process_log AS pl
	JOIN process AS p ON pl.process_id = p.id
	WHERE tank_id = tankId
	ORDER BY pl.id DESC
	LIMIT 1;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-09 15:10:24
