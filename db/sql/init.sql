USE challenge;

CREATE TABLE test(col VARCHAR(10));

CREATE TABLE users(
    username VARCHAR(15) NOT NULL,
    passwordhash VARCHAR(100) NOT NULL
);

CREATE TABLE messages(
    text VARCHAR(100) NOT NULL,
    )

INSERT INTO test(col) VALUES('rohan');
