CREATE TABLE id_swap (
	"id"	TEXT NOT NULL UNIQUE,
	"receiver"	TEXT NOT NULL,
	"message"	TEXT NOT NULL,
	"time"      TEXT NOT NULL,
	"fase"	INTEGER NOT NULL DEFAULT 1,
	PRIMARY KEY("id")
);

CREATE TABLE "id_data" (
	"id"	TEXT NOT NULL UNIQUE,
	"sender"	TEXT NOT NULL,
	"receiver"	TEXT NOT NULL,
	"message"	TEXT NOT NULL,
	"send"	INTEGER NOT NULL DEFAULT 0,
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
	PRIMARY KEY("id")
);