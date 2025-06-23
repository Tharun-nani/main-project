/*
SQLyog Enterprise - MySQL GUI v6.56
MySQL - 5.5.5-10.4.32-MariaDB : Database - lightwaitimage
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`lightwaitimage` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;

USE `lightwaitimage`;

/*Table structure for table `request` */

DROP TABLE IF EXISTS `request`;

CREATE TABLE `request` (
  `Id` int(20) NOT NULL AUTO_INCREMENT,
  `FileId` varchar(20) DEFAULT NULL,
  `owneremail` varchar(200) DEFAULT NULL,
  `receiveremail` varchar(200) DEFAULT NULL,
  `otp` varchar(200) DEFAULT NULL,
  `FileName` varchar(200) DEFAULT NULL,
  `Keyword` varchar(200) DEFAULT NULL,
  `encryption_key` varchar(200) DEFAULT NULL,
  `description` varchar(200) DEFAULT NULL,
  `Files` varchar(200) DEFAULT NULL,
  `Datetime` varchar(200) DEFAULT NULL,
  `status` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `request` */

insert  into `request`(`Id`,`FileId`,`owneremail`,`receiveremail`,`otp`,`FileName`,`Keyword`,`encryption_key`,`description`,`Files`,`Datetime`,`status`) values (1,'1','preeti@gmail.com','nakku@gmail.com','945369','blog-teaser-img2.jpg','file123','DIOmwVavmmN84GyGGXy3nr3M4_YUwckCj8xDZQ5jaQY=','This File is going to add for encryption','uploads/blog-teaser-img2.jpg','2024-08-31 11:09:42','Accepted'),(2,'2','ravi@gmail.com','kumar@gmail.com','960351','history-center.jpg','ravi123','TkxRuJQLf-PBVmWXTz0C2Mz6S8enCxDzOHzUONqirfU=','i need to hide my image','uploads/history-center.jpg','2024-08-31 11:18:50','Accepted');

/*Table structure for table `uploadfile` */

DROP TABLE IF EXISTS `uploadfile`;

CREATE TABLE `uploadfile` (
  `Id` int(20) NOT NULL AUTO_INCREMENT,
  `doemail` varchar(200) DEFAULT NULL,
  `Filename` varchar(200) DEFAULT NULL,
  `Keywords` varchar(200) DEFAULT NULL,
  `filepath` varchar(200) DEFAULT NULL,
  `description` varchar(200) DEFAULT NULL,
  `Datetime` varchar(200) DEFAULT NULL,
  `encryption_key` varchar(225) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `uploadfile` */

insert  into `uploadfile`(`Id`,`doemail`,`Filename`,`Keywords`,`filepath`,`description`,`Datetime`,`encryption_key`) values (1,'preeti@gmail.com','blog-teaser-img2.jpg','file123','uploads/blog-teaser-img2.jpg','This File is going to add for encryption','2024-08-31 11:05:12','DIOmwVavmmN84GyGGXy3nr3M4_YUwckCj8xDZQ5jaQY='),(2,'ravi@gmail.com','history-center.jpg','ravi123','uploads/history-center.jpg','i need to hide my image','2024-08-31 11:18:18','TkxRuJQLf-PBVmWXTz0C2Mz6S8enCxDzOHzUONqirfU=');

/*Table structure for table `users` */

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `Id` int(20) NOT NULL AUTO_INCREMENT,
  `username` varchar(200) DEFAULT NULL,
  `password` varchar(200) DEFAULT NULL,
  `email` varchar(200) DEFAULT NULL,
  `phone` varchar(200) DEFAULT NULL,
  `address` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `users` */

insert  into `users`(`Id`,`username`,`password`,`email`,`phone`,`address`) values (1,'preeti','a01610228fe998f515a72dd730294d87','preeti@gmail.com','07458965874','tpt'),(2,'nakku','a01610228fe998f515a72dd730294d87','nakku@gmail.com','07458965874','tpt'),(3,'ravi','a01610228fe998f515a72dd730294d87','ravi@gmail.com','07458965874','tpt'),(4,'kumar','a01610228fe998f515a72dd730294d87','kumar@gmail.com','7485965874','tpt');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
