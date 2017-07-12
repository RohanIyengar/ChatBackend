USE challenge;

CREATE TABLE test(col VARCHAR(10));

CREATE TABLE Users(
    username VARCHAR(15) NOT NULL,
    salt VARCHAR(30) NOT NULL,
    passwordhash VARCHAR(100) NOT NULL,
    PRIMARY KEY(username)
);

CREATE TABLE Messages(
    text VARCHAR(100) NOT NULL,
    width INT,
    height INT,
    duration TIME,
    sender VARCHAR(15) NOT NULL references Users.username,
    receiver VARCHAR(15) NOT NULL references Users.username,
    PRIMARY KEY(sender, receiver)
);

INSERT INTO test(col) VALUES('rohan');
