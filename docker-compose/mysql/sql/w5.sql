
SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for w5_logs
-- ----------------------------
DROP TABLE IF EXISTS `w5_logs`;
CREATE TABLE `w5_logs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(100) NOT NULL,
  `app_uuid` varchar(100) NOT NULL,
  `app_name` varchar(20) NOT NULL DEFAULT '',
  `result` text NOT NULL,
  `status` int(2) NOT NULL DEFAULT '0',
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of w5_logs
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for w5_setting
-- ----------------------------
DROP TABLE IF EXISTS `w5_setting`;
CREATE TABLE `w5_setting` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `key` varchar(255) NOT NULL DEFAULT '',
  `value` varchar(255) NOT NULL DEFAULT '',
  `update_time` datetime DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `index_key` (`key`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of w5_setting
-- ----------------------------
BEGIN;
INSERT INTO `w5_setting` VALUES (1, 'w5_key', 'W5_is_an_open_source_SOAR_product', '2020-12-02 21:16:15', '2020-11-29 00:32:15');
INSERT INTO `w5_setting` VALUES (2, 'api_key', '', '2020-12-05 18:40:05', '2020-12-05 18:14:56');
COMMIT;

-- ----------------------------
-- Table structure for w5_type
-- ----------------------------
DROP TABLE IF EXISTS `w5_type`;
CREATE TABLE `w5_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` int(2) NOT NULL DEFAULT '1',
  `name` varchar(20) NOT NULL DEFAULT '',
  `update_time` datetime DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of w5_type
-- ----------------------------
BEGIN;
INSERT INTO `w5_type` VALUES (1, 1, '默认剧本', '2020-12-07 11:04:07', '2020-12-07 11:04:09');
INSERT INTO `w5_type` VALUES (2, 2, '默认变量', '2020-12-07 11:04:16', '2020-12-07 11:04:18');
COMMIT;

-- ----------------------------
-- Table structure for w5_users
-- ----------------------------
DROP TABLE IF EXISTS `w5_users`;
CREATE TABLE `w5_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `account` varchar(20) NOT NULL DEFAULT '',
  `passwd` varchar(32) NOT NULL DEFAULT '',
  `nick_name` varchar(20) NOT NULL DEFAULT '',
  `email` varchar(50) NOT NULL DEFAULT '',
  `token` varchar(32) NOT NULL DEFAULT '',
  `status` int(11) NOT NULL DEFAULT '0',
  `update_time` datetime DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `index_account` (`account`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of w5_users
-- ----------------------------
BEGIN;
INSERT INTO `w5_users` VALUES (1, 'admin', 'F38AFA9E15326959EF26DE613E821115', 'W5', 'admin@w5.io', '178E21C9907F568647717A00D004DDC1', 0, '2020-12-07 10:11:28', '2020-12-03 13:57:45');
COMMIT;

-- ----------------------------
-- Table structure for w5_variablen
-- ----------------------------
DROP TABLE IF EXISTS `w5_variablen`;
CREATE TABLE `w5_variablen` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type_id` int(11) NOT NULL DEFAULT '0',
  `key` varchar(20) NOT NULL DEFAULT '',
  `value` varchar(255) NOT NULL DEFAULT '',
  `remarks` varchar(255) NOT NULL DEFAULT '',
  `status` int(11) NOT NULL DEFAULT '0',
  `update_time` datetime DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `index.key` (`key`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of w5_variablen
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for w5_version
-- ----------------------------
DROP TABLE IF EXISTS `w5_version`;
CREATE TABLE `w5_version` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL DEFAULT '',
  `version` varchar(255) NOT NULL DEFAULT '',
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of w5_version
-- ----------------------------
BEGIN;
INSERT INTO `w5_version` VALUES (1, 'w5', '0.1', '2020-12-07 10:10:56');
INSERT INTO `w5_version` VALUES (2, 'apps', '0.1', '2020-12-07 10:10:56');
COMMIT;

-- ----------------------------
-- Table structure for w5_workflow
-- ----------------------------
DROP TABLE IF EXISTS `w5_workflow`;
CREATE TABLE `w5_workflow` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(100) NOT NULL DEFAULT '',
  `user_id` int(11) NOT NULL DEFAULT '0',
  `type_id` int(11) NOT NULL DEFAULT '0',
  `name` varchar(50) NOT NULL DEFAULT '',
  `remarks` varchar(255) NOT NULL DEFAULT '',
  `status` int(11) NOT NULL DEFAULT '0',
  `start_app` varchar(100) NOT NULL DEFAULT '',
  `end_app` varchar(100) NOT NULL DEFAULT '',
  `input_app` varchar(100) NOT NULL DEFAULT '',
  `webhook_app` varchar(100) NOT NULL DEFAULT '',
  `flow_json` text NOT NULL,
  `flow_data` text NOT NULL,
  `controller_data` text,
  `local_var_data` text,
  `update_time` datetime DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `index_uuid` (`uuid`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of w5_workflow
-- ----------------------------
BEGIN;
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
