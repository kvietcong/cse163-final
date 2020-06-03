"""
KV Le
CSE 163 AG
Final Project

A script that has multiple functions that manipulate/visualize data about
My Anime List to answer my third research question for my final project.
"""

import seaborn as sns
import matplotlib.pyplot as plt
sns.set()

distinct_colors = \
    ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4',
     '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff',
     '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1',
     '#000075', '#808080', '#ffffff']


def plot_yearly_studio_score(data, top_n=20):
    """Plots the average score per year for the top_n studios

    Parameters
    ----------
    data : DataFrame
        Pandas DataFrame that contains anime show data
    top_n: Integer
        The amount of top studios that the plot will contain

    Notes
    -----
    Visualization Type: Line Plot
    File Path: plots/rq3_{top_n}studios_yearly_score.png
    If the top_n value goes over the length of "distinct_colors", the palette
        will be shifted back to the default, which has indistinct colors
    Top_n is determined by the average scores of anime made with the studio
    """

    info = data[["studio", "score", "aired_from_year"]].copy()
    info["studio"] = info["studio"].str.split(", ")
    info = info.explode("studio").groupby(["studio", "aired_from_year"]) \
        .mean().sort_values("score", ascending=False).reset_index()
    top_studios = info.groupby("studio").mean() \
        .sort_values("score", ascending=False).iloc[:top_n]["score"]
    info = info[info["studio"].isin(top_studios.index)]

    palette = distinct_colors[:top_n] if top_n < len(distinct_colors) else None

    fig, ax = plt.subplots()
    fig.set_size_inches(15, 10)
    sns.lineplot(x="aired_from_year", y="score", hue="studio",
                 palette=palette, data=info, ax=ax)
    fig.suptitle(f"Average Yearly Score of the Top {top_n} Studios")
    ax.set_xlabel("Year")
    ax.set_ylabel("Score out of Ten")
    ax.set_ylim(0, 10)
    ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0)
    fig.savefig(f"plots/rq3_{top_n}studios_yearly_score.png",
                bbox_inches="tight")
    plt.close(fig)


def plot_studio_averages(data):
    """Plots the average score for anime studios

    Parameters
    ----------
    data : DataFrame
        Pandas DataFrame that contains anime show data

    Notes
    -----
    Visualization Type: Bar Plot
    File Path: plots/rq3_{top_n}studios_yearly_score.png
    """

    info = data[["studio", "score"]].copy()
    info["studio"] = info["studio"].str.split(", ")
    info = info.explode("studio").groupby("studio").mean() \
        .sort_values("score", ascending=False).reset_index()

    fig, ax = plt.subplots()
    fig.set_size_inches(15, 10)
    sns.barplot(x="studio", y="score",
                data=info.iloc[:25], ax=ax)
    fig.suptitle("Top 25 Studio Scores")
    ax.set_xlabel("Studios")
    ax.set_ylabel("Score out of Ten")
    ax.set_ylim(6, 9)
    plt.xticks(rotation=45, ha="right")
    fig.savefig("plots/rq3_best_studio_scores.png", bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots()
    fig.set_size_inches(15, 10)
    sns.barplot(x="studio", y="score",
                data=info.iloc[:-25:-1], ax=ax)
    fig.suptitle("Worst 25 Studio Scores")
    ax.set_xlabel("Studios")
    ax.set_ylabel("Score out of Ten")
    ax.set_ylim(2, 6)
    plt.xticks(rotation=45, ha="right")
    fig.savefig("plots/rq3_worst_studio_scores.png", bbox_inches="tight")
    plt.close(fig)


def plot_genre_average(data, top_n=5, genres=None):
    """Plots the top and bottom 25 studio scores for the top_n genres

    Parameters
    ----------
    data : DataFrame
        Pandas DataFrame that contains anime show data
    top_n: Integer
        The amount of top studios that the plot will contain
    genres: List
        List of genres that can override top_n

    Notes
    -----
    Visualization Type: Line Plot
    File Path: plots/rq3_{top_n}studios_yearly_score.png
    If the top_n value goes over the length of "distinct_colors", the palette
        will be shifted back to the default, which has indistinct colors
    Top_n is determined by the average scores of genre
    """

    info = data[["genre", "studio", "score"]].copy()
    info["studio"] = info["studio"].str.split(", ")
    info = info.explode("studio")
    info["genre"] = info["genre"].str.split(", ")
    info = info.explode("genre")
    if genres:
        top_genres = genres
    else:
        top_genres = \
            info.groupby("genre").mean() \
            .sort_values("score", ascending=False)
        top_genres = \
            top_genres.iloc[:(top_n if top_n else len(top_genres))].index

    for genre in top_genres:
        genre_info = info[info["genre"] == genre]
        genre_info = genre_info.groupby("studio").mean()
        genre_info = genre_info.sort_values("score", ascending=False) \
            .reset_index()
        fig, axs = plt.subplots(2)
        fig.set_size_inches(16, 20)

        axs[0].set_title(f"Top 25 {genre} Studios")
        sns.barplot(x="studio", y="score",
                    data=genre_info.iloc[:25], ax=axs[0])
        axs[0].set_xlabel("Studio")
        axs[0].set_ylabel("Score out of Ten")
        plt.setp(axs[0].get_xticklabels(), ha="right", rotation=45)

        axs[1].set_title(f"Bottom 25 {genre} Studios")
        sns.barplot(x="studio", y="score",
                    data=genre_info.iloc[:-25:-1], ax=axs[1])
        axs[1].set_xlabel("Studio")
        axs[1].set_ylabel("Score out of Ten")
        plt.xticks(rotation=45, ha="right")

        plt.tight_layout()

        if top_n:
            fig.savefig(f"plots/rq3_genre_{genre.lower()}_scores.png",
                        bbox_inches="tight")
        else:
            fig.savefig(f"plots/rq3_genres/rq3_{genre.lower()}_scores.png",
                        bbox_inches="tight")
        plt.close(fig)


def main(anime_data):
    """
    Runs all the data analysis and visualization for research question three

    Parameters
    ----------
    anime_data : DataFrame
        Pandas DataFrame that contains anime show data before 2018
    """

    plot_yearly_studio_score(anime_data)
    plot_yearly_studio_score(anime_data, 50)
    plot_studio_averages(anime_data)
    plot_genre_average(anime_data)
    plot_genre_average(anime_data, genres=["Comedy", "Romance", "Action"])
