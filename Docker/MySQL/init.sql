
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
    uid BIGINT PRIMARY KEY,
    user_name VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    birth_date INT,
    introduce VARCHAR(255) NOT NULL,
    pass VARCHAR(255) NOT NULL
);

/*
*
*グループ向けのメッセージテーブル？
*
*/
CREATE TABLE messageGroup (
    mgid BIGINT AUTO_INCREMENT PRIMARY KEY,　
    uid BIGINT PRIMARY KEY,
    message TEXT,
    image LONGBLOB,
    created_at datetime NOT NULL,
    FOREIGN KEY (uid) REFERENCES users(uid) ON DELETE CASCADE,
    FOREIGN KEY (room) REFERENCES room(mid) ON DELETE CASCADE
);


/*
*
*個人チャット向けのメッセージテーブル？
*
*/
CREATE TABLE messagePairs(
    mpid BIGINT AUTO_INCREMENT PRIMARY KEY,
    uid BIGINT PRIMARY KEY,
    message TEXT,
    image LONGBLOB,
    created_at datetime NOT NULL,
    FOREIGN KEY (uid) REFERENCES users(uid) ON DELETE CASCADE,
    FOREIGN KEY (room) REFERENCES room(mid) ON DELETE CASCADE
);


/*
*
*学校データ格納テーブル
*
*/
CREATE TABLE school (
    sid BIGINT AUTO_INCREMENT PRIMARY KEY,
    school_name VARCHAR(255) NOT NULL,
    school_type int(1), /*幼稚園：１　小学校：２*/
    location CHAR
);


/*
*
*各ユーザーの小学生時代テーブル
*
*/
CREATE TABLE elementaryHistory(
    history_id BIGINT PRIMARY KEY,
    uid BIGINT,
    sid BIGINT AUTO_INCREMENT,
    class_name INT,
    elementary_startYear INT,
    elementary_endYear INT,
    elementary_gradeStart INT,
    elementary_gradeEnd INT
    FOREIGN KEY (uid) REFERENCES users(uid) ON DELETE CASCADE,
    FOREIGN KEY (sid) REFERENCES school(uid) ON DELETE CASCADE
)


/*
*
*各ユーザーの幼稚園時代テーブル
*
*/
CREATE TABLE kindergardenHistory(
    history_id BIGINT PRIMARY KEY,
    uid BIGINT,
    sid BIGINT AUTO_INCREMENT,
    class_name INT,
    elementary_startYear INT,
    elementary_endYear INT,
    elementary_gradeStart INT,
    elementary_gradeEnd INT
    FOREIGN KEY (uid) REFERENCES users(uid) ON DELETE CASCADE,
    FOREIGN KEY (sid) REFERENCES school(uid) ON DELETE CASCADE
)