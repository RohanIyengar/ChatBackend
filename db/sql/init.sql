USE challenge;

CREATE TABLE test(col VARCHAR(10));

CREATE TABLE Users(
    username VARCHAR(15) NOT NULL,
    salt VARCHAR(30) NOT NULL,
    passwordhash VARCHAR(100) NOT NULL,
    PRIMARY KEY(username)
);

CREATE TABLE Messages(
    text VARCHAR(1000) NOT NULL,
    width INT,
    height INT,
    duration TIME,
    videosource VARCHAR(50),
    sender VARCHAR(15) NOT NULL references Users.username,
    receiver VARCHAR(15) NOT NULL references Users.username,
    senttime TIME DEFAULT NOW(),
    PRIMARY KEY(sender, receiver)
);

INSERT INTO test(col) VALUES('rohan');
