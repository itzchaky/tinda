CREATE TABLE IF NOT EXISTS Users(
  userid int PRIMARY KEY AUTO_INCREMENT,
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(20),
  description TEXT,
  password VARCHAR(255) NOT NULL,
  dateBirth DATE,
  location VARCHAR(255)
)

CREATE TABLE IF NOT EXISTS Pictures(
  fileName VARCHAR(255) PRIMARY KEY,
  order int,
  userid int NOT NULL,
  FOREIGN KEY (userid) REFERENCES Users(userid) ON DELETE CASCADE
)

CREATE TABLE IF NOT EXISTS matches(
  matchid int PRIMARY KEY AUTO_INCREMENT,
  matchDate DATE,
  active boolean,
  matcher int REFERENCES Users(userid),
  matchee int REFERENCES Users(userid)
)

CREATE TABLE IF NOT EXISTS chats(
  chatid int PRIMARY KEY AUTO_INCREMENT,
  message TEXT,
  timestamp TIMESTAMP,
  senderid int references Users(userid),
  recipientid int references Users(userid)
)