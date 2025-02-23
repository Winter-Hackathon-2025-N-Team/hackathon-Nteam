
DROP DATABASE chatapp;
DROP USER 'testuser';

/*テーブルをCRUDできるユーザー作成*/
CREATE USER 'testuser' IDENTIFIED BY 'testuser';
CREATE DATABASE chatapp;
USE chatapp

/*ユーザーに権限の付与*/
GRANT ALL PRIVILEGES ON chatapp.* TO 'testuser';

/*
*
*全てのユーザーのデータが格納されているテーブル
*
*/
CREATE TABLE users (
    uid VARCHAR(255) PRIMARY KEY,
    user_name VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password CHAR(64) NOT NULL,
    kindergarten_schoolname VARCHAR(255) NOT NULL,
    kindergarten_start_year INT,
    kindergarten_end_year INT,
    elementary_schoolname VARCHAR(255) NOT NULL,
    elementary_start_year INT,
    elementary_end_year INT
);