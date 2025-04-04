CREATE TABLE "_swap" (
	"id"	TEXT NOT NULL UNIQUE,
	"sender"	TEXT NOT NULL,
	"receiver"	TEXT NOT NULL,
	"message"	TEXT NOT NULL,
	"time"	TEXT NOT NULL,
	"fase"	TEXT NOT NULL DEFAULT 1,
	PRIMARY KEY("id")
);

CREATE TABLE "_data" (
	"id"	TEXT NOT NULL UNIQUE,
	"sender"	TEXT NOT NULL,
	"receiver"	TEXT NOT NULL,
	"message"	TEXT NOT NULL,
	"time"	TEXT NOT NULL,
	"fase"	TEXT NOT NULL DEFAULT 4,
	PRIMARY KEY("id")
);

CREATE TABLE "!cwei_chats" (
	"id"	TEXT NOT NULL UNIQUE,
	"user1"	TEXT NOT NULL,
	"user2"	TEXT NOT NULL,
	"active"	TEXT NOT NULL DEFAULT 0,
	PRIMARY KEY("id")
);

CREATE TABLE "!cwei_users" (
	"id"	TEXT NOT NULL UNIQUE,
	"user"	TEXT NOT NULL UNIQUE,
	"password"	TEXT NOT NULL,
	"email"	TEXT NOT NULL,
	PRIMARY KEY("id")
);