grant all privileges on *.* to 'root'@'%' identified by '123456' with grant option;
flush privileges; 
-- 创建数据库
create database album default character set utf8 collate utf8_general_ci;

use album;

-- 建表
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS col;
DROP TABLE IF EXISTS photo;

CREATE TABLE user (
 email varchar(40),
 password varchar(128),
 PRIMARY KEY (email)
); 
create table col(
	id varchar(64),
	name varchar(20),
    create_time varchar(40),
    type varchar(20),
    user_email varchar(64)
    );
create table photo(
	id varchar(64),
    create_time varchar(40),
    col_id varchar(64)
    )
