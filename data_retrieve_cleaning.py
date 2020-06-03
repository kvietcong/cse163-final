import pandas as pd
from jikanpy import Jikan
from time import sleep


def clean_user_animelists():
    """Cleans original user animelists for information relavent to the project

    Notes
    -----
    File Path: data/user_animelists_cleaned.csv
    """

    new_animelists = \
        pd.read_csv('data/original_data/users_animelists_azathoth.csv',
                    usecols=["username", "anime_id", "my_score",
                             "my_status", "my_watched_episodes"]).dropna()
    new_animelists.to_csv("data/user_animelists_cleaned.csv", index=False)


def clean_animelist():
    """Cleans original anime info for information relavent to the project

    Notes
    -----
    File Path: data/animelist_cleaned.csv
    """

    new_animelist = \
        pd.read_csv('data/original_data/anime_azathoth.csv',
                    usecols=["anime_id", "title", "image_url", "type",
                             "episodes", "duration_min", "score", "scored_by",
                             "rank", "popularity", "members", "favorites",
                             "related", "studio", "genre", "aired_from_year",
                             "source"]).dropna()
    new_animelist.to_csv("data/animelist_cleaned.csv", index=False)


def clean_userlist():
    """Cleans original MAL user info for information relavent to the project

    Notes
    -----
    File Path: data/userlist_cleaned.csv
    """

    new_userlist = \
        pd.read_csv('data/original_data/users_azathoth.csv',
                    usecols=["username", "user_id", "user_watching",
                             "user_completed", "user_onhold", "user_dropped",
                             "user_plantowatch", "user_days_spent_watching",
                             "gender", "location", "birth_date",
                             "stats_mean_score", "stats_episodes"]).dropna()
    new_userlist["age"] = 2020 - \
        pd.to_numeric(new_userlist["birth_date"]
                      .str.split("-", expand=True, n=1)[0])
    # Not to be offensive but working with non-Binary genders will be too hard
    new_userlist = new_userlist[new_userlist["gender"]
                                .isin(["Male", "Female"])]
    new_userlist.to_csv("data/userlist_cleaned.csv", index=False)


def get_2019_mal_data():
    """Uses JikanAPI to retrieve anime info from 2019

    Notes
    -----
    File Path: data/animelist_2019.csv
    """

    jikan = Jikan()
    anime_2019 = {
        "anime_2019_spr": jikan.season(2019, "spring"),
        "anime_2019_sum": jikan.season(2019, "summer"),
        "anime_2019_fall": jikan.season(2019, "fall"),
        "anime_2019_win": jikan.season(2019, "winter")
    }
    attributes = ["type", "episodes", "score", "source",
                  "members", "genres", "title", "mal_id"]
    animes = {
        "anime_id": [],
        "title": [],
        "type": [],
        "episodes": [],
        "duration_min": [],
        "source": [],
        "genre": [],
        "studio": [],
        "score": [],
        "favorites": [],
        "members": []
    }
    for season in anime_2019:
        print(f"Retrieving all {season} Anime")
        for anime in anime_2019[season]["anime"]:
            for attribute in attributes:
                if attribute == "mal_id":
                    anime_id = anime[attribute]
                    animes["anime_id"].append(anime_id)

                    trying = True
                    while trying:
                        try:
                            anime_info = \
                                jikan.anime(anime_id)
                            trying = False
                        except Exception:
                            print(f"Error in getting {anime['title']}. " +
                                  "Retrying")
                            sleep(2)

                    studios = []
                    for studio_info in anime_info["studios"]:
                        studios.append(studio_info["name"])

                    duration = anime_info["duration"]
                    duration = duration.split()
                    duration_hr = duration[duration.index("hr") - 1] \
                        if "hr" in duration else 0
                    duration_min = duration[duration.index("min") - 1] \
                        if "min" in duration else 0
                    duration = int(duration_hr) * 60 + int(duration_min)

                    favorites = anime_info["favorites"]

                    animes["studio"].append(", ".join(studios))
                    animes["duration_min"].append(duration)
                    animes["favorites"].append(favorites)

                    # Sleep is to ensure that we don't make to many requests
                    # and get blocked from JikanAPI
                    sleep(4)
                elif attribute == "genres":
                    genres = []
                    for genre_info in anime[attribute]:
                        genres.append(genre_info["name"])
                    animes["genre"].append(", ".join(genres))
                else:
                    animes[attribute].append(anime[attribute])
    result = pd.DataFrame.from_dict(animes).dropna()
    result = result[result["studio"].astype(bool)]
    result.to_csv("data/animelist_2019.csv", index=False)


def main():
    """Runs all functions to retrieve and clean information for my project"""

    clean_user_animelists()
    clean_animelist()
    clean_userlist()
    get_2019_mal_data()


if __name__ == "__main__":
    main()
