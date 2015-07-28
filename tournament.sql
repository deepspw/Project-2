-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Raw played 
create view rawplayed as select p1, count(*) 
	from (select p1 from matches union all select p2 from matches) as raw 
	group by p1;

-- Played games view
create view played as select players.id, rawplayed.p1, rawplayed.count 
	from players 
	left outer join rawplayed on rawplayed.p1 = players.id;

-- Wincount view
create view wincount as select players.id, matches.winner, count(matches.winner) as wins 
	from players 
	left outer join matches on matches.winner=players.id 
	group by players.id, matches.winner;

