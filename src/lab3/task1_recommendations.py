import os


FILMS_FILENAME = "films.txt"
VIEWS_FILENAME = "films.txt"
PATH = os.path.dirname(os.path.abspath(__file__))


class UsersLibrary:
    def __init__(self):
        self.users = []

    def add_user(self, user):
        self.users.append(user)

    def get_users(self):
        return self.users


class User:
    def __init__(self, user_id, views):
        self.user_id = user_id
        self.views = views
        self.unique_views = set(views)
    
    def are_views_in_common(self, unique_views):
        res = self.unique_views & unique_views
        return 2 * len(res) >= len(self.unique_views), res
    
    def get_recommendation(self, unique_views):
        return self.unique_views - unique_views
    

class FilmsLibrary:
    def __init__(self, filmnames: dict):
        self.filmnames = filmnames

    def add_film(self, id, name):
        if id not in self.filmnames:
            self.filmnames[id] = name


def read_views(path):
    users = UsersLibrary()
    with open(path, 'r') as file:
        for user_id, line in enumerate(file.readlines):
            views = [int(film_id) for film_id in line.rstrip().split(',')]
            users.add_user(User(user_id, views))
    return users


def read_films(path):
    filmnames = {}
    with open(path, 'r') as file:
        for line in file.readlines:
            idx, name = line.rstrip().split(',')
            filmnames[int(idx)] = name
    return FilmsLibrary(filmnames)


if __name__ == "__main__":
    films_path = os.path.join(PATH, FILMS_FILENAME)
    views_path = os.path.join(PATH, VIEWS_FILENAME)

    print("Введите список просмотров пользователя (номера через запятую):")
    cur_views = []
    while True:
        a = input().split(',')
        if all(x.isnumeric() for x in a):
            cur_views = [int(x) for x in a]
            break
        else:
            print('Некорректный ввод.')
    films_library = read_films(films_path)
    views_library = read_views(views_path)
    