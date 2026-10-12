-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: pune_vegetation_db
-- ------------------------------------------------------
-- Server version	8.0.46

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
-- Table structure for table `analysis_runs`
--

DROP TABLE IF EXISTS `analysis_runs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `analysis_runs` (
  `analysis_id` bigint NOT NULL AUTO_INCREMENT,
  `area_id` bigint NOT NULL,
  `dataset_id` bigint NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `max_scene_cloud_pct` decimal(5,2) NOT NULL DEFAULT '20.00',
  `processing_status` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'pending',
  `analysis_mode` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'real_gee',
  `image_count` int NOT NULL DEFAULT '0',
  `composite_method` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'median',
  `error_message` text COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`analysis_id`),
  KEY `fk_runs_dataset` (`dataset_id`),
  KEY `idx_analysis_runs_area` (`area_id`),
  KEY `idx_analysis_runs_status` (`processing_status`),
  KEY `idx_analysis_runs_dates` (`start_date`,`end_date`),
  KEY `idx_analysis_runs_mode` (`analysis_mode`),
  CONSTRAINT `fk_runs_area` FOREIGN KEY (`area_id`) REFERENCES `study_areas` (`area_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_runs_dataset` FOREIGN KEY (`dataset_id`) REFERENCES `satellite_datasets` (`dataset_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `chk_analysis_mode` CHECK ((`analysis_mode` in (_utf8mb4'real_gee',_utf8mb4'demo'))),
  CONSTRAINT `chk_cloud_pct` CHECK (((`max_scene_cloud_pct` >= 0.00) and (`max_scene_cloud_pct` <= 100.00))),
  CONSTRAINT `chk_date_order` CHECK ((`start_date` <= `end_date`)),
  CONSTRAINT `chk_processing_status` CHECK ((`processing_status` in (_utf8mb4'pending',_utf8mb4'running',_utf8mb4'completed',_utf8mb4'failed')))
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `analysis_runs`
--

