CREATE TABLE "id1_swap" (
	"id"	TEXT NOT NULL UNIQUE,
	"sender"	TEXT NOT NULL,
	"receiver"	TEXT NOT NULL,
	"message"	TEXT NOT NULL,
	"time"	TEXT NOT NULL,
	"fase"	TEXT NOT NULL DEFAULT 1,
	PRIMARY KEY("id")
);

CREATE TABLE "id1_data" (
	"id"	TEXT NOT NULL UNIQUE,
	"sender"	TEXT NOT NULL,
	"receiver"	TEXT NOT NULL,
	"message"	TEXT NOT NULL,
	"time"	TEXT NOT NULL,
	"fase"	TEXT NOT NULL DEFAULT 4,
	PRIMARY KEY("id")
);

CREATE TABLE "cwei_chats" (
	"id"	TEXT NOT NULL UNIQUE,
	"active"	INTEGER NOT NULL DEFAULT 1,
	PRIMARY KEY("id")
);

CREATE TABLE "cwei_users" (
	"id"	TEXT NOT NULL UNIQUE,
	"user"	TEXT NOT NULL UNIQUE,
	"password"	TEXT NOT NULL,
	"email"	TEXT NOT NULL,
	PRIMARY KEY("id")
);