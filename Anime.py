'''Represents an item of anime'''

class Anime(object):

    def __init__(self, title, description, my_anime_list_url):
        super().__init__()

        self.title = title
        self.description = description
        self.my_anime_list_url = my_anime_list_url