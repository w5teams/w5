create database w5_db DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_general_ci;
flush privileges;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;
USE w5_db;

-- ----------------------------
-- Table structure for w5_login_history
-- ----------------------------
DROP TABLE IF EXISTS `w5_login_history`;
CREATE TABLE `w5_login_history` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL DEFAULT '0',
  `login_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of w5_login_history
-- ----------------------------
BEGIN;
COMMIT;

DROP TABLE IF EXISTS `w5_audit`;
CREATE TABLE `w5_audit` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `workflow_uuid` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `only_id` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `user_id` int NOT NULL DEFAULT '0',
  `audit_app` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `start_app` varchar(100) COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `status` int NOT NULL DEFAULT '0',
  `update_time` datetime DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

BEGIN;
COMMIT;

DROP TABLE IF EXISTS `w5_nav`;
CREATE TABLE `w5_nav` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `key` varchar(255) COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `icon` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `is_menu` int NOT NULL DEFAULT '0',
  `up` int NOT NULL DEFAULT '0',
  `order` int NOT NULL DEFAULT '0',
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS `w5_role`;
CREATE TABLE `w5_role` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(20) COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `remarks` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `update_time` datetime DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS `w5_role_nav`;
CREATE TABLE `w5_role_nav` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `role_id` int NOT NULL DEFAULT '0',
  `nav_id` int NOT NULL DEFAULT '0',
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS `w5_user_role`;
CREATE TABLE `w5_user_role` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL DEFAULT '0',
  `role_id` int NOT NULL DEFAULT '0',
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `w5_nav` (`id`, `name`, `path`, `key`, `icon`, `is_menu`, `up`, `order`, `create_time`) VALUES
(1, '仪表盘', '/dashboard', 'Dashboard', 'dashboard', 1, 0, 1, '2021-12-25 15:44:37'),
(2, '剧本列表', '/workflow', 'WorkflowHome', 'cloud-sync', 1, 0, 2, '2021-12-25 15:45:33'),
(3, '剧本编辑', '/workflow/edit/', 'WorkflowEdit', '', 2, 0, 0, '2021-12-25 15:49:58'),
(4, '执行日志', '/logs', 'LogsHome', 'bug', 1, 0, 4, '2021-12-25 15:50:03'),
(5, '应用中心', '/app', 'AppHome', 'appstore', 1, 0, 5, '2021-12-25 15:50:03'),
(6, '全局变量', '/variablen', 'VariablenHome', 'gold', 1, 0, 7, '2021-12-25 15:51:43'),
(7, '用户管理', '/user', 'UserHome', 'user', 1, 0, 8, '2021-12-25 15:51:43'),
(8, '系统管理', '/system', 'SystemHome', 'setting', 1, 0, 9, '2021-12-25 15:51:43'),
(9, '任务调度', '/timer', 'TimerHome', 'cluster', 1, 0, 3, '2021-12-25 15:51:43'),
(10, '人工审计', '/audit', 'AuditHome', 'audit', 1, 0, 6, '2021-12-25 15:51:43');

INSERT INTO `w5_role` (`id`, `name`, `remarks`, `update_time`, `create_time`) VALUES
(1, '系统管理员', '用于维护系统的角色组', '2021-12-26 17:52:44', '2021-12-26 17:52:44');

INSERT INTO `w5_role_nav` (`id`, `role_id`, `nav_id`, `create_time`) VALUES
(1, 1, 3, '2021-12-26 17:52:44'),
(2, 1, 1, '2021-12-26 17:52:44'),
(3, 1, 2, '2021-12-26 17:52:44'),
(4, 1, 9, '2021-12-26 17:52:44'),
(5, 1, 4, '2021-12-26 17:52:44'),
(6, 1, 5, '2021-12-26 17:52:44'),
(7, 1, 10, '2021-12-26 17:52:44'),
(8, 1, 6, '2021-12-26 17:52:44'),
(9, 1, 7, '2021-12-26 17:52:44'),
(10, 1, 8, '2021-12-26 17:52:44');

INSERT INTO `w5_user_role` (`id`, `user_id`, `role_id`, `create_time`) VALUES
(1, 1, 1, '2021-12-26 17:53:13');

-- ----------------------------
-- Table structure for w5_logs
-- ----------------------------
DROP TABLE IF EXISTS `w5_logs`;
CREATE TABLE `w5_logs` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `only_id` varchar(30) NOT NULL DEFAULT '',
  `uuid` varchar(100) NOT NULL,
  `app_uuid` varchar(100) NOT NULL,
  `app_name` varchar(20) NOT NULL DEFAULT '',
  `result` text NOT NULL,
  `status` int NOT NULL DEFAULT '0',
  `html` text,
  `args` text,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of w5_logs
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for w5_report
-- ----------------------------
DROP TABLE IF EXISTS `w5_report`;
CREATE TABLE `w5_report` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `report_no` varchar(30) NOT NULL DEFAULT '',
  `workflow_name` varchar(50) NOT NULL DEFAULT '',
  `remarks` varchar(255) NOT NULL DEFAULT '',
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of w5_report
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for w5_setting
-- ----------------------------
DROP TABLE IF EXISTS `w5_setting`;
CREATE TABLE `w5_setting` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `key` varchar(255) NOT NULL DEFAULT '',
  `value` varchar(255) NOT NULL DEFAULT '',
  `update_time` datetime DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `index_key` (`key`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of w5_setting
-- ----------------------------
BEGIN;
INSERT INTO `w5_setting` VALUES (1, 'w5_key', '', '2021-03-28 17:55:45', '2020-11-29 00:32:15');
INSERT INTO `w5_setting` VALUES (2, 'api_key', '', '2021-04-26 16:15:51', '2020-12-05 18:14:56');
INSERT INTO `w5_setting` VALUES (3, 'placement', 'right', '2021-04-26 16:15:51', '2020-12-05 18:14:56');
COMMIT;

-- ----------------------------
-- Table structure for w5_timer
-- ----------------------------
DROP TABLE IF EXISTS `w5_timer`;
CREATE TABLE `w5_timer` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `timer_uuid` varchar(100) NOT NULL DEFAULT '',
  `uuid` varchar(100) NOT NULL DEFAULT '',
  `type` varchar(10) NOT NULL DEFAULT '',
  `interval_type` varchar(10) NOT NULL DEFAULT '',
  `time` varchar(50) NOT NULL DEFAULT '',
  `start_date` varchar(50) NOT NULL DEFAULT '',
  `end_date` varchar(50) NOT NULL DEFAULT '',
  `jitter` int NOT NULL DEFAULT '0',
  `status` int NOT NULL DEFAULT '0',
  `update_time` datetime DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uid` (`timer_uuid`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of w5_timer
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for w5_type
-- ----------------------------
DROP TABLE IF EXISTS `w5_type`;
CREATE TABLE `w5_type` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `type` int NOT NULL DEFAULT '1' ,
  `name` varchar(20) NOT NULL DEFAULT '',
  `update_time` datetime DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of w5_type
-- ----------------------------
BEGIN;
INSERT INTO `w5_type` VALUES (1, 1, '默认剧本', '2021-11-28 15:18:01', '2021-11-28 15:18:03');
INSERT INTO `w5_type` VALUES (2, 2, '默认变量', '2021-11-28 15:18:14', '2021-11-28 15:18:16');
COMMIT;

-- ----------------------------
-- Table structure for w5_users
-- ----------------------------
DROP TABLE IF EXISTS `w5_users`;
CREATE TABLE `w5_users` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `account` varchar(20) NOT NULL DEFAULT '',
  `passwd` varchar(32) NOT NULL DEFAULT '',
  `nick_name` varchar(20) NOT NULL DEFAULT '',
  `avatar` text,
  `email` varchar(50) NOT NULL DEFAULT '',
  `token` varchar(32) NOT NULL DEFAULT '',
  `status` int NOT NULL DEFAULT '0',
  `update_time` datetime DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `index_account` (`account`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of w5_users
-- ----------------------------
BEGIN;
INSERT INTO `w5_users` VALUES (1, 'admin', 'F38AFA9E15326959EF26DE613E821115', 'W5', '<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 231 231\"><path d=\"M33.83,33.83a115.5,115.5,0,1,1,0,163.34,115.49,115.49,0,0,1,0-163.34Z\" style=\"fill:#386465;\"/><path d=\"m115.5 51.75a63.75 63.75 0 0 0-10.5 126.63v14.09a115.5 115.5 0 0 0-53.729 19.027 115.5 115.5 0 0 0 128.46 0 115.5 115.5 0 0 0-53.729-19.029v-14.084a63.75 63.75 0 0 0 53.25-62.881 63.75 63.75 0 0 0-63.65-63.75 63.75 63.75 0 0 0-0.09961 0z\" style=\"fill:#fae3b9;\"/><path d=\"m91.92 194.41a101.47 101.47 0 0 1 23.58 17.09 101.47 101.47 0 0 1 23.58-17.09c0.89 0.19 1.78 0.38 2.67 0.59a114.79 114.79 0 0 1 38 16.5 115.53 115.53 0 0 1-128.46 0 114.79 114.79 0 0 1 38-16.5c0.88-0.21 1.78-0.4 2.67-0.59z\" style=\"fill:#708913;\"/><path d=\"m73.65 199.82c16.59 8.23 28.72 18.91 34.27 30.93a114.86 114.86 0 0 1-56.65-19.25 115.06 115.06 0 0 1 22.38-11.68z\" style=\"fill:#fdea14;\"/><path d=\"m60.63 205.85c12.35 5.94 21.93 13.44 27.59 21.91a114.7 114.7 0 0 1-36.95-16.26q4.53-3 9.36-5.65z\" style=\"fill:#708913;\"/><path d=\"m157.35 199.82c-16.6 8.23-28.72 18.91-34.27 30.93a114.86 114.86 0 0 0 56.65-19.25 115.06 115.06 0 0 0-22.38-11.68z\" style=\"fill:#fdea14;\"/><path d=\"m170.37 205.85c-12.35 5.94-21.93 13.44-27.59 21.91a114.7 114.7 0 0 0 36.95-16.26q-4.53-3-9.36-5.65z\" style=\"fill:#708913;\"/><path d=\"m137.38 11.148c-12.23 1.9593-18.511 14.606-43.436 9.4915-11.285-3.2054-16.406-3.573-20.389 0.58594-4.1548 4.3384-7.033 12.435-9.8184 21.706-2.1354 7.4136-3.7187 14.381-4.7461 21.646h112.7c-3.4878-24.293-10.822-43.281-25.182-51.061-3.5314-1.623-6.5274-2.2959-9.1289-2.3613z\" style=\"fill:#27363C;\"/><path d=\"m114.37 43.383c-19.445 0.088-38.524 2.0724-52.379 5.6992-1.2766 4.5795-2.4317 10.169-3.2285 16.807h113.11c-0.83731-6.0107-1.9164-11.674-3.3184-16.924-15.229-3.8842-34.873-5.6693-54.18-5.582z\" style=\"fill:#5DCAD4;\"/><path d=\"m115.5 55.773c-58.39 0-105.73 15.476-105.73 34.57h0.0312c0 11.295 16.496 21.319 42.126 27.627-0.10331-7.7704 2.788-21.904 5.2734-31.031 6.0935-1.7168 6.9294-1.8971 13.167-2.9919 14.874-2.8256 29.99-4.2037 45.133-4.1153 15.143-0.0884 30.259 1.2897 45.133 4.1153 6.2372 1.0947 7.2065 1.2751 13.3 2.9919 2.4854 9.1267 5.3768 23.26 5.2734 31.031 25.63-6.3082 41.993-16.332 41.993-27.627h0.0312c0-19.093-47.34-34.57-105.73-34.57z\" style=\"fill:#314652;\"/><path d=\"m72.088 83.533c-6.9765 1.1147-13.357 2.856-18.439 4.3477-1.1861 7.415-2.0038 18.858-1.8926 26.293 4.3278-0.62795 10.155-1.3644 13.295-1.6465-0.40554 0.30198 2.7344-17.827 7.0371-28.994zm86.824 0c4.3028 11.167 7.4426 29.296 7.0371 28.994 3.1396 0.28213 8.9671 1.0185 13.295 1.6465 0.11119-7.4351-0.70652-18.878-1.8926-26.293-5.0822-1.4916-11.463-3.2329-18.439-4.3477z\" style=\"fill:#333;\"/><path d=\"m97.56 107.84a10.63 10.63 0 0 1-15 0.13l-0.13-0.13\" style=\"fill:none;stroke-linecap:round;stroke-linejoin:round;stroke-width:6.3px;stroke:#000;\"/><path d=\"m148.59 107.84a10.63 10.63 0 0 1-15 0.13l-0.13-0.13\" style=\"fill:none;stroke-linecap:round;stroke-linejoin:round;stroke-width:6.3px;stroke:#000;\"/><path d=\"m118.05 148.38c-1.5064 0.59192-2.595 2.0264-2.6191 3.9863-0.0574 1.3977 0.53421 3.5611 3.6758 5.7949 8.0544 4.9446 21.507 3.6862 21.255-7.1658-4.664 4.8219-10.021 5.6377-14.773 0.73907-1.2328-1.1599-2.3694-2.4032-3.9294-3.1408-1.0946-0.50424-2.2257-0.61071-3.6096-0.21337z\" style=\"fill:#50230a;\"/><path d=\"m133.61 154.93c3.0731-0.48816 5.5702-2.8457 5.4438-4.5059-0.47801-4.8311-5.7317-3.0917-4.3369-0.31405-2.8103-1.4445-1.8343-3.8862 0.50427-4.7324 2.0509-0.79942 5.0937 0.34314 6.2002 2.6376 2.2229 7.3422-3.4376 11.68-10.384 12.561z\" style=\"fill:#50230a;\"/><path d=\"m112.81 148.38c1.5064 0.59192 2.595 2.0264 2.6191 3.9863 0.0574 1.3977-0.53421 3.5611-3.6758 5.7949-8.0544 4.9446-21.507 3.6862-21.255-7.1658 4.664 4.8219 10.021 5.6377 14.773 0.73907 1.2328-1.1599 2.3694-2.4032 3.9294-3.1408 1.0946-0.50424 2.2257-0.61071 3.6096-0.21337z\" style=\"fill:#50230a;\"/><path d=\"m97.252 154.93c-3.0731-0.48816-5.5702-2.8457-5.4438-4.5059 0.47801-4.8311 5.7317-3.0917 4.3369-0.31405 2.8103-1.4445 1.8343-3.8862-0.50427-4.7324-2.0509-0.79942-5.0937 0.34314-6.2002 2.6376-2.2229 7.3422 3.4376 11.68 10.384 12.561z\" style=\"fill:#50230a;\"/></svg>', 'admin@w5.io', '34B7AC6D9470D5A64332C79129ACCDD9', 0, '2021-11-28 14:21:06', '2020-12-03 13:57:45');
COMMIT;

-- ----------------------------
-- Table structure for w5_variablen
-- ----------------------------
DROP TABLE IF EXISTS `w5_variablen`;
CREATE TABLE `w5_variablen` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `type_id` int NOT NULL DEFAULT '0',
  `key` varchar(20) NOT NULL DEFAULT '',
  `value` varchar(255) NOT NULL DEFAULT '',
  `remarks` varchar(255) NOT NULL DEFAULT '',
  `status` int NOT NULL DEFAULT '0',
  `update_time` datetime DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `index.key` (`key`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of w5_variablen
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for w5_workflow
-- ----------------------------
DROP TABLE IF EXISTS `w5_workflow`;
CREATE TABLE `w5_workflow` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `uuid` varchar(100) NOT NULL DEFAULT '',
  `user_id` int NOT NULL DEFAULT '0',
  `type_id` int NOT NULL DEFAULT '0',
  `name` varchar(50) NOT NULL DEFAULT '',
  `remarks` varchar(255) NOT NULL DEFAULT '',
  `status` int NOT NULL DEFAULT '0',
  `start_app` varchar(100) NOT NULL DEFAULT '',
  `end_app` varchar(100) NOT NULL DEFAULT '',
  `input_app` varchar(100) NOT NULL DEFAULT '',
  `webhook_app` varchar(100) NOT NULL DEFAULT '',
  `timer_app` varchar(100) NOT NULL DEFAULT '',
  `for_list` text,
  `if_list` text,
  `audit_list` text,
  `flow_json` text,
  `flow_data` text,
  `controller_data` text,
  `local_var_data` text,
  `grid_type` varchar(10) NOT NULL DEFAULT '',
  `edge_marker` varchar(10) NOT NULL DEFAULT '',
  `edge_color` varchar(10) NOT NULL DEFAULT '',
  `edge_connector` varchar(10) NOT NULL DEFAULT '',
  `edge_router` varchar(10) NOT NULL DEFAULT '',
  `update_time` datetime DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `index_uuid` (`uuid`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of w5_workflow
-- ----------------------------
BEGIN;
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;