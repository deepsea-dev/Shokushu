'''Represents an item of anime'''

class Anime(object):

    def __init__(self,id, title, description, my_anime_list_url):
        super().__init__()

        self.id = id
        self.title = title
        self.description = description
        self.my_anime_list_url = my_anime_list_url