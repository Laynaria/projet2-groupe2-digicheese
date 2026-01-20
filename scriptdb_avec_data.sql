-- Adminer 5.4.1 MariaDB 10.6.24-MariaDB-ubu2204 dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;

SET NAMES utf8mb4;

DROP TABLE IF EXISTS `adresse`;
CREATE TABLE `adresse` (
  `idAdresse` int(11) NOT NULL AUTO_INCREMENT,
  `compAdresse1` varchar(255) DEFAULT NULL,
  `compAdresse2` varchar(255) DEFAULT NULL,
  `compAdresse3` varchar(255) DEFAULT NULL,
  `numeroVoie` varchar(10) NOT NULL,
  `nomVoie` varchar(255) NOT NULL,
  `idCommune` int(11) NOT NULL,
  `idClient` int(11) NOT NULL,
  PRIMARY KEY (`idAdresse`),
  KEY `idCommune` (`idCommune`),
  KEY `idClient` (`idClient`),
  CONSTRAINT `adresse_ibfk_1` FOREIGN KEY (`idCommune`) REFERENCES `commune` (`idCommune`),
  CONSTRAINT `adresse_ibfk_2` FOREIGN KEY (`idClient`) REFERENCES `client` (`idClient`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


DROP TABLE IF EXISTS `client`;
CREATE TABLE `client` (
  `idClient` int(11) NOT NULL AUTO_INCREMENT,
  `nomClient` varchar(100) NOT NULL,
  `prenomClient` varchar(100) NOT NULL,
  `genre` varchar(10) DEFAULT NULL,
  `emailClient` varchar(255) NOT NULL,
  `telephone` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`idClient`),
  UNIQUE KEY `emailClient` (`emailClient`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


DROP TABLE IF EXISTS `commande`;
CREATE TABLE `commande` (
  `idCommande` int(11) NOT NULL AUTO_INCREMENT,
  `date` date DEFAULT NULL,
  `timbreClient` float DEFAULT NULL,
  `timbreCode` float DEFAULT NULL,
  `chequeClient` float DEFAULT NULL,
  `commentaireCommande` varchar(255) DEFAULT NULL,
  `nbColis` int(11) DEFAULT NULL,
  `bArchive` tinyint(1) DEFAULT NULL,
  `client_id` int(11) DEFAULT NULL,
  `conditionnement_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`idCommande`),
  KEY `client_id` (`client_id`),
  KEY `conditionnement_id` (`conditionnement_id`),
  CONSTRAINT `commande_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `client` (`idClient`),
  CONSTRAINT `commande_ibfk_2` FOREIGN KEY (`conditionnement_id`) REFERENCES `conditionnement` (`idConditionnement`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


DROP TABLE IF EXISTS `commune`;
CREATE TABLE `commune` (
  `idCommune` int(11) NOT NULL AUTO_INCREMENT,
  `cp` varchar(10) NOT NULL,
  `nom_commune` varchar(100) NOT NULL,
  `departement` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`idCommune`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


DROP TABLE IF EXISTS `conditionnement`;
CREATE TABLE `conditionnement` (
  `idConditionnement` int(11) NOT NULL AUTO_INCREMENT,
  `libelle` varchar(50) DEFAULT NULL,
  `poidsConditionnement` float DEFAULT NULL,
  `ordreImpression` int(11) DEFAULT NULL,
  PRIMARY KEY (`idConditionnement`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


DROP TABLE IF EXISTS `detail_commande`;
CREATE TABLE `detail_commande` (
  `idDetailCommande` int(11) NOT NULL AUTO_INCREMENT,
  `quantite` int(11) DEFAULT NULL,
  `colis` varchar(20) DEFAULT NULL,
  `commentaire` varchar(255) DEFAULT NULL,
  `commande_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`idDetailCommande`),
  KEY `commande_id` (`commande_id`),
  CONSTRAINT `detail_commande_ibfk_1` FOREIGN KEY (`commande_id`) REFERENCES `commande` (`idCommande`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


DROP TABLE IF EXISTS `detail_commande_objet`;
CREATE TABLE `detail_commande_objet` (
  `idDetailCommandeObjet` int(11) NOT NULL AUTO_INCREMENT,
  `detailleCommande_id` int(11) DEFAULT NULL,
  `objet_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`idDetailCommandeObjet`),
  KEY `detailleCommande_id` (`detailleCommande_id`),
  KEY `objet_id` (`objet_id`),
  CONSTRAINT `detail_commande_objet_ibfk_1` FOREIGN KEY (`detailleCommande_id`) REFERENCES `detail_commande` (`idDetailCommande`),
  CONSTRAINT `detail_commande_objet_ibfk_2` FOREIGN KEY (`objet_id`) REFERENCES `objet` (`idObjet`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


DROP TABLE IF EXISTS `objet`;
CREATE TABLE `objet` (
  `idObjet` int(11) NOT NULL AUTO_INCREMENT,
  `libelle` varchar(50) DEFAULT NULL,
  `taille` varchar(50) DEFAULT NULL,
  `poids` decimal(10,0) DEFAULT NULL,
  `bIndispo` int(11) DEFAULT NULL,
  `points` int(11) DEFAULT NULL,
  `relCond_id` int(11) NOT NULL,
  PRIMARY KEY (`idObjet`),
  KEY `relCond_id` (`relCond_id`),
  CONSTRAINT `objet_ibfk_1` FOREIGN KEY (`relCond_id`) REFERENCES `rel_cond` (`idRelCond`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


DROP TABLE IF EXISTS `rel_cond`;
CREATE TABLE `rel_cond` (
  `idRelCond` int(11) NOT NULL AUTO_INCREMENT,
  `quantiteObjet` int(11) DEFAULT NULL,
  PRIMARY KEY (`idRelCond`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


DROP TABLE IF EXISTS `role`;
CREATE TABLE `role` (
  `idRole` int(11) NOT NULL AUTO_INCREMENT,
  `libelleRole` varchar(255) NOT NULL,
  PRIMARY KEY (`idRole`),
  UNIQUE KEY `libelleRole` (`libelleRole`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


DROP TABLE IF EXISTS `utilisateur`;
CREATE TABLE `utilisateur` (
  `idUtil` int(11) NOT NULL AUTO_INCREMENT,
  `nomUtil` varchar(255) NOT NULL,
  `prenomUtil` varchar(255) NOT NULL,
  `motDePasse` varchar(255) NOT NULL,
  `emailUtil` varchar(255) NOT NULL,
  PRIMARY KEY (`idUtil`),
  UNIQUE KEY `emailUtil` (`emailUtil`),
  KEY `ix_utilisateur_idUtil` (`idUtil`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


DROP TABLE IF EXISTS `utilisateur_role`;
CREATE TABLE `utilisateur_role` (
  `idUtil` int(11) NOT NULL,
  `idRole` int(11) NOT NULL,
  PRIMARY KEY (`idUtil`,`idRole`),
  KEY `idRole` (`idRole`),
  CONSTRAINT `utilisateur_role_ibfk_1` FOREIGN KEY (`idUtil`) REFERENCES `utilisateur` (`idUtil`),
  CONSTRAINT `utilisateur_role_ibfk_2` FOREIGN KEY (`idRole`) REFERENCES `role` (`idRole`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- 2026-01-20 15:05:47 UTC