CREATE TABLE `mv` ( 
  `taskid` varchar (64) NOT NULL, 
  `url` varchar (1024) DEFAULT NULL, 
  `localpath` varchar (260) DEFAULT NULL, 
  `updatetime` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, PRIMARY KEY (`taskid`)
  )ENGINE=InnoDB DEFAULT CHARSET=utf8;