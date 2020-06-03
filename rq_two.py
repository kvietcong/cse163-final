"""
KV Le
CSE 163 AG
Final Project

A script that has multiple functions that manipulate/visualize data about
My Anime List to answer my second research question for my final project.
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set()

distinct_colors = \
    ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4',
     '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff',
     '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1',
     '#000075', '#808080', '#ffffff']


def plot_genre_count_yearly(data, top_n=15):
    """Plots the yearly count of the top_n genres

    Parameters
    ----------
    data : DataFrame
        Pandas DataFrame that contains anime show data
    top_n : Integer
        Determines how many genres that will be placed onto the graph

    Notes
    -----
    Visualization Type: Line Plot
    File Path: plots/rq2_genres_yearly.png
    If the top_n value goes over the length of "distinct_colors", the palette
        will be shifted back to the default, which has indistinct colors
    Top_n is determined by the overall amount of anime made with the genre
    """

    yearly = data[["genre", "aired_from_year"]]
    # The line below prevents 2018 b/c the data was scraped during that year,
    # therefore incomplete
    yearly = data[data["aired_from_year"] < 2018]
    yearly = pd.concat([yearly["aired_from_year"],
                        pd.get_dummies(yearly["genre"]
                        .str.split(", ", expand=True),
                        prefix="", prefix_sep="")], axis=1)
    yearly = yearly.groupby("aired_from_year").sum() \
        .groupby(level=0, axis=1).sum().reset_index()

    top_genres = data["genre"].str.split(", ", expand=True).stack() \
        .str.get_dummies().sum().sort_values(ascending=False) \
        .iloc[:top_n]
    yearly = \
        yearly.loc[:, yearly.columns.isin(list(top_genres.index)
                                          + ["aired_from_year"])]

    palette = distinct_colors[:top_n] if top_n < len(distinct_colors) else None

    fig, ax = plt.subplots()
    fig.set_size_inches(15, 8)
    sns.lineplot(x="aired_from_year", y="value", hue="Genre",
                 data=pd.melt(yearly, ["aired_from_year"])
                 .rename(columns={"variable": "Genre"}),
                 palette=palette, ax=ax)
    fig.suptitle(f"Top {top_n} Genres by Year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Amount of Anime")
    ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0)
    fig.savefig("plots/rq2_genres_yearly.png", bbox_inches="tight")


def plot_genre_score_yearly(data, top_n=10):
    """Plots the yearly score average of the top_n genres

    Parameters
    ----------
    data : DataFrame
        Pandas DataFrame that contains anime show data
    top_n : Integer
        Determines how many genres that will be placed onto the graph

    Notes
    -----
    Visualization Type: Line Plot
    File Path: plots/rq2_genre_score_yearly.png
    If the top_n value goes over the length of "distinct_colors", the palette
        will be shifted back to the default, which has indistinct colors
    Top_n is determined by the average scores of anime made with the genre
    """

    yearly = data[["genre", "aired_from_year", "score"]].copy()
    yearly["genre"] = yearly["genre"].str.split(", ")
    yearly = yearly.explode("genre").groupby(["genre", "aired_from_year"]) \
        .mean().reset_index()

    top_genres = data[["genre", "score"]].copy()
    top_genres["genre"] = top_genres["genre"].str.split(", ")
    top_genres = top_genres.explode("genre").groupby("genre") \
        .mean().sort_values("score", ascending=False) \
        .reset_index().iloc[:top_n]

    palette = distinct_colors[:top_n] if top_n < len(distinct_colors) else None

    fig, ax = plt.subplots()
    fig.set_size_inches(15, 8)
    sns.lineplot(x="aired_from_year", y="score", hue="genre",
                 data=yearly[yearly["genre"].isin(top_genres["genre"])],
                 palette=palette, ax=ax)
    fig.suptitle(f"Top {top_n} Highly Rated Genre's Average Score by Year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Score out of Ten")
    ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0)
    fig.savefig("plots/rq2_genre_score_yearly.png", bbox_inches="tight")
    plt.close(fig)


def plot_genres_multi(data, name="multi_genre", add="before 2019"):
    """Plots the amount of each genre taking into account all tags

    Parameters
    ----------
    data : DataFrame
        Pandas DataFrame that contains anime show data
    name : String
        Determines name of the file
    add: String
        An addition to the title of the plot

    Notes
    -----
    Visualization Type: Bar Plot
    File Path: plots/rq2_{name}.png
    """

    genres = data["genre"].str.split(", ", expand=True).stack() \
        .str.get_dummies().sum().sort_values(ascending=False)

    fig, ax = plt.subplots()
    fig.set_size_inches(15, 10)
    fig.suptitle("Amount of Animes tagged with a Genre "
                 f"{add} (Includes Multi-Labels)")

    sns.barplot(x=genres.index, y=genres.values, ax=ax)
    ax.set_xlabel("Genres")
    ax.set_ylabel("Amount of Anime")
    plt.xticks(rotation=45, ha="right")
    fig.savefig(f"plots/rq2_{name}.png", bbox_inches="tight")
    plt.close(fig)


def plot_genres_first(data, name="main_genre", add="before 2019"):
    """Plots the amount of each genre taking into account primary tags

    Parameters
    ----------
    data : DataFrame
        Pandas DataFrame that contains anime show data
    name : String
        Determines name of the file
    add: String
        An addition to the title of the plot

    Notes
    -----
    Visualization Type: Bar Plot
    File Path: plots/rq2_{name}.png
    """

    genres = \
        data["genre"].str.split(", ", expand=True, n=1)[0].value_counts()

    fig, ax = plt.subplots()
    fig.set_size_inches(15, 10)
    sns.barplot(x=genres.index, y=genres.values, ax=ax)
    fig.suptitle(f"Amount of Animes with Main Genre {add} (First Tag)")
    ax.set_xlabel("Genres")
    ax.set_ylabel("Amount of Anime")
    plt.xticks(rotation=45, ha="right")
    fig.savefig(f"plots/rq2_{name}.png", bbox_inches="tight")
    plt.close(fig)


def plot_average_scores(data):
    """Plots the score average of the anime genres

    Parameters
    ----------
    data : DataFrame
        Pandas DataFrame that contains anime show data
    top_n : Integer
        Determines how many genres that will be placed onto the graph

    Notes
    -----
    Visualization Type: Bar Plot
    File Path: plots/rq2_average_genre_score.png
    """

    info = data[["genre", "score"]].copy()
    info["genre"] = info["genre"].str.split(", ")
    info = info.explode("genre").groupby("genre") \
        .mean().reset_index().sort_values("score", ascending=False)

    fig, ax = plt.subplots()
    fig.set_size_inches(16, 8)
    fig.suptitle("Average Scores for a Genre")

    sns.barplot(x="genre", y="score", data=info, ax=ax)
    ax.set_xlabel("Genres")
    ax.set_ylabel("Score out of Ten")
    ax.set_ylim(6, 8)
    plt.xticks(rotation=45, ha="right")
    fig.savefig("plots/rq2_average_genre_score.png", bbox_inches="tight")
    plt.close(fig)


def main(anime_data, data_2019):
    """
    Runs all the data analysis and visualization for research question two

    Parameters
    ----------
    anime_data : DataFrame
        Pandas DataFrame that contains anime show data before 2018
    data_2019 : DataFrame
        Pandas DataFrame that contains anime show data in 2019
    """

    plot_genres_multi(anime_data)
    plot_genres_first(anime_data)
    plot_genres_multi(data_2019, "multi_genre2019", "in 2019")
    plot_genres_first(data_2019, "main_genre2019", "in 2019")
    plot_genre_count_yearly(anime_data)
    plot_genre_score_yearly(anime_data)
    plot_average_scores(anime_data)
