drop database if exists todolist;

create database todolist;

use todolist;

create table user(
  `id` int not null auto_increment,
  `username` varchar(50) not null,
  `password` varchar(50) not null,
  primary key(`id`)
)engine=innodb default charset=utf8;