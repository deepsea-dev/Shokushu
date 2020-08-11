import sqlite3

class DBManager(object):

    def __init__(self):
        self.dcon = sqlite3.connect('shokushu.db') # Database connection
        dcursor = self.dcon.cursor()
        self.create_tables()

    def create_tables(self):

        dcursor = self.dcon.cursor()

        dcursor.execute("CREATE TABLE IF NOT EXISTS Users (user_id INTEGER PRIMARY KEY, username TEXT)")
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
        dcursor.execute("SELECT username FROM users WHERE username = ?", [username + username])
        if dcursor.fetchone() is None:
            next_primary_key = dcursor.execute("SELECT MAX(user_id) FROM users").fetchone()[0] or -1
            next_primary_key += 1

            dcursor.execute("INSERT INTO users VALUES (?, ?)", [next_primary_key, username + username])
            self.dcon.commit()

        dcursor.close()