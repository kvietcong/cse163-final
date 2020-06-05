"""
KV Le
CSE 163 AG
Final Project

A script that does basic tests my data analysis for my final project
"""

import pandas as pd
import rq_one as rq1


def test_cleaned_data(anime, users, lists, anime_2019):
    """Tests if the data has been cleaned/retrieved properly

    Parameters
    ----------
    anime : DataFrame
        Pandas DataFrame that contains anime show data
    users : DataFrame
        Pandas DataFrame that contains MAL user data
    lists : DataFrame
        Pandas DataFrame that contains information on MAL user's anime lists
    anime_2019 : DataFrame
        Pandas DataFrame that contains 2019 anime show data

    Notes
    -----
    Throws an Assertion Error if any of the cleaned files have incorrect
        columns of information
    All values that are being tested are calculated and checked by hand
    """

    assert set(["anime_id", "title", "image_url", "type",
                "episodes", "duration_min", "score", "scored_by",
                "rank", "popularity", "members", "favorites",
                "related", "studio", "genre", "aired_from_year",
                "source"]) == set(anime.columns)
    assert set(["username", "user_id", "user_watching",
                "user_completed", "user_onhold", "user_dropped",
                "user_plantowatch", "user_days_spent_watching",
                "gender", "location", "birth_date",
                "stats_mean_score", "stats_episodes", "age"]) \
        == set(users.columns)
    assert set(["username", "anime_id", "my_score",
                "my_status", "my_watched_episodes"]) == set(lists.columns)
    assert set(["anime_id", "title", "type", "episodes", "duration_min",
                "source", "score", "members", "favorites", "studio",
                "genre"]) == set(anime_2019.columns)
    print("All Cleaned Sets Have The Proper Columns")


def test_genre_calculations(anime, anime_2019):
    """Tests if common genre info maniplation techniques that I used are valid

    Parameters
    ----------
    anime : DataFrame
        Pandas DataFrame that contains anime show data
    anime_2019 : DataFrame
        Pandas DataFrame that contains 2019 anime show data

    Notes
    -----
    Expected all data sets to be a sub sample of the first 10 elements
    Throws an Assertion Error if any of the testing fails
    All values that are being tested are calculated and checked by hand
    """

    # Testing mean calculation
    assert abs(anime["score"].mean() - 7.954) < .001
    assert abs(anime_2019["score"].mean() - 7.869) < .001

    # Testing genre count calculations
    genre_counts = anime["genre"].str.split(", ", expand=True).stack() \
        .str.get_dummies().sum().sort_values(ascending=False).reset_index()
    genres = ["Romance", "Comedy", "School", "Shoujo", "Shounen", "Magic",
              "Drama", "Supernatural", "Fantasy", "Slice of Life",
              "Parody", "Music", "Kids", "Josei", "Harem", "Action"]
    amounts = [8, 8, 6, 4, 3, 3, 3, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1]

    for index in range(len(genres)):
        assert (genre_counts["index"].iloc[index],
                genre_counts[0].iloc[index]) == \
                    (genres[index], amounts[index])

    # Testing yearly genre count calculations
    yearly = pd.concat([anime.head(2)["aired_from_year"],
                        pd.get_dummies(anime.head(2)["genre"]
                        .str.split(", ", expand=True),
                        prefix="", prefix_sep="")], axis=1)
    yearly = yearly.groupby("aired_from_year").sum() \
        .groupby(level=0, axis=1).sum().reset_index()
    yearly = pd.melt(yearly, ["aired_from_year"]) \
        .rename(columns={"variable": "Genre"})
    yearly = yearly[yearly["value"] > 0].sort_values("aired_from_year") \
        .reset_index()

    years = ([2007] * 5) + ([2012] * 4)
    genres = ["Comedy", "Parody", "Romance", "School",
              "Shounen", "Comedy", "Romance", "Shounen", "Supernatural"]
    value = [1] * 9

    for index in range(len(years)):
        assert (yearly["aired_from_year"].iloc[index],
                yearly["Genre"].iloc[index], yearly["value"].iloc[index]) == \
            (years[index], genres[index], value[index])

    print("Genre Information Manipulation is generally valid")


def test_studio_calculations(anime):
    """Tests if common studio info maniplation techniques that I used are valid

    Parameters
    ----------
    anime : DataFrame
        Pandas DataFrame that contains anime show data

    Notes
    -----
    Expected all data sets to be a sub sample of the first 10 elements
    Throws an Assertion Error if any of the testing fails
    All values that are being tested are calculated and checked by hand
    """

    # Testing studio averages
    avg = anime[["studio", "score"]].copy()
    avg["studio"] = avg["studio"].str.split(", ")
    avg = avg.explode("studio").groupby("studio").mean() \
        .sort_values("score", ascending=False).reset_index()

    studios = ["Bones", "Hal Film Maker", "J.C.Staff", "Studio Hibari",
               "Studio Pierrot", "Gonzo", "David Production",
               "Satelight", "Production Reed"]
    score = [8.34, 8.21, 8.21, 8.03, 8.03, 7.89, 7.63, 7.55, 7.26]

    for index in range(len(studios)):
        assert (avg["studio"].iloc[index],
                avg["score"].iloc[index]) == \
                    (studios[index], score[index])

    # Testing genre count calculations
    studio_counts = anime["studio"].str.split(", ", expand=True).stack() \
        .str.get_dummies().sum().sort_values(ascending=False).reset_index()
    studios = ["J.C.Staff", "Studio Pierrot", "Studio Hibari", "Satelight",
               "Production Reed", "Hal Film Maker", "Gonzo",
               "David Production", "Bones"]
    amounts = [3] + ([1] * 8)

    for index in range(len(studios)):
        assert (studio_counts["index"].iloc[index],
                studio_counts[0].iloc[index]) == \
                    (studios[index], amounts[index])

    print("Studio Information Manipulation is generally valid")


def test_user_calculations(users):
    """Tests if common user info maniplation techniques that I used are valid

    Parameters
    ----------
    users : DataFrame
        Pandas DataFrame that contains MAL user data

    Notes
    -----
    Expected all data sets to be a sub sample of the first 10 elements
    Throws an Assertion Error if any of the testing fails
    All values that are being tested are calculated and checked by hand
    Prints a success message if the tests pass
    """
    avg1 = rq1.average_user(users)
    avg2 = {
        "age": 27.8,
        "score": 8.214,
        "days_watched": 48.9,
        "episodes": 2962,
        "completed": 109.5,
        "watching": 20.7,
        "planned": 36.3,
        "onhold": 3.8,
        "dropped": 5.3
    }

    for avg in avg1:
        assert avg1[avg] - avg2[avg] < .01

    print("User Information Manipulation is generally valid")


def main():
    """Runs all tests

    Notes
    -----
    Throws an error if any tests are failed
    """
    anime = pd.read_csv("data/animelist_cleaned.csv")
    anime_2019 = pd.read_csv("data/animelist_2019.csv")
    users = pd.read_csv("data/userlist_cleaned.csv")
    lists = pd.read_csv("data/user_animelists_cleaned.csv")

    test_cleaned_data(anime, users, lists, anime_2019)

    anime_small = anime.head(10)
    anime_2019_small = anime_2019.head(10)
    users_small = users.head(10)

    test_genre_calculations(anime_small, anime_2019_small)
    test_studio_calculations(anime_small)
    test_user_calculations(users_small)


if __name__ == "__main__":
    main()
