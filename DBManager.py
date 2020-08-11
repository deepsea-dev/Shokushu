import sqlite3
from Anime import Anime

class DBManager(object):

    def __init__(self):
        self.dcon = sqlite3.connect('shokushu.db') # Database connection
        dcursor = self.dcon.cursor()
        self.create_tables()

    def create_tables(self):

        dcursor = self.dcon.cursor()

        dcursor.execute("CREATE TABLE IF NOT EXISTS Users (user_id INTEGER PRIMARY KEY, username TEXT)")

        # Stores the anime objects
        dcursor.execute("CREATE TABLE IF NOT EXISTS Anime (anime_id INTEGER PRIMARY KEY, anime_title TEXT, anime_description TEXT, anime_url TEXT)")

        # The scores table links a user and an anime and also stores the score that they gave it
        dcursor.execute("CREATE TABLE IF NOT EXISTS Scores (score_id INTEGER PRIMARY KEY,\
                                                            user_id INTEGER,\
                                                            anime_id INTEGER,\
                                                            score INTEGER not null,\
                                                            FOREIGN KEY(user_id) REFERENCES Users(user_id)\
                                                            FOREIGN KEY (anime_id) REFERENCES Anime(anime_id))")

        # Stores all the queues that the bot has
        dcursor.execute("CREATE TABLE IF NOT EXISTS Queue (channel_id INTEGER PRIMARY KEY)")

        # Links queues and animes
        dcursor.execute("CREATE TABLE IF NOT EXISTS Queue_anime_link (queue_id INTEGER not null,\
                                                                       anime_id INTEGER not null,\
                                                                       FOREIGN KEY(queue_id) REFERENCES Queue(channel_id),\
                                                                       FOREIGN KEY (anime_id) REFERENCES Anime(anime_id))")
        dcursor.close()

    def add_user_if_required(self, username):
        dcursor = self.dcon.cursor()
        # TODO maybe use AUTOINCREMENT schema?
        dcursor.execute("SELECT username FROM Users WHERE username = ?", [username + username])
        if dcursor.fetchone() is None:
            next_primary_key = dcursor.execute("SELECT MAX(user_id) FROM Users").fetchone()[0] or -1
            next_primary_key += 1

            dcursor.execute("INSERT INTO Users VALUES (?, ?)", [next_primary_key, username + username])
            self.dcon.commit()

        dcursor.close()


    def get_anime_from_id(self, anime_id):
        ''' returns an anime object'''

        dcursor = self.dcon.cursor()

        dcursor.execute("SELECT * FROM Anime WHERE anime_id = ?", (anime_id,))
        
        anime = dcursor.fetchone()
        if anime is None:
            return None

        self.dcon.commit()
        dcursor.close()

        return Anime(anime[0], anime[1], anime[2], anime[3]) # Return a new anime object with the attrs

    def add_anime(self, anime):
        ''' inserts an anime object into the anime table '''
        dcursor = self.dcon.cursor()

        dcursor.execute("INSERT INTO Anime VALUES (?,?,?,?)", 
                        [anime.id, anime.title, anime.description, anime.my_anime_list_url])
        self.dcon.commit()
        dcursor.close()
