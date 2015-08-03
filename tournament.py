#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

class DB:
	def __init__(self, dbstr="dbname=tournament"):
		"""
		Connect to the PostgreSQL database.  
		Returns a database connection with the string
		provided
		"""
		self.conn = psycopg2.connect(dbstr)
		
	def cursor(self):
		"""
		Returns the current database cursor object
		"""
		return self.conn.cursor()
		
	def execute(self, sql_query_string, and_close=False):
		"""
		Takes a string input and a boolean in order to
		close the database when needed
		"""
		cursor = self.cursor()
		cursor.execute(sql_query_string)
		if and_close: 
			self.conn.commit()
			self.close()
		
		# Returns the connection and cursor if not closed.
		return {"conn": self.conn, "cursor": cursor if not and_close else None}
	
	def close(self):
		"""
		Closes the connection to db
		"""
		return self.conn.close()



def deleteMatches():
    """Remove all the match records from the database."""
    try:
        DB().execute("DELETE FROM matches;", True)  
    except Exception as e:
        print e



def deletePlayers():
    """Remove all the player records from the database."""
    try:
        DB().execute("DELETE FROM players;", True)
    except Exception as e:
        print e

def countPlayers():
    """Returns the number of players currently registered."""

	# Creates a new connection "conn" which selects the players table
    conn = DB().execute("SELECT count(*) AS num FROM players")
	# Creates a new cursor object containing the fetchall from the table
    cursor = conn["cursor"].fetchone()[0]
    conn['conn'].close()
    print cursor
    return cursor




def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    name = str(name)
    try:
		DB().execute("INSERT INTO players(name) values(%s)," (name,))
    except Exception as e:
        print "error: " + str(e)

def playerStandings():
	"""Returns a list of the players and their win records, sorted by wins.

	The first entry in the list should be the player in first place, or a player
	tied for first place if there is currently a tie.

	Returns:
	A list of tuples, each of which contains (id, name, wins, matches):
		id: the player's unique id (assigned by the database)
		name: the player's full name (as registered)
		wins: the number of matches the player has won
		matches: the number of matches the player has played
	"""
	conn = DB().execute("""
		SELECT players.id, players.name, COALESCE(wincount.wins,0) , COALESCE(played.count,0)
		from players 
		left outer join wincount on players.id = wincount.winner 
		left outer join played on players.id = played.id;""")

	cursor = conn["cursor"].fetchall()
	conn['conn'].close()
	return cursor
		

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    try:
        DB().execute("""INSERT INTO matches(p1,p2,winner) values(%s,%s,%s)""" , (loser,winner,winner), True)
    except Exception as e:
        print "error: " + str(e)


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    try:
		conn = DB().execute("""
			SELECT wincount.id, players.name
			FROM wincount 
			LEFT OUTER JOIN players ON players.id = wincount.id
			ORDER BY wins DESC
			""")
		cursor = conn["cursor"].fetchall()
		conn["conn"].close()
		rawdata = cursor
		rawpairs = []
		pairs = []
		for e in rawdata:
			rawpairs.append(e)
		while len(rawpairs) > 1:
			pairs.append((rawpairs.pop() + rawpairs.pop()))
		if len(rawpairs) != 0:
			pairs.append(rawpairs.pop())
		return pairs



    except Exception as e:
        print "error: " + str(e)

