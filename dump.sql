-- MySQL dump 10.13  Distrib 8.0.33, for Linux (x86_64)
--
-- Host: localhost    Database: burrito
-- ------------------------------------------------------
-- Server version       8.0.33

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
-- Table structure for table `actions`
--

DROP TABLE IF EXISTS `actions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `actions` (
  `action_id` int NOT NULL AUTO_INCREMENT,
  `ticket_id` int NOT NULL,
  `user_id` int NOT NULL,
  `action_date` datetime NOT NULL,
  `field_name` varchar(255) NOT NULL,
  `old_value` varchar(255) NOT NULL,
  `new_value` varchar(255) NOT NULL,
  PRIMARY KEY (`action_id`),
  KEY `actions_ticket_id` (`ticket_id`),
  KEY `actions_user_id` (`user_id`),
  CONSTRAINT `actions_ibfk_1` FOREIGN KEY (`ticket_id`) REFERENCES `tickets` (`ticket_id`),
  CONSTRAINT `actions_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `actions`
--

LOCK TABLES `actions` WRITE;
/*!40000 ALTER TABLE `actions` DISABLE KEYS */;
/*!40000 ALTER TABLE `actions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bookmarks`
--

DROP TABLE IF EXISTS `bookmarks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bookmarks` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `ticket_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `bookmarks_user_id` (`user_id`),
  KEY `bookmarks_ticket_id` (`ticket_id`),
  CONSTRAINT `bookmarks_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `bookmarks_ibfk_2` FOREIGN KEY (`ticket_id`) REFERENCES `tickets` (`ticket_id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookmarks`
--

LOCK TABLES `bookmarks` WRITE;
/*!40000 ALTER TABLE `bookmarks` DISABLE KEYS */;
INSERT INTO `bookmarks` VALUES (22,8,30),(23,8,29);
/*!40000 ALTER TABLE `bookmarks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comments`
--

DROP TABLE IF EXISTS `comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comments` (
  `comment_id` int NOT NULL AUTO_INCREMENT,
  `ticket_id` int NOT NULL,
  `author_id` int NOT NULL,
  `comment_date` datetime NOT NULL,
  `body` text NOT NULL,
  PRIMARY KEY (`comment_id`),
  KEY `comments_ticket_id` (`ticket_id`),
  KEY `comments_author_id` (`author_id`),
  CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`ticket_id`) REFERENCES `tickets` (`ticket_id`),
  CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`author_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comments`
--

LOCK TABLES `comments` WRITE;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `deleted`
--

DROP TABLE IF EXISTS `deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `deleted` (
  `user_id` int NOT NULL,
  `ticket_id` int NOT NULL,
  PRIMARY KEY (`user_id`,`ticket_id`),
  KEY `deleted_user_id` (`user_id`),
  KEY `deleted_ticket_id` (`ticket_id`),
  CONSTRAINT `deleted_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `deleted_ibfk_2` FOREIGN KEY (`ticket_id`) REFERENCES `tickets` (`ticket_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `deleted`
--

LOCK TABLES `deleted` WRITE;
/*!40000 ALTER TABLE `deleted` DISABLE KEYS */;
INSERT INTO `deleted` VALUES (7,8),(7,21),(7,23),(7,24),(7,28),(8,4),(8,26),(8,27),(10,18);
/*!40000 ALTER TABLE `deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `faculties`
--

DROP TABLE IF EXISTS `faculties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `faculties` (
  `faculty_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  PRIMARY KEY (`faculty_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faculties`
--

LOCK TABLES `faculties` WRITE;
/*!40000 ALTER TABLE `faculties` DISABLE KEYS */;
INSERT INTO `faculties` VALUES (1,'EliT'),(2,'Biem');
/*!40000 ALTER TABLE `faculties` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `groups`
--

DROP TABLE IF EXISTS `groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `groups` (
  `group_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(10) NOT NULL,
  PRIMARY KEY (`group_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `groups`
--

LOCK TABLES `groups` WRITE;
/*!40000 ALTER TABLE `groups` DISABLE KEYS */;
INSERT INTO `groups` VALUES (1,'IT-11'),(2,'LOL-11'),(3,'KB-01');
/*!40000 ALTER TABLE `groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `liked`
--

DROP TABLE IF EXISTS `liked`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `liked` (
  `user_id` int NOT NULL,
  `ticket_id` int NOT NULL,
  PRIMARY KEY (`user_id`,`ticket_id`),
  KEY `liked_user_id` (`user_id`),
  KEY `liked_ticket_id` (`ticket_id`),
  CONSTRAINT `liked_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `liked_ibfk_2` FOREIGN KEY (`ticket_id`) REFERENCES `tickets` (`ticket_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `liked`
--

LOCK TABLES `liked` WRITE;
/*!40000 ALTER TABLE `liked` DISABLE KEYS */;
INSERT INTO `liked` VALUES (7,1),(7,2),(7,4),(7,5),(7,6),(7,7),(7,14),(7,15),(7,16),(7,17),(7,18),(7,19),(7,24),(7,25),(7,28),(7,29),(8,1),(8,2),(8,7),(8,10),(8,13),(8,15),(8,16),(8,17),(8,18),(8,19),(8,20),(8,25),(9,1),(9,2),(9,5),(9,7),(9,18),(10,2),(10,7),(10,10),(10,15),(10,16),(10,17),(10,18),(10,19),(10,22),(10,25),(10,29);
/*!40000 ALTER TABLE `liked` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notifications`
--

DROP TABLE IF EXISTS `notifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifications` (
  `notification_id` int NOT NULL AUTO_INCREMENT,
  `ticket_id` int NOT NULL,
  `user_id` int NOT NULL,
  `body` text NOT NULL,
  `read` tinyint(1) NOT NULL,
  PRIMARY KEY (`notification_id`),
  KEY `notifications_ticket_id` (`ticket_id`),
  KEY `notifications_user_id` (`user_id`),
  CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`ticket_id`) REFERENCES `tickets` (`ticket_id`),
  CONSTRAINT `notifications_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notifications`
--

LOCK TABLES `notifications` WRITE;
/*!40000 ALTER TABLE `notifications` DISABLE KEYS */;
/*!40000 ALTER TABLE `notifications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `participants`
--

DROP TABLE IF EXISTS `participants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `participants` (
  `user_id` int NOT NULL,
  `ticket_id` int NOT NULL,
  PRIMARY KEY (`user_id`,`ticket_id`),
  KEY `participants_user_id` (`user_id`),
  KEY `participants_ticket_id` (`ticket_id`),
  CONSTRAINT `participants_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `participants_ibfk_2` FOREIGN KEY (`ticket_id`) REFERENCES `tickets` (`ticket_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `participants`
--

LOCK TABLES `participants` WRITE;
/*!40000 ALTER TABLE `participants` DISABLE KEYS */;
/*!40000 ALTER TABLE `participants` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `permissions`
--

DROP TABLE IF EXISTS `permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `permissions` (
  `permission_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  PRIMARY KEY (`permission_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permissions`
--

LOCK TABLES `permissions` WRITE;
/*!40000 ALTER TABLE `permissions` DISABLE KEYS */;
INSERT INTO `permissions` VALUES (1,'UPDATE_PROFILE'),(2,'CREATE_TICKET'),(3,'READ_TICKET'),(4,'SEND_MESSAGE'),(5,'ADMIN'),(6,'GOD_MODE');
/*!40000 ALTER TABLE `permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `queues`
--

DROP TABLE IF EXISTS `queues`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `queues` (
  `queue_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `faculty_id` int NOT NULL,
  `scope` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`queue_id`),
  KEY `queues_faculty_id` (`faculty_id`),
  CONSTRAINT `queues_ibfk_1` FOREIGN KEY (`faculty_id`) REFERENCES `faculties` (`faculty_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `queues`
--

LOCK TABLES `queues` WRITE;
/*!40000 ALTER TABLE `queues` DISABLE KEYS */;
INSERT INTO `queues` VALUES (1,'Lecturers',1,'Reports'),(2,'Food',1,'Reports'),(3,'Academic integrity',2,'Reports'),(4,'Scholarship',2,'Q/A'),(5,'Scholarship',1,'Q/A'),(6,'Food',2,'Q/A'),(7,'Dormitory',1,'Q/A'),(8,'Dormitory',2,'Q/A'),(9,'Dormitory',1,'Reports'),(10,'Dormitory',2,'Reports');
/*!40000 ALTER TABLE `queues` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role_permissions`
--

DROP TABLE IF EXISTS `role_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role_permissions` (
  `role_id` int NOT NULL,
  `permission_id` int NOT NULL,
  KEY `role_permissions_role_id` (`role_id`),
  KEY `role_permissions_permission_id` (`permission_id`),
  CONSTRAINT `role_permissions_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`role_id`) ON DELETE CASCADE,
  CONSTRAINT `role_permissions_ibfk_2` FOREIGN KEY (`permission_id`) REFERENCES `permissions` (`permission_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role_permissions`
--

LOCK TABLES `role_permissions` WRITE;
/*!40000 ALTER TABLE `role_permissions` DISABLE KEYS */;
INSERT INTO `role_permissions` VALUES (1,1),(1,2),(1,1),(1,1),(1,2),(1,3),(1,2),(1,1),(1,3),(1,4),(1,2),(1,3),(1,4),(1,1),(1,1),(1,1),(1,1),(1,1),(2,1),(2,1),(1,4),(1,3),(1,2),(1,2),(1,2),(1,2),(1,2),(2,2),(2,2),(2,1),(1,3),(1,3),(2,3),(1,4),(1,3),(1,3),(1,3),(2,3),(2,2),(2,1),(1,4),(3,1),(1,4),(1,4),(1,4),(1,4),(3,1),(2,3),(2,1),(3,3),(2,1),(2,1),(2,1),(2,1),(2,2),(3,1),(2,2),(3,3),(3,4),(2,2),(2,3),(2,2),(2,2),(2,2),(3,3),(2,3),(3,4),(2,3),(2,3),(3,1),(4,2),(2,3),(2,3),(4,2),(3,1),(3,4),(3,1),(3,1),(3,3),(4,3),(4,3),(3,3),(4,2),(3,1),(3,1),(3,3),(3,3),(4,4),(4,4),(3,3),(3,4),(4,3),(3,3),(3,4),(3,4),(3,4),(5,3),(4,2),(5,3),(4,2),(4,4),(3,4),(3,4),(4,2),(4,2),(4,3),(4,3),(5,4),(5,4),(4,2),(4,3),(4,2),(5,3),(4,3),(4,4),(6,1),(4,4),(4,4),(6,1),(4,4),(4,3),(5,4),(4,3),(5,3),(6,3),(6,3),(4,4),(5,3),(5,3),(6,1),(4,4),(5,3),(5,4),(7,2),(7,2),(5,3),(6,3),(5,4),(7,3),(5,4),(5,4),(5,3),(6,1),(7,3),(5,4),(7,2),(6,3),(6,1),(5,4),(8,3),(6,1),(6,1),(8,3),(9,1),(6,3),(7,2),(6,3),(6,1),(6,3),(7,3),(6,1),(9,1),(9,2),(7,2),(7,2),(7,2),(7,3),(9,2),(6,3),(8,3),(6,3),(9,3),(7,3),(7,3),(8,3),(9,3),(7,3),(7,2),(9,4),(9,1),(7,2),(8,3),(8,3),(7,3),(9,4),(8,3),(9,1),(9,5),(9,2),(9,1),(7,3),(9,1),(8,3),(8,3),(9,5),(10,1),(9,1),(9,3),(9,2),(9,2),(9,2),(9,1),(9,4),(9,3),(9,2),(10,2),(10,1),(9,3),(9,1),(9,3),(9,2),(9,4),(10,3),(9,3),(9,4),(10,2),(9,5),(9,2),(9,4),(9,3),(9,5),(10,3),(10,1),(9,5),(10,4),(9,4),(9,4),(9,3),(9,5),(10,1),(10,4),(10,5),(10,2),(9,5),(9,5),(10,1),(10,1),(9,4),(10,2),(10,6),(10,2),(10,5),(10,1),(10,3),(10,3),(10,2),(9,5),(10,1),(10,6),(10,3),(10,2),(10,3),(10,1),(10,2),(10,4),(10,4),(10,5),(10,4),(10,3),(10,2),(10,4),(10,3),(10,5),(10,6),(10,3),(10,4),(10,5),(10,4),(10,5),(10,6),(10,5),(10,5),(10,6),(10,6),(10,4),(10,6),(10,6),(10,5),(10,6);
/*!40000 ALTER TABLE `role_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `role_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  PRIMARY KEY (`role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'ALL'),(2,'NO_M'),(3,'NO_CT'),(4,'NO_P'),(5,'NO_PCT'),(6,'NO_CTM'),(7,'NO_PM'),(8,'NO_PCTM'),(9,'ADMIN'),(10,'CHIEF_ADMIN');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `statuses`
--

DROP TABLE IF EXISTS `statuses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `statuses` (
  `status_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  PRIMARY KEY (`status_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `statuses`
--

LOCK TABLES `statuses` WRITE;
/*!40000 ALTER TABLE `statuses` DISABLE KEYS */;
INSERT INTO `statuses` VALUES (1,'NEW'),(2,'ACCEPTED'),(3,'OPEN'),(4,'WAITING'),(5,'REJECTED'),(6,'CLOSE');
/*!40000 ALTER TABLE `statuses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subscriptions`
--

DROP TABLE IF EXISTS `subscriptions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subscriptions` (
  `user_id` int NOT NULL,
  `ticket_id` int NOT NULL,
  PRIMARY KEY (`user_id`,`ticket_id`),
  KEY `subscriptions_user_id` (`user_id`),
  KEY `subscriptions_ticket_id` (`ticket_id`),
  CONSTRAINT `subscriptions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `subscriptions_ibfk_2` FOREIGN KEY (`ticket_id`) REFERENCES `tickets` (`ticket_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subscriptions`
--

LOCK TABLES `subscriptions` WRITE;
/*!40000 ALTER TABLE `subscriptions` DISABLE KEYS */;
/*!40000 ALTER TABLE `subscriptions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tickets`
--

DROP TABLE IF EXISTS `tickets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tickets` (
  `ticket_id` int NOT NULL AUTO_INCREMENT,
  `creator_id` int NOT NULL,
  `assignee_id` int DEFAULT NULL,
  `subject` varchar(255) NOT NULL,
  `body` text NOT NULL,
  `hidden` tinyint(1) NOT NULL,
  `anonymous` tinyint(1) NOT NULL,
  `upvotes` int NOT NULL,
  `created` datetime NOT NULL,
  `faculty_id` int NOT NULL,
  `queue_id` int DEFAULT NULL,
  `status_id` int NOT NULL,
  PRIMARY KEY (`ticket_id`),
  KEY `tickets_creator_id` (`creator_id`),
  KEY `tickets_assignee_id` (`assignee_id`),
  KEY `tickets_faculty_id` (`faculty_id`),
  KEY `tickets_queue_id` (`queue_id`),
  KEY `tickets_status_id` (`status_id`),
  CONSTRAINT `tickets_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `tickets_ibfk_2` FOREIGN KEY (`assignee_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `tickets_ibfk_3` FOREIGN KEY (`faculty_id`) REFERENCES `faculties` (`faculty_id`),
  CONSTRAINT `tickets_ibfk_4` FOREIGN KEY (`queue_id`) REFERENCES `queues` (`queue_id`),
  CONSTRAINT `tickets_ibfk_5` FOREIGN KEY (`status_id`) REFERENCES `statuses` (`status_id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tickets`
--

LOCK TABLES `tickets` WRITE;
/*!40000 ALTER TABLE `tickets` DISABLE KEYS */;
INSERT INTO `tickets` VALUES (1,9,NULL,'Katleta po Kievsky','Katleta po Kievsky azh 40 grn + !!!!!!! ya za taki groshi cilu shaurmu malenku mozhu kupyty.',0,0,0,'2023-06-10 12:07:24',1,2,6),(2,7,NULL,'Саша нічо не робить ','Urgent!!!\n\nСаша не ходить на мітинги й нічо не робить, хоче багато балів і грошей\n\nPlease advise\n\n----\n\nKind regards,\n\nШиз',0,0,0,'2023-06-10 12:07:29',1,7,3),(3,8,NULL,'Йа пердолє курва','Гойда дамбіть бамбас',1,0,0,'2023-06-10 19:57:33',1,2,3),(4,8,NULL,'і','і',0,0,0,'2023-06-10 19:59:23',1,1,2),(5,7,NULL,'Test','testtest',0,0,0,'2023-06-13 08:53:07',1,1,2),(6,7,NULL,'Test for Biem','testtest',0,0,0,'2023-06-13 08:53:42',2,3,2),(7,7,NULL,'Test for Biem 2','another one',0,0,0,'2023-06-13 08:53:53',2,3,2),(8,7,NULL,'Test','desc',0,0,0,'2023-06-13 10:18:11',1,1,6),(10,8,NULL,'я живу під мостом','лдололфіовдфоілдвжодфліво',0,0,0,'2023-06-13 20:09:52',1,7,4),(11,7,10,'Скарга на університетське харчування в столовці','Шановна адміністрація університетського столової!\n\nЯ звертаюся до вас зі скаргою щодо низької якості харчування, яке надається в столовій університету. Незважаючи на те, що столова має велике значення для студентів, які залежать від надання здорового та ситного харчування, я дуже розчарований у рівні послуг, які надаються в цьому закладі.\n\nПо-перше, мене хвилює низька якість продуктів, які використовуються в приготуванні їжі. Часто я помічаю, що овочі та фрукти є несвіжими, а м\'ясо має неприємний запах. Це не тільки негативно впливає на смак страв, але й може становити ризик для здоров\'я студентів.\n\nПо-друге, обслуговування в столовій залишає бажати кращого. Часто студенти змушені чекати велику кількість часу, щоб отримати їжу, чергуючи в довгих чергах. Це не тільки втрачає наше дорогоцінне час, але й утруднює навчання та виконання інших обов\'язків.\n\nКрім того, асортимент страв, що пропонується, є обмеженим та малорізноманітним. Часто ми отримуємо однотипні страви, які швидко набридають. Важливо мати можливість вибирати з різноманіття страв, які задовольнять смакові уподобання та діетичні потреби різних студентів.\n\nТакож, бажаю відмітити, що середовище в столовій несприятливе для спокійного та комфортного харчування. Гучна музика, неприємний запах та недостатня чистота створюють стресову атмосферу, яка негативно впливає на наше самопочуття та настрій.\n\nЯ сподіваюся, що ви врахуєте мої зауваження та вживете необхідних заходів для поліпшення ситуації. Столова має велике значення для нашого благополуччя та здоров\'я, тому намагайтеся забезпечити нам якісне та задовільне харчування.\n\nДякую за вашу увагу, і я сподіваюся на позитивні зміни в найближчому майбутньому.\n\nЗ повагою,\nзастосувач, занепокоєний станом університетського харчування',0,0,0,'2023-06-14 10:27:42',1,2,6),(12,7,NULL,'Запитання про стипендію','1. Які критерії потрібно виконати, щоб отримати стипендію?\n2. Яка сума стипендії надається студентам?\n3. Які документи необхідно подати для отримання стипендії?\n4. Які періоди виплати стипендій?\n5. Чи існують додаткові можливості отримати фінансову підтримку, окрім стипендії?\n6. Чи залежить сума стипендії від академічних досягнень чи інших факторів?\n7. Як можна збільшити шанси на отримання стипендії?\n8. Чи є можливість отримати стипендію на основі соціальних критеріїв?\n9. Чи надає університет додаткову підтримку стипендіатам у формі практик, стажувань або інших можливостей?\n10. Чи є можливість продовження отримання стипендії наступні роки навчання?',0,0,0,'2023-06-14 10:36:36',1,5,3),(13,7,NULL,'Гуртожиток: питання студента','1. Які умови проживання надаються студентам в гуртожитку?\n2. Яким чином відбувається розподіл кімнат в гуртожитку?\n3. Які послуги та зручності надаються в гуртожитку (наприклад, інтернет, пральня, спортивний зал)?\n4. Чи є обмеження щодо часу виходу та входу в гуртожиток?\n5. Як забезпечується безпека та контроль доступу до гуртожитку?\n6. Чи дозволяється проживання з одним чи декількома співмешканцями?\n7. Які правила та політики стосовно порядку та дисципліни існують у гуртожитку?\n8. Чи є можливість отримати пріоритет при наданні місця в гуртожитку для студентів з інших міст або іноземців?\n9. Чи існують спеціальні гуртожитки для студентів з особливими потребами чи обмеженими можливостями?\n10. Як можна звернутися за допомогою або подати скаргу щодо умов проживання в гуртожитку?',0,0,0,'2023-06-14 10:38:54',1,7,3),(14,7,NULL,'Скарга на навчальний процес','Шановна адміністрація університету!\n\nЯ звертаюся до вас зі своїми спостереженнями та певними побажаннями щодо навчального процесу в нашому університеті. Хочу відзначити, що мої слова базуються на моєму бажанні покращити загальний досвід студентів та сприяти їхньому академічному успіху.\n\nПо-перше, я б хотів висловити свою занепокоєність щодо недостатньої доступності викладачів поза класних занять. Часто студенти мають запитання, потребують додаткових пояснень або консультацій поза годинами лекцій та семінарів. Було б чудово, якби університет забезпечив більш відкритий та доступний для спілкування підхід з боку викладачів.\n\nПо-друге, хотілося б бачити більше різноманітних методів навчання, які заохочують активну участь студентів. Традиційні лекції і семінари є важливими, але існує потреба у більш інтерактивних форматах, таких як дискусії, групові проекти та практичні вправи. Це допоможе залучити студентів до процесу навчання і зробить його більш захопливим та ефективним.\n\nКрім того, було б корисно мати більш прозору систему оцінювання та зворотний зв\'язок щодо академічних досягнень. Часто студенти не отримують достатньо докладного роз\'яснення щодо критеріїв оцінювання та побажань викладачів. Це може призводити до незрозуміння та непорозумінь, а також ускладнювати процес саморозвитку.\n\nЯ хотів би відзначити\n\n, що мої коментарі та пропозиції носять конструктивний характер і спрямовані на покращення загального досвіду студентів. Я вірю, що наш університет має потенціал стати ще кращим, і як студент, я прагну внести свій внесок у цей процес.\n\nДякую за вашу увагу до моїх зауважень. Будь ласка, розгляньте їх серйозно та вживіть відповідних заходів для поліпшення навчального процесу в нашому університеті.\n\nЗ повагою,\nзастосувач, зацікавлений у вдосконаленні навчального середовища',0,0,0,'2023-06-14 10:46:06',1,1,6),(15,7,NULL,'Скарга на систему стипендій','Шановна адміністрація університету!\n\nЯ звертаюся до вас з серйозною скаргою щодо системи стипендій, яка діє в нашому університеті. Хочу відзначити, що мої слова висловлюють загальне незадоволення студентської громади та висловлюють нашу спільну потребу в поліпшенні цієї ситуації.\n\nПо-перше, сума стипендії, яка надається студентам, є надто низькою, щоб задовольнити їхні фінансові потреби та забезпечити повноцінне навчання. Багато студентів змушені працювати на парт-тайм роботі, щоб забезпечити себе основними засобами існування. Це негативно впливає на їхню академічну продуктивність та може призводити до втрати інтересу до навчання.\n\nПо-друге, критерії отримання стипендії є недостатньо прозорими та справедливими. Часто студенти, які мають високі академічні досягнення або відзначаються у суспільних або наукових сферах, не отримують належного визнання та винагороди у вигляді стипендії. В той же час, деякі студенти, які не проявляють особливих зусиль, отримують стипендії, що порушує принципи справедливості та мотивації досягнень.\n\nКрім того, процес отримання та виплати стипендій є недостатньо ефективним та затягується в часі. Багато студентів змушені чекати довгий період, щоб отримати свої стипендії, що ускладнює їхнє фінансове планування та може впливат\n\nи на їхню здатність продовжувати навчання.\n\nЯ хотів би наголосити, що стипендії відіграють важливу роль у стимулюванні студентів досягати високих результатів та розвиватися. Проте, в нашому університеті ця система потребує суттєвих змін та поліпшень.\n\nЯ закликаю вас вжити наступних заходів:\n\n1. Збільшити суму стипендій, щоб вона була достатньою для забезпечення основних потреб студентів та їхнього академічного розвитку.\n\n2. Удосконалити критерії отримання стипендії, враховуючи не лише академічні досягнення, а й зусилля студентів у суспільних, наукових та спортивних сферах.\n\n3. Зробити процес отримання та виплати стипендій швидшим та більш ефективним, зменшивши бюрократичні перешкоди та затримки.\n\nЯ сподіваюся, що ви врахуєте мої скарги та вживете необхідних заходів для покращення системи стипендій у нашому університеті. Стипендії мають велике значення для мотивації та підтримки студентів, і їхнє належне функціонування важливо для успішності навчання та розвитку.\n\nДякую за увагу до моїх проблематичних питань. Будь ласка, розгляньте їх серйозно та дійте на користь студентської громади.\n\nЗ повагою,\nзастосувач, занепокоєний системою стипендій',0,0,0,'2023-06-14 10:47:26',1,9,3),(16,7,NULL,'Скарга на викладача','Шановний Павло Ігорьович,\n\nЯ звертаюся до вас з серйозною скаргою стосовно вашої роботи в якості викладача в нашому університеті. Хочу відзначити, що мої слова базуються на особистому досвіді та спостереженнях, і метою цього звернення є покращення якості навчання та студентського досвіду.\n\nПо-перше, я хотів би висловити своє розчарування щодо якості вашого викладання. Уроки, які ви проводите, часто характеризуються відсутністю структури, низьким рівнем підготовки та недостатньою здатністю пояснювати складні концепції. Це ускладнює наше розуміння предмету та утруднює навчання.\n\nПо-друге, бажаною характеристикою викладача є здатність встановлювати ефективний контакт зі студентами та стимулювати їхню активну участь. Однак, я маю враження, що ви не проявляєте достатнього інтересу до наших запитань та коментарів, і не стимулюєте нас до активного залучення до дискусій та обговорень.\n\nКрім того, я хочу звернути вашу увагу на відсутність чіткості та конструктивного зворотного зв\'язку щодо наших академічних досягнень та оцінювання. Ми не отримуємо належних роз\'яснень щодо наших помилок та можливостей для поліпшення, що ускладнює наше особисте зростання та навчання.\n\nЯ розумію, що робота викладача може бути вимогливою та викликати стрес, але ми, як студенти, маємо право на якісну освіту та належну підтримку. М\n\nи довіряємо вам як фахівцю та наставнику, і сподіваємось на поліпшення в цих аспектах вашої роботи.\n\nЯ закликаю вас вжити наступних заходів:\n\n1. Звернути більшу увагу на підготовку до уроків та забезпечення їхньої структурованості та доступності для студентів.\n\n2. Стимулювати активну участь студентів у навчальному процесі, створюючи сприятливу атмосферу для дискусій та взаємодії.\n\n3. Надавати чіткий та конструктивний зворотний зв\'язок стосовно академічних досягнень та оцінювання, сприяючи особистому розвитку студентів.\n\nЯ сподіваюся, що ви врахуєте мої зауваження та зробите необхідні зміни у вашій роботі. Наш успіх залежить від якості навчання та нашої взаємодії з викладачами.\n\nДякую за увагу до моїх проблематичних питань. Будь ласка, розгляньте їх серйозно та дійте на користь студентської громади.\n\nЗ повагою,\nзастосувач, занепокоєний якістю викладання',0,0,0,'2023-06-14 10:51:55',1,1,2),(17,10,NULL,'В гуртожитку добу не було гарячої води','13 червня повідомили, що не буде гарячої води. Мовляв, зняли на перевірку лічильник.\n\nХіба у водоканалу немає запасних лічильників на заміну, чи студенти стерплять?!!!',0,0,0,'2023-06-14 11:24:04',1,9,2),(18,10,NULL,'Пільгове проживання','Доброго дня.\n\nЯкі мені документи треба для того, щоб проживати на пільгових умовах?\n\nМій батько учасник бойових дій. \n\nДякую заздалегідь',0,0,0,'2023-06-14 11:25:46',1,7,2),(19,10,NULL,'Викладач відмовляється викладати українською','Викладач John Doe відверто відмовляється викладати українською мовою ігноруючи зауваження. \n\nДо того ж методичний матеріал також в більшості своїй викладено російською.',0,0,0,'2023-06-14 11:28:02',1,1,4),(20,7,NULL,'Питання до деканату','1. Які основні обов\'язки деканату в університеті?\n2. Як можна звернутися до деканату із запитаннями або проблемами?\n3. Які документи потрібні для оформлення академічних справ у деканаті?\n4. Як можна отримати інформацію про актуальні академічні календарі, терміни здачі робіт чи іспитів?\n5. Чи надає деканат підтримку студентам у вирішенні особистих проблем або складних життєвих ситуацій?\n6. Які є процедури зміни спеціальності або курсу в деканаті?\n7. Як можна отримати довідку про навчання або академічну успішність у деканаті?\n8. Які є процедури оформлення академічних відпусток або звільнень від навчання?\n9. Які є можливості для студентів отримати стипендію чи фінансову допомогу через деканат?\n10. Які є правила та процедури щодо перенесення іспитів або подачі заяв про академічну відстрочку?\n',0,0,0,'2023-06-14 12:08:15',1,7,2),(21,7,NULL,'qwr','qwrqwr',1,1,0,'2023-06-23 21:32:18',1,2,5),(22,8,NULL,'Хочу куфотб','Я котлетка',0,0,0,'2023-07-01 17:56:04',1,2,5),(23,7,NULL,'qwqwt','qwtqwtqwt',0,0,0,'2023-07-05 19:43:48',1,5,5),(24,7,NULL,'qwrqwr','asgasnxzhh',0,0,0,'2023-07-05 19:54:53',1,1,4),(25,8,NULL,'Що робити якщо я люблю пельмені?','Пельмені це пельмені',0,1,0,'2023-07-06 17:15:50',1,2,4),(26,8,NULL,'test','test private',1,0,0,'2023-07-06 17:16:49',1,5,2),(27,8,NULL,'mister fish','q',1,1,0,'2023-07-06 17:17:29',1,5,2),(28,7,NULL,'new','Delete this ticket',0,0,0,'2023-07-07 18:21:46',1,2,5),(29,10,NULL,'Тестування','Перший тікетс з вебки в кубернетес кластері. І шо, навіть запрацює?',0,0,0,'2023-07-26 20:01:25',1,2,4),(30,7,NULL,'Test markdown','# Heading 1\n\n## Heading 2\n\n### Heading 3\n\n#### Heading 4\n\n##### Heading 5\n\n###### Heading 6\n\n\n**A bold text**\n\n_An italic text_\n\n**A strong text**\n\n\n1. An ordered list text\n1. An ordered list text\n1. An ordered list text\n\n\n- An unordered list text\n- An unordered list text\n- An unordered list text\n\n\n`A blockquote text`\n\n~~A crossed-out text~~\n\n![cat](https://e1.pxfuel.com/desktop-wallpaper/993/108/desktop-wallpaper-cute-cat-small-cat-thumbnail.jpg)\n\n- [ ] Task 1\n\n- [ ] Task 2\n\n- [x] Completed task\n\n- TreS: https://demo.tres.cyberbydlo.com/general_tickets\n\n| S/N | Pet | Image |\n|--|--|--|\n| 1 | Cat |![A cat looking at you](https://www.dogalize.com/wp-content/uploads/2019/03/Small-cats-list-200x200.jpg) |\n| 2 | Dog |![A dog looking at you](https://static.vecteezy.com/system/resources/thumbnails/016/761/881/small/the-dog-smiles-because-he-is-happy-png.png)|',0,0,0,'2023-08-02 18:43:10',1,5,2),(31,8,NULL,'Викладач імбіцил','Викладач не пояснив правопис \"внатурі\" чи \"в натурі\".\n\n# Буду скаржитися НАТО.',0,1,0,'2023-08-03 17:38:03',1,1,3),(32,8,NULL,'проблеми з шлунком','я з\'їв викладача',0,1,0,'2023-08-05 12:05:27',1,2,3);
/*!40000 ALTER TABLE `tickets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `firstname` varchar(60) DEFAULT NULL,
  `lastname` varchar(60) DEFAULT NULL,
  `login` varchar(25) NOT NULL,
  `faculty_id` int DEFAULT NULL,
  `group_id` int DEFAULT NULL,
  `password` text NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `registration_date` datetime NOT NULL,
  `role_id` int DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  KEY `users_faculty_id` (`faculty_id`),
  KEY `users_group_id` (`group_id`),
  KEY `users_role_id` (`role_id`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`faculty_id`) REFERENCES `faculties` (`faculty_id`),
  CONSTRAINT `users_ibfk_2` FOREIGN KEY (`group_id`) REFERENCES `groups` (`group_id`),
  CONSTRAINT `users_ibfk_3` FOREIGN KEY (`role_id`) REFERENCES `roles` (`role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,NULL,NULL,'qwertyuiop',1,1,'932cd2a1f3f99f2137f0dcef380b88558f76e60fdf528f4a90303ed554ac90141a479d6067b53f96953fadd3ed5940399df6c4a51fb98cc8204a0f5c7af62f16',NULL,NULL,'2023-05-24 17:45:15',1),(2,NULL,NULL,'sdfsdfsdf',1,1,'404478514d2c3e43bab303816f80be1e9a8d7b4f2eeab77cc58f75ed6f1185973f586323f3bd4b57cb0150a8851e39fd6bb36d16ec18f48ed81afb2d5eb89f7e',NULL,NULL,'2023-05-26 20:49:19',1),(3,NULL,NULL,'xAZLM',1,1,'371c53ea6b8a7ca8a798ca3a88ce1b1c311a509a9cfd97863cdc18f992199af7','EOnLs','rpwlP','2023-05-27 14:44:13',1),(4,'nEDkQ','rRily','IwiKa',2,1,'8a29fa58185657c71ed18acac2ee92660a00be84933183e82a48d21f27f5d25c','BHvsd','GIVgj','2023-05-27 14:45:43',1),(5,NULL,'CIoKu','WeVxX',2,2,'9bbba14bffca769f8f3655400fd395c19c92c35f4647077f6a5f1a1671ccec1a','HMJYL',NULL,'2023-05-27 14:49:02',1),(6,'kgMjx',NULL,'hoKyG',2,2,'107c10a72d5d4e0f719f8b5375e03ae86410950bc0a11d21dcc8651466ceac55','mcraF',NULL,'2023-05-27 14:58:54',1),(7,'Biba','Booba','admin',1,1,'d82494f05d6917ba02f7aaa29689ccb444bb73f20380876cb05d1f37537b7892',NULL,NULL,'2023-05-27 15:18:48',1),(8,'Pelmen','Minometchik','SSU_lover',1,2,'9a900403ac313ba27a1bc81f0932652b8020dac92c234d98fa0b06bf0040ecfd',NULL,NULL,'2023-05-29 17:56:26',1),(9,NULL,NULL,'artem',1,2,'42b72816da05f1ec0b3ea5327be3a9ace4ec2330993c813a3c6d1f2e5822c9ce',NULL,NULL,'2023-06-10 10:31:51',1),(10,'Dmytro','Borshch','dmytro',1,3,'fa3f7dc098ae79d63efc4f17f2bce2489b7d3bef4f5fc19ed3618c0623aae31a',NULL,NULL,'2023-06-14 11:20:45',1);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-08-05 12:48:13
