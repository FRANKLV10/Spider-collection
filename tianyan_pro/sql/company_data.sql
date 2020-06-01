/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 100411
 Source Host           : localhost:3306
 Source Schema         : tianyancha

 Target Server Type    : MySQL
 Target Server Version : 100411
 File Encoding         : 65001

 Date: 28/04/2020 10:56:00
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for company_data
-- ----------------------------
DROP TABLE IF EXISTS `company_data`;
CREATE TABLE `company_data`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `es_time` date NULL DEFAULT NULL,
  `data_dict` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `Index_estime`(`id`, `es_time`) USING BTREE,
  INDEX `es_time`(`es_time`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1977202 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
