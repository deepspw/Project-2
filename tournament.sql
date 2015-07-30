-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Create database 
CREATE DATABASE tournament;
\c tournament;

-- Create table players
CREATE TABLE players(
	id SERIAL, 
	name TEXT, 
	PRIMARY KEY (id)
	);

-- Create table matches
CREATE TABLE matches(
	p1 int,
	p2 int,
	winner int,
	FOREIGN KEY (p1) REFERENCES players(id),
	FOREIGN KEY (p2) REFERENCES players(id),
	FOREIGN KEY (winner) REFERENCES players(id)
	);

-- Raw played 
CREATE VIEW rawplayed AS SELECT p1, COUNT(*) 
	FROM (SELECT p1 FROM matches UNION ALL SELECT p2 FROM matches) AS RAW 
	GROUP BY p1;

-- Played games view
CREATE VIEW played AS SELECT players.id, rawplayed.p1, rawplayed.count 
	FROM players 
	LEFT OUTER JOIN rawplayed ON rawplayed.p1 = players.id;

-- Wincount view
CREATE VIEW wincount AS SELECT players.id, matches.winner, count(matches.winner) AS wins 
	FROM players 
	LEFT OUTER JOIN matches ON matches.winner=players.id 
	GROUP BY players.id, matches.winner;

