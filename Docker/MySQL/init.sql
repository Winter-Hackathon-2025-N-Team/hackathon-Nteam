
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
    user_id BIGINT PRIMARY KEY,
    user_name VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    birth_date INT,
    introduce VARCHAR(255) NOT NULL,
    icon LONGBLOG,
    pass VARCHAR(255) NOT NULL
);

-- 1. グループテーブル（グループ自体の情報を管理）
CREATE TABLE groups (
    group_id BIGINT AUTO_INCREMENT PRIMARY KEY, -- グループID
    group_name VARCHAR(255) NOT NULL, -- グループの名前
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 2. グループメンバー（誰がどのグループに属しているかを管理）
CREATE TABLE group_members (
    group_id BIGINT NOT NULL, -- どのグループか
    user_id BIGINT NOT NULL, -- どのユーザーか
    joined_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (group_id, user_id), -- 同じユーザーが同じグループに重複して入らないようにする
    FOREIGN KEY (group_id) REFERENCES groups(group_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- 3. グループメッセージ（どのグループでのメッセージかを記録）
CREATE TABLE group_messages (
    message_id BIGINT AUTO_INCREMENT PRIMARY KEY, -- メッセージID
    group_id BIGINT NOT NULL, -- どのグループか
    sender_id BIGINT NOT NULL, -- 誰が送信したか
    message TEXT,
    image LONGBLOB,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (group_id) REFERENCES groups(group_id) ON DELETE CASCADE,
    FOREIGN KEY (sender_id) REFERENCES users(user_id) ON DELETE CASCADE
);



-- 1. チャットルーム（ユーザー間の会話を識別するためのテーブル）
CREATE TABLE chat_rooms (
    chat_id BIGINT AUTO_INCREMENT PRIMARY KEY, -- チャットルームID
    user1_id BIGINT NOT NULL,  -- 参加者1のID
    user2_id BIGINT NOT NULL,  -- 参加者2のID
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user1_id, user2_id), -- 同じ組み合わせのチャットルームは1つのみ
    FOREIGN KEY (user1_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (user2_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- 2. メッセージ（どのチャットルームでやり取りされたかを記録）
CREATE TABLE messages (
    message_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    chat_id BIGINT NOT NULL,  -- どのチャットルームのメッセージか
    sender_id BIGINT NOT NULL, -- メッセージを送ったユーザー
    message TEXT,
    image LONGBLOB,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chat_id) REFERENCES chat_rooms(chat_id) ON DELETE CASCADE,
    FOREIGN KEY (sender_id) REFERENCES users(user_id) ON DELETE CASCADE
);



/*
*
*学校データ格納テーブル
*
*/
CREATE TABLE school (
    school_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    school_name CHAR(255) NOT NULL,
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
    user_id BIGINT,
    school_id BIGINT AUTO_INCREMENT,
    class_name INT,
    elementary_startYear INT,
    elementary_endYear INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (school_id) REFERENCES school(school_id) ON DELETE CASCADE
)


/*
*
*各ユーザーの幼稚園時代テーブル
*
*/
CREATE TABLE kindergardenHistory(
    history_id BIGINT PRIMARY KEY,
    user_id BIGINT,
    school_id BIGINT AUTO_INCREMENT,
    class_name INT,
    elementary_startYear INT,
    elementary_endYear INT,
    elementary_gradeStart INT,
    elementary_gradeEnd INT
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (school_id) REFERENCES school(school_id) ON DELETE CASCADE
)