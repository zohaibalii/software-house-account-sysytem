-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 12, 2021 at 12:28 PM
-- Server version: 10.4.17-MariaDB
-- PHP Version: 8.0.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `webtrika`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth`
--

CREATE TABLE `auth` (
  `sno` int(11) NOT NULL,
  `name` varchar(70) NOT NULL,
  `username` varchar(70) NOT NULL,
  `password` varchar(70) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `auth`
--

INSERT INTO `auth` (`sno`, `name`, `username`, `password`) VALUES
(1, 'zoahib', 'ali', 'pakistann'),
(2, 'zohaib', 'zohaib', 'pakistann');

-- --------------------------------------------------------

--
-- Table structure for table `calls`
--

CREATE TABLE `calls` (
  `sno` int(11) NOT NULL,
  `name` varchar(70) NOT NULL,
  `number` varchar(100) NOT NULL,
  `reason` varchar(1000) NOT NULL,
  `country` varchar(70) NOT NULL,
  `city` varchar(70) NOT NULL,
  `date` varchar(70) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `calls`
--

INSERT INTO `calls` (`sno`, `name`, `number`, `reason`, `country`, `city`, `date`) VALUES
(179, 'Zubair', '0300', 'reasonn ', 'inida', 'mumbai', '2021-04-12'),
(180, 'Zohaibb', '03003858987', 'web develpment ', 'pakistan', 'karachi', '2021-04-12');

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `sno` int(11) NOT NULL,
  `customername` varchar(70) NOT NULL,
  `service` varchar(30) NOT NULL,
  `country` varchar(30) NOT NULL,
  `projectname` varchar(100) NOT NULL,
  `price` int(11) NOT NULL,
  `startdate` date NOT NULL,
  `enddate` date NOT NULL,
  `detail` varchar(1000) NOT NULL,
  `extra` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`sno`, `customername`, `service`, `country`, `projectname`, `price`, `startdate`, `enddate`, `detail`, `extra`) VALUES
(15, '6 ', 'Web Development', '', 'post', 200, '2021-04-03', '2021-04-03', 'DETAIL', 'extra');

-- --------------------------------------------------------

--
-- Table structure for table `customerdetail`
--

CREATE TABLE `customerdetail` (
  `sno` int(11) NOT NULL,
  `name` varchar(70) NOT NULL,
  `country` varchar(70) NOT NULL,
  `phone` varchar(100) NOT NULL,
  `email` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `customerdetail`
--

INSERT INTO `customerdetail` (`sno`, `name`, `country`, `phone`, `email`) VALUES
(6, 'Zohaib', 'India', '03003858987', 'zohaibbozdar786@gmail.com'),
(10, 'Khaliq', 'Pakistan', '030000', 'zohaibbuzdarr@gmail.com'),
(11, 'zubair', 'Pakistan', '30000', 'zohaibbozdar786@gmail.com'),
(12, 'zaid', 'india', '030000', 'zaid@gmail.com'),
(14, 'khALIQ', 'pAKISTAN', '1234567890', 'CLIENT@GMAIL.COM');

-- --------------------------------------------------------

--
-- Table structure for table `hosting`
--

CREATE TABLE `hosting` (
  `sno` int(11) NOT NULL,
  `name` int(11) NOT NULL,
  `disk` varchar(100) NOT NULL,
  `startdatee` varchar(200) NOT NULL,
  `enddatee` varchar(300) NOT NULL,
  `price` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `hosting`
--

INSERT INTO `hosting` (`sno`, `name`, `disk`, `startdatee`, `enddatee`, `price`) VALUES
(19, 6, 'UNLIMITED', '2021-04-03', '2021-04-06', 2000),
(20, 11, '10 GB', '2021-04-05', '2021-04-05', 2000),
(21, 12, '5 GB', '2021-04-05', '2021-04-05', 2000);

-- --------------------------------------------------------

--
-- Table structure for table `logingtime`
--

CREATE TABLE `logingtime` (
  `sno` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `time` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `logingtime`
--

INSERT INTO `logingtime` (`sno`, `name`, `time`) VALUES
(2, 'ali', '2021-04-05 17:10:16'),
(3, 'ali', '2021-04-05 17:10:31'),
(4, 'zohaib', '2021-04-05 19:36:12');

-- --------------------------------------------------------

--
-- Table structure for table `maintenance`
--

CREATE TABLE `maintenance` (
  `sno` int(11) NOT NULL,
  `clientname` int(11) NOT NULL,
  `projectname` varchar(70) NOT NULL,
  `detail` varchar(10000) NOT NULL,
  `price` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `maintenance`
--

INSERT INTO `maintenance` (`sno`, `clientname`, `projectname`, `detail`, `price`) VALUES
(2, 12, 'project name', 'ye wo', 786),
(3, 11, 'pname', 'detail', 200),
(4, 10, 'PNAMEE', 'DETAILll', 200);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `auth`
--
ALTER TABLE `auth`
  ADD PRIMARY KEY (`sno`);

--
-- Indexes for table `calls`
--
ALTER TABLE `calls`
  ADD PRIMARY KEY (`sno`);

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`sno`);

--
-- Indexes for table `customerdetail`
--
ALTER TABLE `customerdetail`
  ADD PRIMARY KEY (`sno`);

--
-- Indexes for table `hosting`
--
ALTER TABLE `hosting`
  ADD PRIMARY KEY (`sno`);

--
-- Indexes for table `logingtime`
--
ALTER TABLE `logingtime`
  ADD PRIMARY KEY (`sno`);

--
-- Indexes for table `maintenance`
--
ALTER TABLE `maintenance`
  ADD PRIMARY KEY (`sno`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auth`
--
ALTER TABLE `auth`
  MODIFY `sno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `calls`
--
ALTER TABLE `calls`
  MODIFY `sno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=181;

--
-- AUTO_INCREMENT for table `customer`
--
ALTER TABLE `customer`
  MODIFY `sno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `customerdetail`
--
ALTER TABLE `customerdetail`
  MODIFY `sno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `hosting`
--
ALTER TABLE `hosting`
  MODIFY `sno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `logingtime`
--
ALTER TABLE `logingtime`
  MODIFY `sno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `maintenance`
--
ALTER TABLE `maintenance`
  MODIFY `sno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
