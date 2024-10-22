import os


FILMS_FILENAME = "films.txt"
VIEWS_FILENAME = "films.txt"

class User:
    def __init__(self, id, views):
        self.id = id
        self.views = views
    
class FilmsLibrary:
    def __init__(self, filmnames: dict):
        self.filmnames = filmnames

    def add_film(self, id, name):
        if id not in self.filmnames:
            self.filmnames[id] = name



if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    films_path = os.path.join(current_dir, FILMS_FILENAME)
    views_path = os.path.join(current_dir, VIEWS_FILENAME)

    print("Введите список просмотров пользователя (номера через запятую):")
    cur_views = []
    while True:
        a = input().split(',')
        if all(x.isnumeric() for x in a):
            cur_views = [int(x) for x in a]
            break
        else:
            print('Некорректный ввод.')
    