LOCK TABLES `analysis_runs` WRITE;
/*!40000 ALTER TABLE `analysis_runs` DISABLE KEYS */;
INSERT INTO `analysis_runs` VALUES (1,3,1,'2023-09-01','2023-11-30',20.00,'completed','demo',14,'median',NULL,'2026-10-12 13:34:01'),(2,1,1,'2023-01-01','2023-05-31',15.00,'completed','demo',22,'median',NULL,'2026-10-12 13:34:01'),(3,6,1,'2023-06-01','2023-10-31',25.00,'completed','demo',18,'median',NULL,'2026-10-12 13:34:01'),(4,1,1,'2023-07-01','2023-07-31',15.00,'completed','demo',2,'median',NULL,'2026-10-12 13:44:01'),(5,1,1,'2023-07-01','2023-07-31',15.00,'completed','demo',2,'median',NULL,'2026-10-12 13:44:37'),(6,1,1,'2023-07-01','2023-07-31',15.00,'completed','demo',2,'median',NULL,'2026-10-12 14:02:48'),(7,1,1,'2023-06-01','2023-11-30',20.00,'completed','demo',13,'median',NULL,'2026-10-12 14:03:26'),(8,6,1,'2023-06-01','2023-11-30',20.00,'completed','demo',13,'median',NULL,'2026-10-12 14:11:27'),(9,6,1,'2023-06-01','2023-11-30',20.00,'completed','demo',13,'median',NULL,'2026-10-12 14:11:34'),(10,5,1,'2023-06-01','2023-11-30',20.00,'completed','demo',13,'median',NULL,'2026-10-12 14:13:16'),(11,5,1,'2023-06-01','2023-11-30',20.00,'completed','demo',13,'median',NULL,'2026-10-12 14:13:23'),(12,5,1,'2023-06-01','2023-11-30',20.00,'completed','demo',13,'median',NULL,'2026-10-12 14:13:28'),(13,1,1,'2023-07-01','2023-07-31',15.00,'completed','demo',2,'median',NULL,'2026-10-12 14:20:38'),(14,6,1,'2023-06-01','2023-11-30',20.00,'completed','demo',13,'median',NULL,'2026-10-12 14:27:29'),(15,6,1,'2023-06-01','2023-11-30',20.00,'completed','demo',13,'median',NULL,'2026-10-12 14:27:34'),(16,1,1,'2023-07-01','2023-07-31',15.00,'completed','demo',2,'median',NULL,'2026-10-12 15:03:16'),(17,1,1,'2023-09-01','2023-10-31',25.00,'completed','real_gee',5,'median',NULL,'2026-10-12 15:04:21'),(18,1,1,'2023-07-01','2023-07-31',15.00,'completed','demo',2,'median',NULL,'2026-10-12 15:04:50'),(19,6,1,'2023-06-01','2023-11-30',20.00,'completed','demo',13,'median',NULL,'2026-10-12 15:12:17'),(20,5,1,'2023-06-01','2023-11-30',20.00,'completed','demo',13,'median',NULL,'2026-10-12 15:15:57');
/*!40000 ALTER TABLE `analysis_runs` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `trg_audit_analysis_insert` AFTER INSERT ON `analysis_runs` FOR EACH ROW BEGIN
    INSERT INTO audit_logs (action_type, table_name, record_id, details)
    VALUES (
        'INSERT',
        'analysis_runs',
        NEW.analysis_id,
        CONCAT('Analysis created for Area ID: ', NEW.area_id, ' Mode: ', NEW.analysis_mode, ' Status: ', NEW.processing_status)
    );
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `audit_logs`
--

DROP TABLE IF EXISTS `audit_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `audit_logs` (
  `log_id` bigint NOT NULL AUTO_INCREMENT,
  `action_type` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `table_name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `record_id` bigint DEFAULT NULL,
  `details` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `logged_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`log_id`),
  KEY `idx_audit_table_date` (`table_name`,`logged_at`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `audit_logs`
--

LOCK TABLES `audit_logs` WRITE;
/*!40000 ALTER TABLE `audit_logs` DISABLE KEYS */;
INSERT INTO `audit_logs` VALUES (1,'INSERT','analysis_runs',1,'Analysis created for Area ID: 3 Mode: demo Status: completed','2026-10-12 13:34:01'),(2,'INSERT','analysis_runs',2,'Analysis created for Area ID: 1 Mode: demo Status: completed','2026-10-12 13:34:01'),(3,'INSERT','analysis_runs',3,'Analysis created for Area ID: 6 Mode: demo Status: completed','2026-10-12 13:34:01'),(4,'INSERT','analysis_runs',4,'Analysis created for Area ID: 1 Mode: demo Status: completed','2026-10-12 13:44:01'),(5,'INSERT','analysis_runs',5,'Analysis created for Area ID: 1 Mode: demo Status: completed','2026-10-12 13:44:37'),(6,'INSERT','analysis_runs',6,'Analysis created for Area ID: 1 Mode: demo Status: completed','2026-10-12 14:02:48'),(7,'INSERT','analysis_runs',7,'Analysis created for Area ID: 1 Mode: demo Status: completed','2026-10-12 14:03:26'),(8,'INSERT','analysis_runs',8,'Analysis created for Area ID: 6 Mode: demo Status: completed','2026-10-12 14:11:27'),(9,'INSERT','analysis_runs',9,'Analysis created for Area ID: 6 Mode: demo Status: completed','2026-10-12 14:11:34'),(10,'INSERT','analysis_runs',10,'Analysis created for Area ID: 5 Mode: demo Status: completed','2026-10-12 14:13:16'),(11,'INSERT','analysis_runs',11,'Analysis created for Area ID: 5 Mode: demo Status: completed','2026-10-12 14:13:23'),(12,'INSERT','analysis_runs',12,'Analysis created for Area ID: 5 Mode: demo Status: completed','2026-10-12 14:13:28'),(13,'INSERT','analysis_runs',13,'Analysis created for Area ID: 1 Mode: demo Status: completed','2026-10-12 14:20:38'),(14,'INSERT','analysis_runs',14,'Analysis created for Area ID: 6 Mode: demo Status: completed','2026-10-12 14:27:29'),(15,'INSERT','analysis_runs',15,'Analysis created for Area ID: 6 Mode: demo Status: completed','2026-10-12 14:27:34'),(16,'INSERT','analysis_runs',16,'Analysis created for Area ID: 1 Mode: demo Status: completed','2026-10-12 15:03:16'),(17,'INSERT','analysis_runs',17,'Analysis created for Area ID: 1 Mode: real_gee Status: completed','2026-10-12 15:04:21'),(18,'INSERT','analysis_runs',18,'Analysis created for Area ID: 1 Mode: demo Status: completed','2026-10-12 15:04:50'),(19,'INSERT','analysis_runs',19,'Analysis created for Area ID: 6 Mode: demo Status: completed','2026-10-12 15:12:17'),(20,'INSERT','analysis_runs',20,'Analysis created for Area ID: 5 Mode: demo Status: completed','2026-10-12 15:15:57');
/*!40000 ALTER TABLE `audit_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ndvi_summaries`
--

DROP TABLE IF EXISTS `ndvi_summaries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ndvi_summaries` (
  `summary_id` bigint NOT NULL AUTO_INCREMENT,
  `analysis_id` bigint NOT NULL,
  `mean_ndvi` decimal(8,6) DEFAULT NULL,
  `median_ndvi` decimal(8,6) DEFAULT NULL,
  `min_ndvi` decimal(8,6) DEFAULT NULL,
  `max_ndvi` decimal(8,6) DEFAULT NULL,
  `valid_pixel_count` bigint DEFAULT NULL,
  `vegetation_area_sq_km` decimal(12,3) DEFAULT NULL,
  `calculated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`summary_id`),
  KEY `idx_summaries_analysis` (`analysis_id`),
  CONSTRAINT `fk_summaries_analysis` FOREIGN KEY (`analysis_id`) REFERENCES `analysis_runs` (`analysis_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `chk_summary_max` CHECK (((`max_ndvi` is null) or ((`max_ndvi` >= -(1.000000)) and (`max_ndvi` <= 1.000000)))),
  CONSTRAINT `chk_summary_mean` CHECK (((`mean_ndvi` is null) or ((`mean_ndvi` >= -(1.000000)) and (`mean_ndvi` <= 1.000000)))),
  CONSTRAINT `chk_summary_median` CHECK (((`median_ndvi` is null) or ((`median_ndvi` >= -(1.000000)) and (`median_ndvi` <= 1.000000)))),
  CONSTRAINT `chk_summary_min` CHECK (((`min_ndvi` is null) or ((`min_ndvi` >= -(1.000000)) and (`min_ndvi` <= 1.000000))))
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ndvi_summaries`
--

LOCK TABLES `ndvi_summaries` WRITE;
/*!40000 ALTER TABLE `ndvi_summaries` DISABLE KEYS */;
INSERT INTO `ndvi_summaries` VALUES (1,1,0.684200,0.712000,0.125000,0.892000,4850000,524.350,'2026-10-12 13:34:01'),(2,2,0.312000,0.298000,-0.082000,0.645000,2100000,68.200,'2026-10-12 13:34:01'),(3,3,0.542000,0.568000,0.040000,0.812000,6200000,480.100,'2026-10-12 13:34:01'),(4,4,0.582000,0.591000,0.120000,0.810000,500000,42.500,'2026-10-12 13:44:01'),(5,5,0.582000,0.591000,0.120000,0.810000,500000,42.500,'2026-10-12 13:44:37'),(6,6,0.582000,0.591000,0.120000,0.810000,500000,42.500,'2026-10-12 14:02:48'),(7,7,0.500101,0.550091,0.221363,0.599718,13,211.538,'2026-10-12 14:03:26'),(8,8,0.500101,0.550091,0.221363,0.599718,13,685.385,'2026-10-12 14:11:27'),(9,9,0.500101,0.550091,0.221363,0.599718,13,685.385,'2026-10-12 14:11:34'),(10,10,0.500101,0.550091,0.221363,0.599718,13,583.846,'2026-10-12 14:13:16'),(11,11,0.500101,0.550091,0.221363,0.599718,13,583.846,'2026-10-12 14:13:23'),(12,12,0.500101,0.550091,0.221363,0.599718,13,583.846,'2026-10-12 14:13:28'),(13,13,0.582000,0.591000,0.120000,0.810000,500000,42.500,'2026-10-12 14:20:38'),(14,14,0.500101,0.550091,0.221363,0.599718,13,685.385,'2026-10-12 14:27:29'),(15,15,0.500101,0.550091,0.221363,0.599718,13,685.385,'2026-10-12 14:27:34'),(16,16,0.582000,0.591000,0.120000,0.810000,500000,42.500,'2026-10-12 15:03:16'),(17,17,0.430113,0.433577,-0.461500,0.884478,1044220,NULL,'2026-10-12 15:04:21'),(18,18,0.582000,0.591000,0.120000,0.810000,500000,42.500,'2026-10-12 15:04:50'),(19,19,0.500101,0.550091,0.221363,0.599718,13,685.385,'2026-10-12 15:12:17'),(20,20,0.500101,0.550091,0.221363,0.599718,13,583.846,'2026-10-12 15:15:57');
/*!40000 ALTER TABLE `ndvi_summaries` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ndvi_time_series`
--

DROP TABLE IF EXISTS `ndvi_time_series`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ndvi_time_series` (
  `point_id` bigint NOT NULL AUTO_INCREMENT,
  `analysis_id` bigint NOT NULL,
  `observation_date` date NOT NULL,
  `mean_ndvi` decimal(8,6) NOT NULL,
  `median_ndvi` decimal(8,6) DEFAULT NULL,
  `image_count` int NOT NULL DEFAULT '1',
  `quality_notes` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`point_id`),
  UNIQUE KEY `uq_analysis_obs_date` (`analysis_id`,`observation_date`),
  KEY `idx_time_series_analysis_date` (`analysis_id`,`observation_date`),
  CONSTRAINT `fk_time_series_analysis` FOREIGN KEY (`analysis_id`) REFERENCES `analysis_runs` (`analysis_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `chk_ts_mean` CHECK (((`mean_ndvi` >= -(1.000000)) and (`mean_ndvi` <= 1.000000))),
  CONSTRAINT `chk_ts_median` CHECK (((`median_ndvi` is null) or ((`median_ndvi` >= -(1.000000)) and (`median_ndvi` <= 1.000000))))
) ENGINE=InnoDB AUTO_INCREMENT=164 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ndvi_time_series`
--

LOCK TABLES `ndvi_time_series` WRITE;
/*!40000 ALTER TABLE `ndvi_time_series` DISABLE KEYS */;
INSERT INTO `ndvi_time_series` VALUES (1,1,'2023-09-05',0.621000,0.645000,1,'DEMO DATA — Clear sky post-monsoon sample'),(2,1,'2023-09-20',0.665000,0.690000,1,'DEMO DATA — Vigorous foliage peak'),(3,1,'2023-10-05',0.710000,0.735000,1,'DEMO DATA — Maximum canopy density'),(4,1,'2023-10-25',0.698000,0.720000,1,'DEMO DATA — Stable vegetative cover'),(5,1,'2023-11-12',0.672000,0.701000,1,'DEMO DATA — Transition into early dry season'),(6,1,'2023-11-28',0.640000,0.665000,1,'DEMO DATA — Post-monsoon drying trend'),(7,2,'2023-01-15',0.385000,0.370000,1,'DEMO DATA — Moderate urban green cover (Winter)'),(8,2,'2023-02-14',0.342000,0.330000,1,'DEMO DATA — Gradual drying trend'),(9,2,'2023-03-15',0.298000,0.285000,1,'DEMO DATA — Pre-monsoon dry season bare patches'),(10,2,'2023-04-12',0.265000,0.252000,1,'DEMO DATA — Summer heat peak low vegetation'),(11,2,'2023-05-20',0.245000,0.231000,1,'DEMO DATA — Lowest annual baseline before monsoon'),(12,3,'2023-06-15',0.280000,0.270000,1,'DEMO DATA — Sowing season preparation'),(13,3,'2023-07-20',0.420000,0.435000,1,'DEMO DATA — Crop germination and early vegetative phase'),(14,3,'2023-08-25',0.585000,0.610000,1,'DEMO DATA — Peak sugarcane and kharif crop canopy'),(15,3,'2023-09-28',0.640000,0.670000,1,'DEMO DATA — Maturing crops with high chlorophyll'),(16,3,'2023-10-25',0.535000,0.550000,1,'DEMO DATA — Early harvest cycle starts'),(17,4,'2023-07-10',0.550000,0.560000,1,'Integration test point 1'),(18,4,'2023-07-25',0.614000,0.622000,1,'Integration test point 2'),(19,5,'2023-07-10',0.550000,0.560000,1,'Integration test point 1'),(20,5,'2023-07-25',0.614000,0.622000,1,'Integration test point 2'),(21,6,'2023-07-10',0.550000,0.560000,1,'Integration test point 1'),(22,6,'2023-07-25',0.614000,0.622000,1,'Integration test point 2'),(23,7,'2023-06-01',0.255244,0.257796,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(24,7,'2023-06-16',0.221363,0.223577,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(25,7,'2023-07-01',0.595244,0.601196,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(26,7,'2023-07-16',0.561363,0.566977,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(27,7,'2023-07-31',0.557879,0.563458,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(28,7,'2023-08-15',0.589509,0.595404,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(29,7,'2023-08-30',0.540359,0.545763,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(30,7,'2023-09-14',0.599718,0.605715,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(31,7,'2023-09-29',0.550091,0.555592,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(32,7,'2023-10-14',0.599718,0.605715,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(33,7,'2023-10-29',0.550091,0.555592,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(34,7,'2023-11-13',0.442605,0.447031,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(35,7,'2023-11-28',0.438127,0.442508,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(36,8,'2023-06-01',0.255244,0.257796,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(37,8,'2023-06-16',0.221363,0.223577,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(38,8,'2023-07-01',0.595244,0.601196,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(39,8,'2023-07-16',0.561363,0.566977,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(40,8,'2023-07-31',0.557879,0.563458,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(41,8,'2023-08-15',0.589509,0.595404,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(42,8,'2023-08-30',0.540359,0.545763,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(43,8,'2023-09-14',0.599718,0.605715,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(44,8,'2023-09-29',0.550091,0.555592,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(45,8,'2023-10-14',0.599718,0.605715,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(46,8,'2023-10-29',0.550091,0.555592,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(47,8,'2023-11-13',0.442605,0.447031,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(48,8,'2023-11-28',0.438127,0.442508,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(49,9,'2023-06-01',0.255244,0.257796,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(50,9,'2023-06-16',0.221363,0.223577,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(51,9,'2023-07-01',0.595244,0.601196,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(52,9,'2023-07-16',0.561363,0.566977,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(53,9,'2023-07-31',0.557879,0.563458,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(54,9,'2023-08-15',0.589509,0.595404,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(55,9,'2023-08-30',0.540359,0.545763,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(56,9,'2023-09-14',0.599718,0.605715,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(57,9,'2023-09-29',0.550091,0.555592,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(58,9,'2023-10-14',0.599718,0.605715,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(59,9,'2023-10-29',0.550091,0.555592,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(60,9,'2023-11-13',0.442605,0.447031,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(61,9,'2023-11-28',0.438127,0.442508,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(62,10,'2023-06-01',0.255244,0.257796,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(63,10,'2023-06-16',0.221363,0.223577,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(64,10,'2023-07-01',0.595244,0.601196,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(65,10,'2023-07-16',0.561363,0.566977,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(66,10,'2023-07-31',0.557879,0.563458,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(67,10,'2023-08-15',0.589509,0.595404,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(68,10,'2023-08-30',0.540359,0.545763,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(69,10,'2023-09-14',0.599718,0.605715,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(70,10,'2023-09-29',0.550091,0.555592,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(71,10,'2023-10-14',0.599718,0.605715,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(72,10,'2023-10-29',0.550091,0.555592,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(73,10,'2023-11-13',0.442605,0.447031,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(74,10,'2023-11-28',0.438127,0.442508,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(75,11,'2023-06-01',0.255244,0.257796,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(76,11,'2023-06-16',0.221363,0.223577,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(77,11,'2023-07-01',0.595244,0.601196,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(78,11,'2023-07-16',0.561363,0.566977,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(79,11,'2023-07-31',0.557879,0.563458,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(80,11,'2023-08-15',0.589509,0.595404,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(81,11,'2023-08-30',0.540359,0.545763,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(82,11,'2023-09-14',0.599718,0.605715,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(83,11,'2023-09-29',0.550091,0.555592,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(84,11,'2023-10-14',0.599718,0.605715,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(85,11,'2023-10-29',0.550091,0.555592,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(86,11,'2023-11-13',0.442605,0.447031,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(87,11,'2023-11-28',0.438127,0.442508,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(88,12,'2023-06-01',0.255244,0.257796,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(89,12,'2023-06-16',0.221363,0.223577,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(90,12,'2023-07-01',0.595244,0.601196,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(91,12,'2023-07-16',0.561363,0.566977,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(92,12,'2023-07-31',0.557879,0.563458,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(93,12,'2023-08-15',0.589509,0.595404,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(94,12,'2023-08-30',0.540359,0.545763,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(95,12,'2023-09-14',0.599718,0.605715,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(96,12,'2023-09-29',0.550091,0.555592,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(97,12,'2023-10-14',0.599718,0.605715,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(98,12,'2023-10-29',0.550091,0.555592,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(99,12,'2023-11-13',0.442605,0.447031,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(100,12,'2023-11-28',0.438127,0.442508,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(101,13,'2023-07-10',0.550000,0.560000,1,'Integration test point 1'),(102,13,'2023-07-25',0.614000,0.622000,1,'Integration test point 2'),(103,14,'2023-06-01',0.255244,0.257796,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(104,14,'2023-06-16',0.221363,0.223577,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(105,14,'2023-07-01',0.595244,0.601196,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(106,14,'2023-07-16',0.561363,0.566977,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(107,14,'2023-07-31',0.557879,0.563458,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(108,14,'2023-08-15',0.589509,0.595404,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(109,14,'2023-08-30',0.540359,0.545763,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(110,14,'2023-09-14',0.599718,0.605715,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(111,14,'2023-09-29',0.550091,0.555592,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(112,14,'2023-10-14',0.599718,0.605715,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(113,14,'2023-10-29',0.550091,0.555592,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(114,14,'2023-11-13',0.442605,0.447031,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(115,14,'2023-11-28',0.438127,0.442508,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(116,15,'2023-06-01',0.255244,0.257796,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(117,15,'2023-06-16',0.221363,0.223577,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(118,15,'2023-07-01',0.595244,0.601196,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(119,15,'2023-07-16',0.561363,0.566977,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(120,15,'2023-07-31',0.557879,0.563458,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(121,15,'2023-08-15',0.589509,0.595404,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(122,15,'2023-08-30',0.540359,0.545763,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(123,15,'2023-09-14',0.599718,0.605715,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(124,15,'2023-09-29',0.550091,0.555592,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(125,15,'2023-10-14',0.599718,0.605715,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(126,15,'2023-10-29',0.550091,0.555592,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(127,15,'2023-11-13',0.442605,0.447031,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(128,15,'2023-11-28',0.438127,0.442508,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(129,16,'2023-07-10',0.550000,0.560000,1,'Integration test point 1'),(130,16,'2023-07-25',0.614000,0.622000,1,'Integration test point 2'),(131,17,'2023-10-06',0.486733,0.486733,1,'Sentinel-2 L2A Surface Reflectance'),(132,17,'2023-10-11',0.468531,0.468531,1,'Sentinel-2 L2A Surface Reflectance'),(133,17,'2023-10-16',0.374965,0.374965,1,'Sentinel-2 L2A Surface Reflectance'),(134,17,'2023-10-21',0.394430,0.394430,1,'Sentinel-2 L2A Surface Reflectance'),(135,17,'2023-10-26',0.417953,0.417953,1,'Sentinel-2 L2A Surface Reflectance'),(136,18,'2023-07-10',0.550000,0.560000,1,'Integration test point 1'),(137,18,'2023-07-25',0.614000,0.622000,1,'Integration test point 2'),(138,19,'2023-06-01',0.255244,0.257796,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(139,19,'2023-06-16',0.221363,0.223577,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(140,19,'2023-07-01',0.595244,0.601196,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(141,19,'2023-07-16',0.561363,0.566977,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(142,19,'2023-07-31',0.557879,0.563458,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(143,19,'2023-08-15',0.589509,0.595404,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(144,19,'2023-08-30',0.540359,0.545763,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(145,19,'2023-09-14',0.599718,0.605715,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(146,19,'2023-09-29',0.550091,0.555592,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(147,19,'2023-10-14',0.599718,0.605715,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(148,19,'2023-10-29',0.550091,0.555592,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(149,19,'2023-11-13',0.442605,0.447031,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(150,19,'2023-11-28',0.438127,0.442508,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(151,20,'2023-06-01',0.255244,0.257796,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(152,20,'2023-06-16',0.221363,0.223577,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(153,20,'2023-07-01',0.595244,0.601196,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(154,20,'2023-07-16',0.561363,0.566977,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(155,20,'2023-07-31',0.557879,0.563458,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(156,20,'2023-08-15',0.589509,0.595404,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(157,20,'2023-08-30',0.540359,0.545763,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(158,20,'2023-09-14',0.599718,0.605715,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(159,20,'2023-09-29',0.550091,0.555592,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(160,20,'2023-10-14',0.599718,0.605715,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(161,20,'2023-10-29',0.550091,0.555592,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(162,20,'2023-11-13',0.442605,0.447031,1,'DEMO DATA — NOT REAL SATELLITE RESULTS'),(163,20,'2023-11-28',0.438127,0.442508,1,'DEMO DATA — NOT REAL SATELLITE RESULTS');
/*!40000 ALTER TABLE `ndvi_time_series` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `satellite_datasets`
--

DROP TABLE IF EXISTS `satellite_datasets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `satellite_datasets` (
  `dataset_id` bigint NOT NULL AUTO_INCREMENT,
  `provider` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'Google Earth Engine',
  `collection_id` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `satellite_name` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'Sentinel-2',
  `sensor` varchar(80) COLLATE utf8mb4_unicode_ci DEFAULT 'MSI',
  `band_nir` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'B8',
  `band_red` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'B4',
  `processing_notes` text COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`dataset_id`),
  UNIQUE KEY `collection_id` (`collection_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `satellite_datasets`
--

LOCK TABLES `satellite_datasets` WRITE;
/*!40000 ALTER TABLE `satellite_datasets` DISABLE KEYS */;
INSERT INTO `satellite_datasets` VALUES (1,'Google Earth Engine','COPERNICUS/S2_SR_HARMONIZED','Sentinel-2','MSI','B8','B4','Surface Reflectance Harmonized collection. B8 (NIR 842nm, 10m) and B4 (Red 665nm, 10m). Cloud masking via SCL QA bands.','2026-10-12 13:34:01');
/*!40000 ALTER TABLE `satellite_datasets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `study_areas`
--

DROP TABLE IF EXISTS `study_areas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `study_areas` (
  `area_id` bigint NOT NULL AUTO_INCREMENT,
  `area_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `area_type` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'preset',
  `region_label` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `geometry_geojson` json NOT NULL,
  `centroid_lat` decimal(10,7) DEFAULT NULL,
  `centroid_lon` decimal(10,7) DEFAULT NULL,
  `area_sq_km` decimal(12,3) DEFAULT NULL,
  `boundary_source` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`area_id`),
  KEY `idx_study_areas_type` (`area_type`),
  KEY `idx_study_areas_region` (`region_label`),
  CONSTRAINT `chk_area_type` CHECK ((`area_type` in (_utf8mb4'preset',_utf8mb4'custom',_utf8mb4'administrative')))
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `study_areas`
--

LOCK TABLES `study_areas` WRITE;
/*!40000 ALTER TABLE `study_areas` DISABLE KEYS */;
INSERT INTO `study_areas` VALUES (1,'Pune City / Urban Core','preset','Pune Urban','{\"type\": \"Polygon\", \"coordinates\": [[[73.738, 18.532], [73.755, 18.571], [73.782, 18.598], [73.821, 18.615], [73.874, 18.608], [73.921, 18.585], [73.962, 18.552], [73.985, 18.514], [73.972, 18.475], [73.945, 18.441], [73.905, 18.423], [73.861, 18.432], [73.818, 18.448], [73.774, 18.462], [73.742, 18.495], [73.738, 18.532]]]}',18.5204300,73.8567440,250.000,'Approximate study-area bounding polygon for Pune DBMS demonstration','2026-10-12 13:34:01'),(2,'Haveli Area','preset','Haveli','{\"type\": \"Polygon\", \"coordinates\": [[[73.75, 18.35], [74.05, 18.35], [74.05, 18.6], [73.75, 18.6], [73.75, 18.35]]]}',18.4800000,73.9100000,580.000,'Approximate study-area bounding polygon for Pune DBMS demonstration','2026-10-12 13:34:01'),(3,'Mulshi Area','preset','Mulshi','{\"type\": \"Polygon\", \"coordinates\": [[[73.351, 18.412], [73.385, 18.462], [73.412, 18.524], [73.456, 18.588], [73.518, 18.632], [73.582, 18.648], [73.645, 18.618], [73.678, 18.562], [73.652, 18.495], [73.612, 18.435], [73.551, 18.392], [73.482, 18.368], [73.415, 18.375], [73.351, 18.412]]]}',18.5100000,73.5100000,620.000,'Approximate study-area bounding polygon for Pune DBMS demonstration','2026-10-12 13:34:01'),(4,'Maval Area','preset','Maval','{\"type\": \"Polygon\", \"coordinates\": [[[73.45, 18.65], [73.75, 18.65], [73.75, 18.88], [73.45, 18.88], [73.45, 18.65]]]}',18.7500000,73.5800000,540.000,'Approximate study-area bounding polygon for Pune DBMS demonstration','2026-10-12 13:34:01'),(5,'Bhor Area','preset','Bhor','{\"type\": \"Polygon\", \"coordinates\": [[[73.7, 18.02], [74.0, 18.02], [74.0, 18.3], [73.7, 18.3], [73.7, 18.02]]]}',18.1500000,73.8400000,690.000,'Approximate study-area bounding polygon for Pune DBMS demonstration','2026-10-12 13:34:01'),(6,'Baramati Area','preset','Baramati','{\"type\": \"Polygon\", \"coordinates\": [[[74.4, 18.0], [74.78, 18.0], [74.78, 18.3], [74.4, 18.3], [74.4, 18.0]]]}',18.1500000,74.5800000,810.000,'Approximate study-area bounding polygon for Pune DBMS demonstration','2026-10-12 13:34:01'),(7,'Shirur Area','preset','Shirur','{\"type\": \"Polygon\", \"coordinates\": [[[74.2, 18.68], [74.55, 18.68], [74.55, 18.98], [74.2, 18.98], [74.2, 18.68]]]}',18.8200000,74.3700000,750.000,'Approximate study-area bounding polygon for Pune DBMS demonstration','2026-10-12 13:34:01'),(8,'Daund Area','preset','Daund','{\"type\": \"Polygon\", \"coordinates\": [[[74.42, 18.32], [74.76, 18.32], [74.76, 18.62], [74.42, 18.62], [74.42, 18.32]]]}',18.4600000,74.5800000,720.000,'Approximate study-area bounding polygon for Pune DBMS demonstration','2026-10-12 13:34:01'),(9,'Test Automation Zone','custom','Pune Test','{\"type\": \"Polygon\", \"coordinates\": [[[73.81, 18.51], [73.89, 18.51], [73.89, 18.59], [73.81, 18.59], [73.81, 18.51]]]}',18.5500000,73.8500000,65.200,'Pytest Test Suite','2026-10-12 13:44:00'),(10,'Test Automation Zone','custom','Pune Test','{\"type\": \"Polygon\", \"coordinates\": [[[73.81, 18.51], [73.89, 18.51], [73.89, 18.59], [73.81, 18.59], [73.81, 18.51]]]}',18.5500000,73.8500000,65.200,'Pytest Test Suite','2026-10-12 13:44:37'),(11,'Test Automation Zone','custom','Pune Test','{\"type\": \"Polygon\", \"coordinates\": [[[73.81, 18.51], [73.89, 18.51], [73.89, 18.59], [73.81, 18.59], [73.81, 18.51]]]}',18.5500000,73.8500000,65.200,'Pytest Test Suite','2026-10-12 14:02:48'),(12,'Test Automation Zone','custom','Pune Test','{\"type\": \"Polygon\", \"coordinates\": [[[73.81, 18.51], [73.89, 18.51], [73.89, 18.59], [73.81, 18.59], [73.81, 18.51]]]}',18.5500000,73.8500000,65.200,'Pytest Test Suite','2026-10-12 14:20:38'),(13,'Test Automation Zone','custom','Pune Test','{\"type\": \"Polygon\", \"coordinates\": [[[73.81, 18.51], [73.89, 18.51], [73.89, 18.59], [73.81, 18.59], [73.81, 18.51]]]}',18.5500000,73.8500000,65.200,'Pytest Test Suite','2026-10-12 15:03:16'),(14,'Test Automation Zone','custom','Pune Test','{\"type\": \"Polygon\", \"coordinates\": [[[73.81, 18.51], [73.89, 18.51], [73.89, 18.59], [73.81, 18.59], [73.81, 18.51]]]}',18.5500000,73.8500000,65.200,'Pytest Test Suite','2026-10-12 15:04:50');
/*!40000 ALTER TABLE `study_areas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` bigint NOT NULL AUTO_INCREMENT,
  `full_name` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `role` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'analyst',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`),
  CONSTRAINT `chk_user_role` CHECK ((`role` in (_utf8mb4'admin',_utf8mb4'analyst',_utf8mb4'researcher',_utf8mb4'viewer')))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Pune Geoinformatics Analyst','analyst@puneveg.org','analyst','2026-10-12 13:34:01'),(2,'DBMS Course Examiner','examiner@college.edu','admin','2026-10-12 13:34:01');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `v_analysis_complete_summary`
--

DROP TABLE IF EXISTS `v_analysis_complete_summary`;
/*!50001 DROP VIEW IF EXISTS `v_analysis_complete_summary`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_analysis_complete_summary` AS SELECT 
 1 AS `analysis_id`,
 1 AS `area_name`,
 1 AS `region_label`,
 1 AS `area_type`,
 1 AS `area_sq_km`,
 1 AS `satellite_name`,
 1 AS `collection_id`,
 1 AS `start_date`,
 1 AS `end_date`,
 1 AS `max_scene_cloud_pct`,
 1 AS `processing_status`,
 1 AS `analysis_mode`,
 1 AS `image_count`,
 1 AS `composite_method`,
 1 AS `mean_ndvi`,
 1 AS `median_ndvi`,
 1 AS `min_ndvi`,
 1 AS `max_ndvi`,
 1 AS `valid_pixel_count`,
 1 AS `vegetation_area_sq_km`,
 1 AS `analysis_created_at`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `v_area_performance_summary`
--

DROP TABLE IF EXISTS `v_area_performance_summary`;
/*!50001 DROP VIEW IF EXISTS `v_area_performance_summary`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_area_performance_summary` AS SELECT 
 1 AS `area_id`,
 1 AS `area_name`,
 1 AS `region_label`,
 1 AS `area_type`,
 1 AS `area_sq_km`,
 1 AS `total_analyses`,
 1 AS `overall_avg_mean_ndvi`,
 1 AS `lowest_recorded_ndvi`,
 1 AS `highest_recorded_ndvi`,
 1 AS `latest_analysis_date`*/;
SET character_set_client = @saved_cs_client;

--
-- Dumping routines for database 'pune_vegetation_db'
--

--
-- Final view structure for view `v_analysis_complete_summary`
--

/*!50001 DROP VIEW IF EXISTS `v_analysis_complete_summary`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_analysis_complete_summary` AS select `ar`.`analysis_id` AS `analysis_id`,`sa`.`area_name` AS `area_name`,`sa`.`region_label` AS `region_label`,`sa`.`area_type` AS `area_type`,`sa`.`area_sq_km` AS `area_sq_km`,`sd`.`satellite_name` AS `satellite_name`,`sd`.`collection_id` AS `collection_id`,`ar`.`start_date` AS `start_date`,`ar`.`end_date` AS `end_date`,`ar`.`max_scene_cloud_pct` AS `max_scene_cloud_pct`,`ar`.`processing_status` AS `processing_status`,`ar`.`analysis_mode` AS `analysis_mode`,`ar`.`image_count` AS `image_count`,`ar`.`composite_method` AS `composite_method`,`ns`.`mean_ndvi` AS `mean_ndvi`,`ns`.`median_ndvi` AS `median_ndvi`,`ns`.`min_ndvi` AS `min_ndvi`,`ns`.`max_ndvi` AS `max_ndvi`,`ns`.`valid_pixel_count` AS `valid_pixel_count`,`ns`.`vegetation_area_sq_km` AS `vegetation_area_sq_km`,`ar`.`created_at` AS `analysis_created_at` from (((`analysis_runs` `ar` join `study_areas` `sa` on((`ar`.`area_id` = `sa`.`area_id`))) join `satellite_datasets` `sd` on((`ar`.`dataset_id` = `sd`.`dataset_id`))) left join `ndvi_summaries` `ns` on((`ar`.`analysis_id` = `ns`.`analysis_id`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_area_performance_summary`
--

/*!50001 DROP VIEW IF EXISTS `v_area_performance_summary`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_area_performance_summary` AS select `sa`.`area_id` AS `area_id`,`sa`.`area_name` AS `area_name`,`sa`.`region_label` AS `region_label`,`sa`.`area_type` AS `area_type`,`sa`.`area_sq_km` AS `area_sq_km`,count(`ar`.`analysis_id`) AS `total_analyses`,round(avg(`ns`.`mean_ndvi`),4) AS `overall_avg_mean_ndvi`,round(min(`ns`.`min_ndvi`),4) AS `lowest_recorded_ndvi`,round(max(`ns`.`max_ndvi`),4) AS `highest_recorded_ndvi`,max(`ar`.`created_at`) AS `latest_analysis_date` from ((`study_areas` `sa` left join `analysis_runs` `ar` on(((`sa`.`area_id` = `ar`.`area_id`) and (`ar`.`processing_status` = 'completed')))) left join `ndvi_summaries` `ns` on((`ar`.`analysis_id` = `ns`.`analysis_id`))) group by `sa`.`area_id`,`sa`.`area_name`,`sa`.`region_label`,`sa`.`area_type`,`sa`.`area_sq_km` */;
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

-- Dump completed on 2026-10-12 21:51:06
