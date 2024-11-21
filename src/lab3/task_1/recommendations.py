import os
from typing import Tuple, Set, List


FILMS_FILENAME = "films.txt"
VIEWS_FILENAME = "views.txt"
PATH = os.path.dirname(os.path.abspath(__file__))


class User:
    def __init__(self, user_id: int, views: list[int]):
        self.user_id = user_id
        self.views = views
        self.unique_views = set(views)
    
    def are_views_in_common(self, user: 'User') -> Tuple[float, Set[int]]:
        res = self.unique_views & user.unique_views
        return (len(res) == 0, len(res) / len(self.unique_views), res)
    
    def get_recommendation(self, unique_views: set) -> Set[int]:
        return self.unique_views - unique_views
    
    def add_films_views(self, film_ids: dict[int, float]) -> None:
        if self.user_id in userid_coeff:
            coeff = userid_coeff[self.user_id]
            for film_id in self.views:
                if film_id in film_ids:
                    film_ids[film_id] += coeff


class UsersLibrary:
    def __init__(self):
        self.users = []
        self.last_user_id = None

    def add_user(self, user: User):
        self.users.append(user)
        self.last_user_id = user.user_id

    def get_users(self) -> List[User]:
        return self.users
    
    def get_number_of_user(self) -> int:
        return len(self.users)
    
    def get_last_user_id(self) -> int:
        return self.last_user_id
    

class FilmsLibrary:
    def __init__(self, filmnames: dict):
        self.filmnames = filmnames

    def add_film(self, film_id, name):
        if film_id not in self.filmnames:
            self.filmnames[film_id] = name

    def get_film(self, film_id):
        if film_id in self.filmnames:
            return self.filmnames[film_id]
        return None


def read_views(path):
    users = UsersLibrary()
    with open(path, 'r', encoding='utf-8') as file:
        for user_id, line in enumerate(file.readlines()):
            views = [int(film_id) for film_id in line.rstrip().split(',')]
            users.add_user(User(user_id, views))
    return users


def read_films(path):
    filmnames = {}
    with open(path, 'r', encoding='utf-8') as file:
        for line in file.readlines():
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

    cur_user_id = views_library.get_last_user_id() + 1
    cur_user = User(cur_user_id, cur_views)

    recommendation_films = set()
    userid_coeff = {}
    for user in views_library.get_users():
        is_empty, common_coeff, common_views = cur_user.are_views_in_common(user)
        if not is_empty:
            recommendation_films |= user.get_recommendation(common_views)
            userid_coeff[user.user_id] = common_coeff
    
    recommendation_films_count = {film_id: 0.0 for film_id in recommendation_films}

    for user in views_library.get_users():
        user.add_films_views(recommendation_films_count)

    max_views_count = max(recommendation_films_count.values())
    number_of_users = views_library.get_number_of_user()
    for film_id, views_count in recommendation_films_count.items():
        if views_count == max_views_count:
            print("-"*30)
            print("Наиболее подходящий фильм:")
            print(films_library.get_film(film_id))
            print("Коэффициент:", round(recommendation_films_count[film_id] / number_of_users, 4))
            print("-"*30)
            break