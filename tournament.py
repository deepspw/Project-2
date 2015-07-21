#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
    

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    try:
        connection = connect()
        c = connection.cursor()
        c.execute("DELETE FROM matches;")
        connection.commit()
        connection.close()
    except Exception as e:
        print e



def deletePlayers():
    """Remove all the player records from the database."""
    try:
        connection = connect()
        c = connection.cursor()
        c.execute("DELETE FROM players;")
        connection.commit()
        connection.close()
    except Exception as e:
        print e

def countPlayers():
    """Returns the number of players currently registered."""
    connection = connect()
    c = connection.cursor()
    c.execute("SELECT count(*) AS num FROM players")
    count = c.fetchall()
    connection.close()
    return count.pop()[0]




def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    name = str(name)
    try:
        connection = connect()
        c = connection.cursor()
        c.execute("INSERT INTO players(name) values(%s)", (name,))
        connection.commit()
        connection.close()
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
    try:
        connection = connect()
        c = connection.cursor()
        c.execute("""select players.id, players.name, wincount.wins from players left outer join wincount on players.id = wincount.winner;
				 """)
        return c.fetchall()
    except Exception as e:
    	print "error: " + str(e)
    	# select id name regardless of wether they played, needs to track matches played too


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    try:
        connection = connect()
        c = connection.cursor()
        c.execute("INSERT INTO matches(winner) values(%s)", (winner,))
        connection.commit()
        connection.close()
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
        connection = connect()
        c = connection.cursor()
        c.execute("""SELECT winner FROM matches, COUNT(*) group by winner
                ORDER by num desc;""")
        print c.fetchall()
    except Exception as e:
        print "error: " + str(e)



print playerStandings()