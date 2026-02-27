-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: shoes_company
-- ------------------------------------------------------
-- Server version	8.0.45

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `manufacturers`
--

DROP TABLE IF EXISTS `manufacturers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `manufacturers` (
  `manufacturer_id` int NOT NULL AUTO_INCREMENT,
  `manufacturer_name` varchar(100) NOT NULL,
  PRIMARY KEY (`manufacturer_id`),
  UNIQUE KEY `manufacturer_name` (`manufacturer_name`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `manufacturers`
--

LOCK TABLES `manufacturers` WRITE;
/*!40000 ALTER TABLE `manufacturers` DISABLE KEYS */;
INSERT INTO `manufacturers` VALUES (5,'Alessio Nesca'),(8,'ARGO'),(12,'Caprice'),(6,'CROSBY'),(9,'FRAU'),(1,'Kari'),(10,'Luiza Belly'),(2,'Marco Tozzi'),(4,'Rieker'),(7,'ROMER'),(11,'TOFA'),(3,'Рос');
/*!40000 ALTER TABLE `manufacturers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orderitems`
--

DROP TABLE IF EXISTS `orderitems`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orderitems` (
  `order_item_id` int NOT NULL AUTO_INCREMENT,
  `order_id` int NOT NULL,
  `product_id` int NOT NULL,
  `quantity` int NOT NULL,
  `unit_price` decimal(10,2) NOT NULL,
  PRIMARY KEY (`order_item_id`),
  UNIQUE KEY `unique_order_product` (`order_id`,`product_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `orderitems_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`) ON DELETE CASCADE,
  CONSTRAINT `orderitems_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE CASCADE,
  CONSTRAINT `orderitems_chk_1` CHECK ((`quantity` > 0)),
  CONSTRAINT `orderitems_chk_2` CHECK ((`unit_price` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orderitems`
--

LOCK TABLES `orderitems` WRITE;
/*!40000 ALTER TABLE `orderitems` DISABLE KEYS */;
INSERT INTO `orderitems` VALUES (1,1,1,2,4990.00),(2,1,2,2,3244.00),(3,2,3,1,4499.00),(4,2,4,1,5900.00),(5,3,5,10,3800.00),(6,3,6,10,4100.00),(7,4,7,5,2700.00),(8,4,8,4,1890.00),(9,5,1,2,4990.00),(10,5,2,2,3244.00),(11,6,3,1,4499.00),(12,6,4,1,5900.00),(13,7,5,10,3800.00),(14,7,6,10,4100.00),(15,8,7,5,2700.00),(16,8,8,4,1890.00),(17,9,9,5,4300.00),(18,9,10,1,2800.00),(19,10,11,5,2156.00),(20,10,12,5,1800.00);
/*!40000 ALTER TABLE `orderitems` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `order_id` int NOT NULL AUTO_INCREMENT,
  `order_date` datetime NOT NULL,
  `delivery_date` datetime DEFAULT NULL,
  `pickup_point_id` int NOT NULL,
  `client_id` int NOT NULL,
  `pickup_code` varchar(20) NOT NULL,
  `status` varchar(50) NOT NULL DEFAULT 'Новый',
  PRIMARY KEY (`order_id`),
  KEY `pickup_point_id` (`pickup_point_id`),
  KEY `client_id` (`client_id`),
  KEY `idx_orders_date` (`order_date`),
  KEY `idx_orders_status` (`status`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`pickup_point_id`) REFERENCES `pickuppoints` (`point_id`) ON DELETE CASCADE,
  CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`client_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (1,'2025-02-27 00:00:00','2025-04-20 00:00:00',1,4,'901','Завершен'),(2,'2022-09-28 00:00:00','2025-04-21 00:00:00',11,1,'902','Завершен'),(3,'2025-03-21 00:00:00','2025-04-22 00:00:00',2,2,'903','Завершен'),(4,'2025-02-20 00:00:00','2025-04-23 00:00:00',11,3,'904','Завершен'),(5,'2025-03-17 00:00:00','2025-04-24 00:00:00',2,4,'905','Завершен'),(6,'2025-03-01 00:00:00','2025-04-25 00:00:00',15,1,'906','Завершен'),(7,'2025-02-28 00:00:00','2025-04-26 00:00:00',3,2,'907','Завершен'),(8,'2025-03-31 00:00:00','2025-04-27 00:00:00',19,3,'908','Новый'),(9,'2025-04-02 00:00:00','2025-04-28 00:00:00',5,4,'909','Новый'),(10,'2025-04-03 00:00:00','2025-04-29 00:00:00',19,4,'910','Новый');
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pickuppoints`
--

DROP TABLE IF EXISTS `pickuppoints`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pickuppoints` (
  `point_id` int NOT NULL AUTO_INCREMENT,
  `address` varchar(255) NOT NULL,
  `post_code` varchar(10) NOT NULL,
  PRIMARY KEY (`point_id`),
  UNIQUE KEY `address` (`address`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pickuppoints`
--

LOCK TABLES `pickuppoints` WRITE;
/*!40000 ALTER TABLE `pickuppoints` DISABLE KEYS */;
INSERT INTO `pickuppoints` VALUES (1,'г. Лесной, ул. Вишневая, 32','420151'),(2,'г. Лесной, ул. Подгорная, 8','125061'),(3,'г. Лесной, ул. Шоссейная, 24','630370'),(4,'г. Лесной, ул. Зеленая, 32','400562'),(5,'г. Лесной, ул. Маяковского, 47','614510'),(6,'г. Лесной, ул. Светлая, 46','410542'),(7,'г. Лесной, ул. Цветочная, 8','620839'),(8,'г. Лесной, ул. Коммунистическая, 1','443890'),(9,'г. Лесной, ул. Спортивная, 46','603379'),(10,'г. Лесной, ул. Гоголя, 41','603721'),(11,'г. Лесной, ул. Северная, 13','410172'),(12,'г. Лесной, ул. Молодежная, 50','614611'),(13,'г. Лесной, ул. Новая, 19','454311'),(14,'г. Лесной, ул. Октябрьская, 19','660007'),(15,'г. Лесной, ул. Садовая, 4','603036'),(16,'г. Лесной, ул. Фрунзе, 43','394060'),(17,'г. Лесной, ул. Школьная, 50','410661'),(18,'г. Лесной, ул. Коммунистическая, 20','625590'),(19,'г. Лесной, ул. 8 Марта','625683'),(20,'г. Лесной, ул. Комсомольская, 26','450983'),(21,'г. Лесной, ул. Чехова, 3','394782'),(22,'г. Лесной, ул. Дзержинского, 28','603002'),(23,'г. Лесной, ул. Набережная, 30','450558'),(24,'г. Лесной, ул. Чехова, 1','344288'),(25,'г. Лесной, ул. Степная, 30','614164'),(26,'г. Лесной, ул. Коммунистическая, 43','394242'),(27,'г. Лесной, ул. Солнечная, 25','660540'),(28,'г. Лесной, ул. Шоссейная, 40','125837'),(29,'г. Лесной, ул. Партизанская, 49','125703'),(30,'г. Лесной, ул. Победы, 46','625283'),(31,'г. Лесной, ул. Полевая, 35','614753'),(32,'г. Лесной, ул. Маяковского, 44','426030'),(33,'г. Лесной, ул. Клубная, 44','450375'),(34,'г. Лесной, ул. Некрасова, 12','625560'),(35,'г. Лесной, ул. Комсомольская, 17','630201'),(36,'г. Лесной, ул. Мичурина, 26','190949');
/*!40000 ALTER TABLE `pickuppoints` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productcategories`
--

DROP TABLE IF EXISTS `productcategories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `productcategories` (
  `category_id` int NOT NULL AUTO_INCREMENT,
  `category_name` varchar(50) NOT NULL,
  PRIMARY KEY (`category_id`),
  UNIQUE KEY `category_name` (`category_name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productcategories`
--

LOCK TABLES `productcategories` WRITE;
/*!40000 ALTER TABLE `productcategories` DISABLE KEYS */;
INSERT INTO `productcategories` VALUES (1,'Женская обувь'),(2,'Мужская обувь');
/*!40000 ALTER TABLE `productcategories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `product_id` int NOT NULL AUTO_INCREMENT,
  `article_number` varchar(20) NOT NULL,
  `product_name` varchar(150) NOT NULL,
  `unit_of_measure` varchar(10) NOT NULL DEFAULT 'шт.',
  `price` decimal(10,2) NOT NULL,
  `supplier_id` int NOT NULL,
  `manufacturer_id` int NOT NULL,
  `category_id` int NOT NULL,
  `current_discount` int DEFAULT '0',
  `stock_quantity` int DEFAULT '0',
  `description` text,
  `photo_filename` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`product_id`),
  UNIQUE KEY `article_number` (`article_number`),
  KEY `supplier_id` (`supplier_id`),
  KEY `manufacturer_id` (`manufacturer_id`),
  KEY `idx_products_article` (`article_number`),
  KEY `idx_products_name` (`product_name`),
  KEY `idx_products_price` (`price`),
  KEY `idx_products_category` (`category_id`),
  CONSTRAINT `products_ibfk_1` FOREIGN KEY (`supplier_id`) REFERENCES `suppliers` (`supplier_id`) ON DELETE CASCADE,
  CONSTRAINT `products_ibfk_2` FOREIGN KEY (`manufacturer_id`) REFERENCES `manufacturers` (`manufacturer_id`) ON DELETE CASCADE,
  CONSTRAINT `products_ibfk_3` FOREIGN KEY (`category_id`) REFERENCES `productcategories` (`category_id`) ON DELETE CASCADE,
  CONSTRAINT `products_chk_1` CHECK ((`price` > 0)),
  CONSTRAINT `products_chk_2` CHECK (((`current_discount` >= 0) and (`current_discount` <= 100))),
  CONSTRAINT `products_chk_3` CHECK ((`stock_quantity` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,'А112Т4','Ботинки','шт.',21412.00,1,12,2,3,6,'Мужские Ботинки демисезонные kari','1.jpg'),(2,'F635R4','Ботинки','шт.',3244.00,2,2,1,20,13,'Ботинки Marco Tozzi женские демисезонные, размер 39, цвет бежевый','2.jpg'),(3,'H782T5','Туфли','шт.',4499.00,1,1,2,25,5,'Туфли kari мужские классика MYZ21AW-450A, размер 43, цвет: черный','3.jpg'),(4,'G783F5','Ботинки','шт.',5900.00,1,3,2,2,8,'Мужские ботинки Рос-Обувь кожаные с натуральным мехом','4.jpg'),(5,'J384T6','Ботинки','шт.',3800.00,2,4,2,2,16,'B3430/14 Полуботинки мужские Rieker','5.jpg'),(6,'D572U8','Кроссовки','шт.',4100.00,2,3,2,3,6,'129615-4 Кроссовки мужские','6.jpg'),(7,'F572H7','Туфли','шт.',2700.00,1,2,1,2,14,'Туфли Marco Tozzi женские летние, размер 39, цвет черный','7.jpg'),(8,'D329H3','Полуботинки','шт.',1890.00,2,5,1,4,4,'Полуботинки Alessio Nesca женские 3-30797-47, размер 37, цвет: бордовый','8.jpg'),(9,'B320R5','Туфли','шт.',4300.00,1,4,1,2,6,'Туфли Rieker женские демисезонные, размер 41, цвет коричневый','9.jpg'),(10,'G432E4','Туфли','шт.',2800.00,1,1,1,3,15,'Туфли kari женские TR-YR-413017, размер 37, цвет: черный','10.jpg'),(11,'S213E3','Полуботинки','шт.',2156.00,2,6,2,3,6,'407700/01-01 Полуботинки мужские CROSBY',NULL),(12,'E482R4','Полуботинки','шт.',1800.00,1,1,1,2,14,'Полуботинки kari женские MYZ20S-149, размер 41, цвет: черный',NULL),(13,'S634B5','Кеды','шт.',5500.00,2,6,2,3,0,'Кеды Caprice мужские демисезонные, размер 42, цвет черный',NULL),(14,'K345R4','Полуботинки','шт.',2100.00,2,6,2,2,3,'407700/01-02 Полуботинки мужские CROSBY',NULL),(15,'O754F4','Туфли','шт.',5400.00,2,4,1,4,18,'Туфли женские демисезонные Rieker артикул 55073-68/37',NULL),(16,'G531F4','Ботинки','шт.',6600.00,1,1,1,12,9,'Ботинки женские зимние ROMER арт. 893167-01 Черный',NULL),(17,'J542F5','Тапочки','шт.',500.00,1,1,2,13,0,'Тапочки мужские Арт.70701-55-67син р.41',NULL),(18,'B431R5','Ботинки','шт.',2700.00,2,4,2,2,5,'Мужские кожаные ботинки/мужские ботинки',NULL),(19,'P764G4','Туфли','шт.',6800.00,1,6,1,15,15,'Туфли женские, ARGO, размер 38',NULL),(20,'C436G5','Ботинки','шт.',10200.00,1,5,1,15,9,'Ботинки женские, ARGO, размер 40',NULL),(21,'F427R5','Ботинки','шт.',11800.00,2,4,1,15,11,'Ботинки на молнии с декоративной пряжкой FRAU',NULL),(22,'N457T5','Полуботинки','шт.',4600.00,1,6,1,3,13,'Полуботинки Ботинки черные зимние, мех',NULL),(23,'D364R4','Туфли','шт.',12400.00,1,1,1,16,5,'Туфли Luiza Belly женские Kate-lazo черные из натуральной замши',NULL),(24,'S326R5','Тапочки','шт.',9900.00,2,6,2,17,15,'Мужские кожаные тапочки \"Профиль С.Дали\"',NULL),(25,'L754R4','Полуботинки','шт.',1700.00,1,1,1,2,7,'Полуботинки kari женские WB2020SS-26, размер 38, цвет: черный',NULL),(26,'M542T5','Кроссовки','шт.',2800.00,2,4,2,18,3,'Кроссовки мужские TOFA',NULL),(27,'D268G5','Туфли','шт.',4399.00,2,4,1,3,12,'Туфли Rieker женские демисезонные, размер 36, цвет коричневый',NULL),(28,'T324F5','Сапоги','шт.',4699.00,1,6,1,2,5,'Сапоги замша Цвет: синий',NULL),(29,'K358H6','Тапочки','шт.',599.00,1,4,2,20,2,'Тапочки мужские син р.41',NULL),(30,'H535R5','Ботинки','шт.',2300.00,2,4,1,2,7,'Женские Ботинки демисезонные',NULL);
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `role_id` int NOT NULL AUTO_INCREMENT,
  `role_name` varchar(50) NOT NULL,
  PRIMARY KEY (`role_id`),
  UNIQUE KEY `role_name` (`role_name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (3,'Авторизированный клиент'),(1,'Администратор'),(4,'Гость'),(2,'Менеджер');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `suppliers`
--

DROP TABLE IF EXISTS `suppliers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `suppliers` (
  `supplier_id` int NOT NULL AUTO_INCREMENT,
  `supplier_name` varchar(100) NOT NULL,
  PRIMARY KEY (`supplier_id`),
  UNIQUE KEY `supplier_name` (`supplier_name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `suppliers`
--

LOCK TABLES `suppliers` WRITE;
/*!40000 ALTER TABLE `suppliers` DISABLE KEYS */;
INSERT INTO `suppliers` VALUES (1,'Kari'),(2,'Обувь для вас');
/*!40000 ALTER TABLE `suppliers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `full_name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `role_id` int NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`),
  KEY `idx_users_email` (`email`),
  KEY `idx_users_role` (`role_id`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`role_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Никифорова Весения Николаевна','94d5ous@gmail.com','uzWC67',1),(2,'Сазонов Руслан Германович','uth4iz@mail.com','2L6KZG',1),(3,'Одинцов Серафим Артёмович','yzls62@outlook.com','JlFRCZ',1),(4,'Степанов Михаил Артёмович','1diph5e@tutanota.com','8ntwUp',2),(5,'Ворсин Петр Евгеньевич','tjde7c@yahoo.com','YOyhfR',2),(6,'Старикова Елена Павловна','wpmrc3do@tutanota.com','RSbvHv',2),(7,'Михайлюк Анна Вячеславовна','5d4zbu@tutanota.com','rwVDh9',3),(8,'Ситдикова Елена Анатольевна','ptec8ym@yahoo.com','LdNyos',3),(9,'Ворсин Петр Евгеньевич','1qz4kw@mail.com','gynQMT',3),(10,'Старикова Елена Павловна','4np6se@mail.com','AtnDjr',3);
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

-- Dump completed on 2026-02-27 23:01:55
