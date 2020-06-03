"""
KV Le
CSE 163 AG
Final Project

A script that runs all modules that contain data manipulation/visualization for
my Final Project about Anime and MyAnimeList Users.
"""

import rq_one
import rq_two
import rq_three
import rq_four
import pandas as pd


def main():
    """Runs all functions to analyze/visualize information for my project"""

    anime_data = pd.read_csv("data/animelist_cleaned.csv")
    data_2019 = pd.read_csv("data/animelist_2019.csv")
    user_data = pd.read_csv("data/userlist_cleaned.csv")
    rq_one.main(anime_data, user_data)
    rq_two.main(anime_data, data_2019)
    rq_three.main(anime_data)
    rq_four.main(anime_data, data_2019)


if __name__ == "__main__":
    main()
