-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Dec 08, 2025 at 05:03 PM
-- Server version: 8.3.0
-- PHP Version: 8.2.18

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `mentormentee`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_group_id_b120cbf9` (`group_id`),
  KEY `auth_group_permissions_permission_id_84c5c92e` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  KEY `auth_permission_content_type_id_2f476e4b` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=73 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add admin', 7, 'add_admin'),
(26, 'Can change admin', 7, 'change_admin'),
(27, 'Can delete admin', 7, 'delete_admin'),
(28, 'Can view admin', 7, 'view_admin'),
(29, 'Can add department', 8, 'add_department'),
(30, 'Can change department', 8, 'change_department'),
(31, 'Can delete department', 8, 'delete_department'),
(32, 'Can view department', 8, 'view_department'),
(33, 'Can add faculty', 9, 'add_faculty'),
(34, 'Can change faculty', 9, 'change_faculty'),
(35, 'Can delete faculty', 9, 'delete_faculty'),
(36, 'Can view faculty', 9, 'view_faculty'),
(37, 'Can add login', 10, 'add_login'),
(38, 'Can change login', 10, 'change_login'),
(39, 'Can delete login', 10, 'delete_login'),
(40, 'Can view login', 10, 'view_login'),
(41, 'Can add student', 11, 'add_student'),
(42, 'Can change student', 11, 'change_student'),
(43, 'Can delete student', 11, 'delete_student'),
(44, 'Can view student', 11, 'view_student'),
(45, 'Can add mentoring session', 12, 'add_mentoringsession'),
(46, 'Can change mentoring session', 12, 'change_mentoringsession'),
(47, 'Can delete mentoring session', 12, 'delete_mentoringsession'),
(48, 'Can view mentoring session', 12, 'view_mentoringsession'),
(49, 'Can add mentor assignment log', 13, 'add_mentorassignmentlog'),
(50, 'Can change mentor assignment log', 13, 'change_mentorassignmentlog'),
(51, 'Can delete mentor assignment log', 13, 'delete_mentorassignmentlog'),
(52, 'Can view mentor assignment log', 13, 'view_mentorassignmentlog'),
(53, 'Can add courses', 14, 'add_courses'),
(54, 'Can change courses', 14, 'change_courses'),
(55, 'Can delete courses', 14, 'delete_courses'),
(56, 'Can view courses', 14, 'view_courses'),
(57, 'Can add batches', 15, 'add_batches'),
(58, 'Can change batches', 15, 'change_batches'),
(59, 'Can delete batches', 15, 'delete_batches'),
(60, 'Can view batches', 15, 'view_batches'),
(61, 'Can add schedule', 16, 'add_schedule'),
(62, 'Can change schedule', 16, 'change_schedule'),
(63, 'Can delete schedule', 16, 'delete_schedule'),
(64, 'Can view schedule', 16, 'view_schedule'),
(65, 'Can add session request', 17, 'add_sessionrequest'),
(66, 'Can change session request', 17, 'change_sessionrequest'),
(67, 'Can delete session request', 17, 'delete_sessionrequest'),
(68, 'Can view session request', 17, 'view_sessionrequest'),
(69, 'Can add student uploads', 18, 'add_studentuploads'),
(70, 'Can change student uploads', 18, 'change_studentuploads'),
(71, 'Can delete student uploads', 18, 'delete_studentuploads'),
(72, 'Can view student uploads', 18, 'view_studentuploads');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$1000000$99OICkEVRSI5BiDRKe78oO$C81jvEyBiIh9KpjzUXhb69+0Vt4UK6mIu40Jw8IfFBI=', '2025-12-04 06:10:00.402203', 1, 'kishore', '', '', 'kishor.mullappilly@gmail.com', 1, 1, '2025-12-04 06:09:43.386840');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_user_id_6a12ed8b` (`user_id`),
  KEY `auth_user_groups_group_id_97559544` (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_user_id_a95ead1b` (`user_id`),
  KEY `auth_user_user_permissions_permission_id_1fbb5f2c` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6` (`user_id`)
) ;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=MyISAM AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(2, 'auth', 'permission'),
(3, 'auth', 'group'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session'),
(7, 'MentorMentee', 'admin'),
(8, 'MentorMentee', 'department'),
(9, 'MentorMentee', 'faculty'),
(10, 'MentorMentee', 'login'),
(11, 'MentorMentee', 'student'),
(12, 'MentorMentee', 'mentoringsession'),
(13, 'MentorMentee', 'mentorassignmentlog'),
(14, 'MentorMentee', 'courses'),
(15, 'MentorMentee', 'batches'),
(16, 'MentorMentee', 'schedule'),
(17, 'MentorMentee', 'sessionrequest'),
(18, 'MentorMentee', 'studentuploads');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-11-27 17:31:39.069673'),
(2, 'auth', '0001_initial', '2025-11-27 17:31:39.570879'),
(3, 'MentorMentee', '0001_initial', '2025-11-27 17:31:40.363612'),
(4, 'MentorMentee', '0002_remove_admin_user_remove_faculty_user', '2025-11-27 17:31:40.488813'),
(5, 'MentorMentee', '0003_courses', '2025-11-27 17:31:40.551750'),
(6, 'MentorMentee', '0004_student_course', '2025-11-27 17:31:40.606810'),
(7, 'MentorMentee', '0005_remove_student_course', '2025-11-27 17:31:40.654173'),
(8, 'MentorMentee', '0006_student_course', '2025-11-27 17:31:40.711596'),
(9, 'MentorMentee', '0007_remove_student_created_at_student_dob', '2025-11-27 17:31:40.772755'),
(10, 'MentorMentee', '0008_batches', '2025-11-27 17:31:40.830619'),
(11, 'MentorMentee', '0009_student_batch', '2025-11-27 17:31:40.902616'),
(12, 'MentorMentee', '0010_student_student_image', '2025-11-27 17:31:40.943912'),
(13, 'MentorMentee', '0011_remove_faculty_created_at', '2025-11-27 17:31:40.972999'),
(14, 'MentorMentee', '0012_faculty_faculty_image', '2025-11-27 17:31:41.018949'),
(15, 'MentorMentee', '0013_admin_admin_image', '2025-11-27 17:31:41.058687'),
(16, 'MentorMentee', '0014_mentoringsession_date_mentoringsession_details_and_more', '2025-11-27 17:31:41.224433'),
(17, 'MentorMentee', '0015_remove_mentoringsession_session_date', '2025-11-27 17:31:41.255066'),
(18, 'MentorMentee', '0016_remove_mentoringsession_action_plan_and_more', '2025-11-27 17:31:41.444302'),
(19, 'MentorMentee', '0017_rename_summary_mentoringsession_academic_details_and_more', '2025-11-27 17:31:41.492112'),
(20, 'admin', '0001_initial', '2025-11-27 17:31:41.661743'),
(21, 'admin', '0002_logentry_remove_auto_add', '2025-11-27 17:31:41.669126'),
(22, 'admin', '0003_logentry_add_action_flag_choices', '2025-11-27 17:31:41.676402'),
(23, 'contenttypes', '0002_remove_content_type_name', '2025-11-27 17:31:41.739753'),
(24, 'auth', '0002_alter_permission_name_max_length', '2025-11-27 17:31:41.769133'),
(25, 'auth', '0003_alter_user_email_max_length', '2025-11-27 17:31:41.800322'),
(26, 'auth', '0004_alter_user_username_opts', '2025-11-27 17:31:41.806250'),
(27, 'auth', '0005_alter_user_last_login_null', '2025-11-27 17:31:41.835658'),
(28, 'auth', '0006_require_contenttypes_0002', '2025-11-27 17:31:41.836727'),
(29, 'auth', '0007_alter_validators_add_error_messages', '2025-11-27 17:31:41.842290'),
(30, 'auth', '0008_alter_user_username_max_length', '2025-11-27 17:31:41.872675'),
(31, 'auth', '0009_alter_user_last_name_max_length', '2025-11-27 17:31:41.900200'),
(32, 'auth', '0010_alter_group_name_max_length', '2025-11-27 17:31:41.929225'),
(33, 'auth', '0011_update_proxy_permissions', '2025-11-27 17:31:41.941853'),
(34, 'auth', '0012_alter_user_first_name_max_length', '2025-11-27 17:31:41.970092'),
(35, 'sessions', '0001_initial', '2025-11-27 17:31:42.005644'),
(36, 'MentorMentee', '0018_student_login', '2025-11-28 06:32:36.631220'),
(37, 'MentorMentee', '0019_schedule', '2025-11-29 13:34:48.825700'),
(38, 'MentorMentee', '0020_alter_schedule_status_sessionrequest', '2025-11-30 15:45:41.410320'),
(39, 'MentorMentee', '0021_sessionrequest_comments', '2025-11-30 16:09:55.398392'),
(40, 'MentorMentee', '0022_studentuploads', '2025-12-02 10:33:30.791031');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('mwsa78vf0wynb3pf1qpy0e0pr48xio0d', 'eyJsb2dpbl9pZCI6Mn0:1vOBbI:G5YzNizH9LVErVjVmM3NqrmzkFHiR0fZ_hEfGlGLvJI', '2025-12-10 09:14:12.245000'),
('yfk1jvx2kkybvse8ju48p3qxlh8kxq40', 'eyJsb2dpbl9pZCI6MX0:1vR1CG:aqesMd2DIC-1lYC0kKkrqARqSuuu3-ITSKze5xEWm-c', '2025-12-18 04:44:04.167249'),
('msh4sw64qsv5myp78581o3oq9wnvj8di', '.eJxVjDkOgzAQAP-ydWR5F-ODMj1vQD7WQIJsiaOK8veIiIZ2ZjQfWOo4l2FO0KF7wOCPfRqOjdc_AoQbCz6-uZwivXwZq4i17OscxJmIy26ir4mX59XeBpPfJuhAspPokSgl1BJjSzqnQNGzkoyBdCPRGiIdkZQzmRpF2UZndIvKWobvD8_cOvQ:1vR2XQ:SH0jgEXCMp7VLTPTXxcmed0KD2s8JjObDuyUOje-pis', '2025-12-18 06:10:00.412626');

-- --------------------------------------------------------

--
-- Table structure for table `mentormentee_admin`
--

DROP TABLE IF EXISTS `mentormentee_admin`;
CREATE TABLE IF NOT EXISTS `mentormentee_admin` (
  `admin_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `department_id` int DEFAULT NULL,
  `login_id` int NOT NULL,
  `admin_image` varchar(500) NOT NULL,
  PRIMARY KEY (`admin_id`),
  KEY `MentorMentee_admin_department_id_f4e24400` (`department_id`),
  KEY `MentorMentee_admin_login_id_257fe5a6` (`login_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `mentormentee_admin`
--

INSERT INTO `mentormentee_admin` (`admin_id`, `name`, `email`, `created_at`, `department_id`, `login_id`, `admin_image`) VALUES
(1, 'Ms. Priyanka', 'priyanka@rajagiri.edu', '2025-11-26 01:05:18.000000', 1, 1, '');

-- --------------------------------------------------------

--
-- Table structure for table `mentormentee_batches`
--

DROP TABLE IF EXISTS `mentormentee_batches`;
CREATE TABLE IF NOT EXISTS `mentormentee_batches` (
  `batch_id` int NOT NULL AUTO_INCREMENT,
  `batch_name` varchar(30) NOT NULL,
  `course_id` int NOT NULL,
  PRIMARY KEY (`batch_id`),
  KEY `MentorMentee_batches_course_id_fa2274b0` (`course_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `mentormentee_batches`
--

INSERT INTO `mentormentee_batches` (`batch_id`, `batch_name`, `course_id`) VALUES
(1, 'MCA 25-27', 1),
(2, 'MSC CS 25-27', 2);

-- --------------------------------------------------------

--
-- Table structure for table `mentormentee_courses`
--

DROP TABLE IF EXISTS `mentormentee_courses`;
CREATE TABLE IF NOT EXISTS `mentormentee_courses` (
  `course_id` int NOT NULL AUTO_INCREMENT,
  `course_name` varchar(20) NOT NULL,
  `department_id` int NOT NULL,
  PRIMARY KEY (`course_id`),
  KEY `MentorMentee_courses_department_id_cfd45fed` (`department_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `mentormentee_courses`
--

INSERT INTO `mentormentee_courses` (`course_id`, `course_name`, `department_id`) VALUES
(1, 'MCA', 1),
(2, 'Msc. CS (DA)', 1);

-- --------------------------------------------------------

--
-- Table structure for table `mentormentee_department`
--

DROP TABLE IF EXISTS `mentormentee_department`;
CREATE TABLE IF NOT EXISTS `mentormentee_department` (
  `dept_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `code` varchar(20) NOT NULL,
  `hod_name` varchar(100) DEFAULT NULL,
  `email` varchar(254) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`dept_id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `mentormentee_department`
--

INSERT INTO `mentormentee_department` (`dept_id`, `name`, `code`, `hod_name`, `email`, `created_at`) VALUES
(1, 'Computer Science', 'CS', 'Dr. Bindhya M Varghese', 'bindhya@rajagiri.edu', '2025-11-26 01:06:22.000000'),
(2, 'Commerce', 'CM', 'Dr. Name', 'name@rajagiri.edu', '2025-11-26 14:10:04.000000');

-- --------------------------------------------------------

--
-- Table structure for table `mentormentee_faculty`
--

DROP TABLE IF EXISTS `mentormentee_faculty`;
CREATE TABLE IF NOT EXISTS `mentormentee_faculty` (
  `faculty_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `designation` varchar(100) DEFAULT NULL,
  `department_id` int NOT NULL,
  `login_id` int NOT NULL,
  `faculty_image` varchar(500) NOT NULL,
  PRIMARY KEY (`faculty_id`),
  KEY `MentorMentee_faculty_department_id_56849c4d` (`department_id`),
  KEY `MentorMentee_faculty_login_id_9ea42aa8` (`login_id`)
) ENGINE=MyISAM AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `mentormentee_faculty`
--

INSERT INTO `mentormentee_faculty` (`faculty_id`, `name`, `email`, `phone`, `designation`, `department_id`, `login_id`, `faculty_image`) VALUES
(1, 'Diljith K Benny', 'diljith@rajagiri.edu', NULL, 'Assistant Professor', 1, 2, ''),
(2, 'Dr. Jaya Vijayan', 'jaya@rajagiri.edu', NULL, 'Assistant Professor', 1, 3, ''),
(3, 'Dr. Ann Baby', 'ann@rajagiri.edu', NULL, 'Assistant Professor', 1, 5, ''),
(4, 'Dr. Shiju Thomas M Y', 'shiju@rajagiri.edu', NULL, 'Assistant Professor', 1, 6, ''),
(5, 'Dr. Sabeen Govind', 'sabeen@rajagiri.edu', NULL, 'Assistant Professor', 1, 7, ''),
(6, 'Dr. Keerthy A S', 'keerthy@rajagiri.edu', NULL, 'Assistant Professor', 1, 8, ''),
(7, 'Ms. Neethu Narayanan', 'neethu@rajagiri.edu', NULL, 'Assistant Professor', 1, 9, ''),
(8, 'Ms. Priyanka E Thambi', 'priyanka@rajagiri.edu', NULL, 'Assistant Professor', 1, 10, ''),
(9, 'Ms. Ann Rija', 'annrija@rajagiri.edu', NULL, 'Assistant Professor', 1, 11, ''),
(10, 'Dr. Shoby Sunny', 'shoby@rajagiri.edu', NULL, 'Assistant Professor', 1, 12, ''),
(11, 'Ms. Sunu Fathima', 'sunufathima@rajagiri.edu', NULL, 'Assistant Professor', 1, 13, ''),
(12, 'Ms. Sunu Mary Abraham', 'sunu@rajagiri.edu', NULL, 'Assistant Professor', 1, 4, '');

-- --------------------------------------------------------

--
-- Table structure for table `mentormentee_login`
--

DROP TABLE IF EXISTS `mentormentee_login`;
CREATE TABLE IF NOT EXISTS `mentormentee_login` (
  `login_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(25) NOT NULL,
  `password` varchar(8) NOT NULL,
  `userType` varchar(10) NOT NULL,
  PRIMARY KEY (`login_id`)
) ENGINE=MyISAM AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `mentormentee_login`
--

INSERT INTO `mentormentee_login` (`login_id`, `username`, `password`, `userType`) VALUES
(1, 'admin', 'admin', 'admin'),
(2, 'Diljith', 'diljith', 'faculty'),
(3, 'Jaya', 'jaya', 'faculty'),
(4, 'Ann', 'ann', 'faculty'),
(5, 'Sunu', 'sunu', 'faculty'),
(6, 'Shiju', 'shiju', 'faculty'),
(7, 'Sabeen', 'sabeen', 'faculty'),
(8, 'Keerthy', 'keerthy', 'faculty'),
(9, 'Neethu', 'neethu', 'faculty'),
(10, 'Priyanka', 'priyanka', 'faculty'),
(11, 'Ann Rija', 'ann rija', 'faculty'),
(12, 'Shoby', 'shoby', 'faculty'),
(13, 'Sunu Fathima', 'sunu fat', 'faculty'),
(14, 'Admin', 'admin123', 'admin'),
(19, 'MCA0000', '1234', 'student');

-- --------------------------------------------------------

--
-- Table structure for table `mentormentee_mentorassignmentlog`
--

DROP TABLE IF EXISTS `mentormentee_mentorassignmentlog`;
CREATE TABLE IF NOT EXISTS `mentormentee_mentorassignmentlog` (
  `log_id` int NOT NULL AUTO_INCREMENT,
  `timestamp` datetime(6) NOT NULL,
  `changed_by_id` int DEFAULT NULL,
  `new_faculty_id` int DEFAULT NULL,
  `old_faculty_id` int DEFAULT NULL,
  `student_id` int NOT NULL,
  PRIMARY KEY (`log_id`),
  KEY `MentorMentee_mentorassignmentlog_changed_by_id_88473941` (`changed_by_id`),
  KEY `MentorMentee_mentorassignmentlog_new_faculty_id_3f15dc37` (`new_faculty_id`),
  KEY `MentorMentee_mentorassignmentlog_old_faculty_id_476f3874` (`old_faculty_id`),
  KEY `MentorMentee_mentorassignmentlog_student_id_891862dc` (`student_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `mentormentee_mentoringsession`
--

DROP TABLE IF EXISTS `mentormentee_mentoringsession`;
CREATE TABLE IF NOT EXISTS `mentormentee_mentoringsession` (
  `session_id` int NOT NULL AUTO_INCREMENT,
  `faculty_id` int NOT NULL,
  `student_id` int NOT NULL,
  `date` datetime(6) NOT NULL,
  `details` longtext,
  `academic_details` longtext,
  `title` longtext,
  PRIMARY KEY (`session_id`),
  KEY `MentorMentee_mentoringsession_faculty_id_37540114` (`faculty_id`),
  KEY `MentorMentee_mentoringsession_student_id_98a9bc1d` (`student_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `mentormentee_schedule`
--

DROP TABLE IF EXISTS `mentormentee_schedule`;
CREATE TABLE IF NOT EXISTS `mentormentee_schedule` (
  `schedule_id` int NOT NULL AUTO_INCREMENT,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `status` varchar(25) NOT NULL,
  `created_at` date NOT NULL,
  `batch_id` int NOT NULL,
  `created_by_id` int NOT NULL,
  PRIMARY KEY (`schedule_id`),
  KEY `MentorMentee_schedule_batch_id_c2f539cb` (`batch_id`),
  KEY `MentorMentee_schedule_created_by_id_33854e62` (`created_by_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `mentormentee_schedule`
--

INSERT INTO `mentormentee_schedule` (`schedule_id`, `start_date`, `end_date`, `status`, `created_at`, `batch_id`, `created_by_id`) VALUES
(1, '2025-12-01', '2025-12-05', 'active', '2025-11-29', 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `mentormentee_sessionrequest`
--

DROP TABLE IF EXISTS `mentormentee_sessionrequest`;
CREATE TABLE IF NOT EXISTS `mentormentee_sessionrequest` (
  `request_id` int NOT NULL AUTO_INCREMENT,
  `request_date` date NOT NULL,
  `status` varchar(25) NOT NULL,
  `session_date` date DEFAULT NULL,
  `session_time` time(6) DEFAULT NULL,
  `faculty_id` int NOT NULL,
  `student_id` int NOT NULL,
  `comments` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`request_id`),
  KEY `MentorMentee_sessionrequest_faculty_id_434c5d25` (`faculty_id`),
  KEY `MentorMentee_sessionrequest_student_id_9089f01a` (`student_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `mentormentee_student`
--

DROP TABLE IF EXISTS `mentormentee_student`;
CREATE TABLE IF NOT EXISTS `mentormentee_student` (
  `student_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `reg_no` varchar(10) NOT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `year` int NOT NULL,
  `department_id` int NOT NULL,
  `faculty_id` int DEFAULT NULL,
  `course_id` int NOT NULL,
  `dob` date DEFAULT NULL,
  `batch_id` int NOT NULL,
  `student_image` varchar(500) NOT NULL,
  `application_form` varchar(100) DEFAULT NULL,
  `assessment_file` varchar(100) DEFAULT NULL,
  `login_id` int DEFAULT NULL,
  PRIMARY KEY (`student_id`),
  UNIQUE KEY `reg_no` (`reg_no`),
  KEY `MentorMentee_student_department_id_4586e776` (`department_id`),
  KEY `MentorMentee_student_faculty_id_e95fd178` (`faculty_id`),
  KEY `MentorMentee_student_course_id_a5162afd` (`course_id`),
  KEY `MentorMentee_student_batch_id_a0b79d9f` (`batch_id`),
  KEY `MentorMentee_student_login_id_8bbccf99` (`login_id`)
) ENGINE=MyISAM AUTO_INCREMENT=63 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `mentormentee_student`
--

INSERT INTO `mentormentee_student` (`student_id`, `name`, `email`, `reg_no`, `phone`, `year`, `department_id`, `faculty_id`, `course_id`, `dob`, `batch_id`, `student_image`, `application_form`, `assessment_file`, `login_id`) VALUES
(1, 'ABHINAV B PRASAD', 'mca2501@rajagiri.edu', 'MCA2501', NULL, 1, 1, 2, 1, NULL, 1, '', '', '', NULL),
(2, 'ABHINAV MARTIN MATHEW', 'mca2502@rajagiri.edu', 'MCA2502', NULL, 1, 1, 11, 1, NULL, 1, '', '', '', NULL),
(3, 'AFWANA P NAZER', 'mca2503@rajagiri.edu', 'MCA2503', NULL, 1, 1, 7, 1, NULL, 1, '', '', '', NULL),
(4, 'AKASH SABU', 'mca2504@rajagiri.edu', 'MCA2504', NULL, 1, 1, 2, 1, NULL, 1, '', '', '', NULL),
(5, 'AKSHAY SHIBU', 'mca2505@rajagiri.edu', 'MCA2505', NULL, 1, 1, 12, 1, NULL, 1, '', '', '', NULL),
(6, 'ALAN SHAJI', 'mca2506@rajagiri.edu', 'MCA2506', NULL, 1, 1, 9, 1, NULL, 1, '', '', '', NULL),
(7, 'ALBERT C S', 'mca2507@rajagiri.edu', 'MCA2507', NULL, 1, 1, 7, 1, NULL, 1, '', '', '', NULL),
(8, 'ALBIN MAMMEN MATHEW', 'mca2508@rajagiri.edu', 'MCA2508', NULL, 1, 1, 1, 1, NULL, 1, '', '', '', NULL),
(9, 'AMINA MUHAMMED', 'mca2509@rajagiri.edu', 'MCA2509', NULL, 1, 1, 10, 1, NULL, 1, '', '', '', NULL),
(10, 'ANANDHU KRISHNA B', 'mca2510@rajagiri.edu', 'MCA2510', NULL, 1, 1, 6, 1, NULL, 1, '', '', '', NULL),
(11, 'ANASWARA PRASOBH', 'mca2511@rajagiri.edu', 'MCA2511', NULL, 1, 1, 9, 1, NULL, 1, '', '', '', NULL),
(12, 'ANN JO MATHEW', 'mca2512@rajagiri.edu', 'MCA2512', NULL, 1, 1, 5, 1, NULL, 1, '', '', '', NULL),
(13, 'ANN TREESA JIJO', 'mca2513@rajagiri.edu', 'MCA2513', NULL, 1, 1, 5, 1, NULL, 1, '', '', '', NULL),
(14, 'ANTONY JOE', 'mca2514@rajagiri.edu', 'MCA2514', NULL, 1, 1, 9, 1, NULL, 1, '', '', '', NULL),
(15, 'ANWIN JOJO', 'mca2515@rajagiri.edu', 'MCA2515', NULL, 1, 1, 4, 1, NULL, 1, '', '', '', NULL),
(16, 'ASHBI SAJU', 'mca2516@rajagiri.edu', 'MCA2516', NULL, 1, 1, 8, 1, NULL, 1, '', '', '', NULL),
(17, 'ATHIRA BINU', 'mca2517@rajagiri.edu', 'MCA2517', NULL, 1, 1, 4, 1, NULL, 1, '', '', '', NULL),
(18, 'BHADRA', 'mca2518@rajagiri.edu', 'MCA2518', NULL, 1, 1, 10, 1, NULL, 1, '', '', '', NULL),
(19, 'CHARLES SHAJU', 'mca2519@rajagiri.edu', 'MCA2519', NULL, 1, 1, 3, 1, NULL, 1, '', '', '', NULL),
(20, 'DAYA MATHEW', 'mca2520@rajagiri.edu', 'MCA2520', NULL, 1, 1, 10, 1, NULL, 1, '', '', '', NULL),
(21, 'DEVIKA B MENON', 'mca2521@rajagiri.edu', 'MCA2521', NULL, 1, 1, 4, 1, NULL, 1, '', '', '', NULL),
(22, 'DEVNA J', 'mca2522@rajagiri.edu', 'MCA2522', NULL, 1, 1, 3, 1, NULL, 1, '', '', '', NULL),
(23, 'DION SIJI KURIAKOSE', 'mca2523@rajagiri.edu', 'MCA2523', NULL, 1, 1, 5, 1, NULL, 1, '', '', '', NULL),
(24, 'DIYA MARY GEORGE', 'mca2524@rajagiri.edu', 'MCA2524', NULL, 1, 1, 3, 1, NULL, 1, '', '', '', NULL),
(25, 'EBIN LOUIS', 'mca2525@rajagiri.edu', 'MCA2525', NULL, 1, 1, 8, 1, NULL, 1, '', '', '', NULL),
(26, 'FARSAN SUNEER', 'mca2526@rajagiri.edu', 'MCA2526', NULL, 1, 1, 3, 1, NULL, 1, '', '', '', NULL),
(27, 'FEBIN SUNNY', 'mca2527@rajagiri.edu', 'MCA2527', NULL, 1, 1, 2, 1, NULL, 1, '', '', '', NULL),
(28, 'FERCINENT THOMAS', 'mca2528@rajagiri.edu', 'MCA2528', NULL, 1, 1, 1, 1, NULL, 1, '', '', '', NULL),
(29, 'GEETHIKA A', 'mca2529@rajagiri.edu', 'MCA2529', NULL, 1, 1, 7, 1, NULL, 1, '', '', '', NULL),
(30, 'HAFIZ MUHAMMED P H', 'mca2530@rajagiri.edu', 'MCA2530', NULL, 1, 1, 11, 1, NULL, 1, '', '', '', NULL),
(31, 'JASIN JOJI', 'mca2531@rajagiri.edu', 'MCA2531', NULL, 1, 1, 1, 1, NULL, 1, '', '', '', NULL),
(32, 'JEES THOMAS CLEETUS', 'mca2532@rajagiri.edu', 'MCA2532', NULL, 1, 1, 6, 1, NULL, 1, '', '', '', NULL),
(33, 'JIYO P V', 'mca2533@rajagiri.edu', 'MCA2533', NULL, 1, 1, 11, 1, NULL, 1, '', '', '', NULL),
(34, 'JOSEPH PAUL', 'mca2534@rajagiri.edu', 'MCA2534', NULL, 1, 1, 8, 1, NULL, 1, '', '', '', NULL),
(35, 'JUBIN JOY', 'mca2535@rajagiri.edu', 'MCA2535', NULL, 1, 1, 12, 1, NULL, 1, '', '', '', NULL),
(36, 'K JOSHUA JOEL', 'mca2536@rajagiri.edu', 'MCA2536', NULL, 1, 1, 5, 1, NULL, 1, '', '', '', NULL),
(37, 'KARTHIK KRISHNAN', 'mca2537@rajagiri.edu', 'MCA2537', NULL, 1, 1, 9, 1, NULL, 1, '', '', '', NULL),
(38, 'KISHORE M', 'mca2538@rajagiri.edu', 'MCA2538', NULL, 1, 1, 11, 1, NULL, 1, '', '', '', NULL),
(39, 'LENA MATHEW', 'mca2539@rajagiri.edu', 'MCA2539', NULL, 1, 1, 8, 1, NULL, 1, '', '', '', NULL),
(40, 'M S VISMAYA', 'mca2540@rajagiri.edu', 'MCA2540', NULL, 1, 1, 9, 1, NULL, 1, '', '', '', NULL),
(41, 'MAHADEVAN NAIR M P', 'mca2541@rajagiri.edu', 'MCA2541', NULL, 1, 1, 1, 1, NULL, 1, '', '', '', NULL),
(42, 'MARIA JOSE', 'mca2542@rajagiri.edu', 'MCA2542', NULL, 1, 1, 12, 1, NULL, 1, '', '', '', NULL),
(43, 'MEENADEVI RAVIKUMAR', 'mca2543@rajagiri.edu', 'MCA2543', NULL, 1, 1, 3, 1, NULL, 1, '', '', '', NULL),
(44, 'MERLIN XAVIER', 'mca2544@rajagiri.edu', 'MCA2544', NULL, 1, 1, 12, 1, NULL, 1, '', '', '', NULL),
(45, 'NANDHANA C S', 'mca2545@rajagiri.edu', 'MCA2545', NULL, 1, 1, 7, 1, NULL, 1, '', '', '', NULL),
(46, 'NOVELIA JOSEPH', 'mca2546@rajagiri.edu', 'MCA2546', NULL, 1, 1, 4, 1, NULL, 1, '', '', '', NULL),
(47, 'POOJA NAIR', 'mca2547@rajagiri.edu', 'MCA2547', NULL, 1, 1, 5, 1, NULL, 1, '', '', '', NULL),
(48, 'RENA ELZA VIJU', 'mca2548@rajagiri.edu', 'MCA2548', NULL, 1, 1, 12, 1, NULL, 1, '', '', '', NULL),
(49, 'ROBERT JOY', 'mca2549@rajagiri.edu', 'MCA2549', NULL, 1, 1, 10, 1, NULL, 1, '', '', '', NULL),
(50, 'ROSHA THANKACHAN', 'mca2550@rajagiri.edu', 'MCA2550', NULL, 1, 1, 6, 1, NULL, 1, '', '', '', NULL),
(51, 'SAM JOSEPH', 'mca2551@rajagiri.edu', 'MCA2551', NULL, 1, 1, 10, 1, NULL, 1, '', '', '', NULL),
(52, 'SANDRA B', 'mca2552@rajagiri.edu', 'MCA2552', NULL, 1, 1, 6, 1, NULL, 1, '', '', '', NULL),
(53, 'SHARVIN VINCENT', 'mca2553@rajagiri.edu', 'MCA2553', NULL, 1, 1, 2, 1, NULL, 1, '', '', '', NULL),
(54, 'SHYAM JAMES', 'mca2554@rajagiri.edu', 'MCA2554', NULL, 1, 1, 6, 1, NULL, 1, '', '', '', NULL),
(55, 'SIDDHARTH M V', 'mca2555@rajagiri.edu', 'MCA2555', NULL, 1, 1, 1, 1, NULL, 1, '', '', '', NULL),
(56, 'SREERAJ SREEKUMAR', 'mca2556@rajagiri.edu', 'MCA2556', NULL, 1, 1, 2, 1, NULL, 1, '', '', '', NULL),
(57, 'TOM GEO', 'mca2557@rajagiri.edu', 'MCA2557', NULL, 1, 1, 8, 1, NULL, 1, '', '', '', NULL),
(58, 'TREESA JOSE', 'mca2558@rajagiri.edu', 'MCA2558', NULL, 1, 1, 11, 1, NULL, 1, '', '', '', NULL),
(59, 'VISWAS B KURIAN', 'mca2559@rajagiri.edu', 'MCA2559', NULL, 1, 1, 4, 1, NULL, 1, '', '', '', NULL),
(60, 'YAHWIN LUKOSE', 'mca2560@rajagiri.edu', 'MCA2560', NULL, 1, 1, 7, 1, NULL, 1, '', '', '', NULL),
(62, 'Samplename1', 'sampleStudent@rajagiri.edu', 'MCA0000', '9845561497', 1, 1, NULL, 1, '2025-11-28', 1, 'logo_wLV9NiX.png', 'id_5aRcyEu.pdf', '', 19);

-- --------------------------------------------------------

--
-- Table structure for table `mentormentee_studentuploads`
--

DROP TABLE IF EXISTS `mentormentee_studentuploads`;
CREATE TABLE IF NOT EXISTS `mentormentee_studentuploads` (
  `upload_id` int NOT NULL AUTO_INCREMENT,
  `upload_file` varchar(500) NOT NULL,
  `student_id` int NOT NULL,
  PRIMARY KEY (`upload_id`),
  KEY `MentorMentee_studentuploads_student_id_1e6c396d` (`student_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
