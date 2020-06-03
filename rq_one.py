"""
KV Le
CSE 163 AG
Final Project

A script that has multiple functions that manipulate/visualize data about
My Anime List to answer my first research question for my final project.
"""

import json
import pickle
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
sns.set()


def average_user(data):
    """Retrieves the averages of the given user data

    Parameters
    ----------
    data : DataFrame
        Pandas DataFrame that contains anime user data

    Returns
    -------
    Dictionary
        Returns the averages of the user data in a dictionary
    """

    averages = {
        "age":
            2020 - pd.to_numeric(data["birth_date"]
                                 .str.split("-", expand=True, n=1)[0]).mean(),
        "score": data["stats_mean_score"].mean(),
        "days_watched": data["user_days_spent_watching"].mean(),
        "episodes": data["stats_episodes"].mean(),
        "completed": data["user_completed"].mean(),
        "watching": data["user_watching"].mean(),
        "planned": data["user_plantowatch"].mean(),
        "onhold": data["user_onhold"].mean(),
        "dropped": data["user_dropped"].mean()
    }
    return averages


def average_by_gender(data):
    """Retrieves the averages of a Male and Female MAL user

    Parameters
    ----------
    data : DataFrame
        Pandas DataFrame that contains anime user data

    Returns
    -------
    Dictionary
        Returns the averages of the genders in a dictionary
    """

    averages = {
        "male": average_user(data[data["gender"] == "Male"]),
        "female": average_user(data[data["gender"] == "Female"])
    }
    return averages


def plot_averages(avg, g_avg, name="averages"):
    """Plots different gendered averages and overall average for the data

    Parameters
    ----------
    avg : Dictionary
        Pandas DataFrame that contains overall average data
    avg : Dictionary
        Pandas DataFrame that contains gendered average data
    name : String
        File name to be saved as

    Notes
    -----
    Visualization Type: Bar Plots
    File Path: plots/rq1_{name}.png
    """

    g_avg = pd.DataFrame.from_dict(g_avg).reset_index()
    g_avg = g_avg.rename(columns={"index": "category"})
    labels = [("Average Age", "Years"), ("Average Score", "Score Out of 10"),
              ("Days Watched", "Days"),
              ("Average Episodes Watched", "Episodes"),
              ("Average Shows Completed", "Shows"),
              ("Average Shows Watching", "Shows"),
              ("Average Shows Planned", "Shows"),
              ("Average Shows On Hold", "Shows"),
              ("Average Shows Dropped", "Shows")]

    fig, axs = plt.subplots(nrows=3, ncols=3)
    fig.set_size_inches(20, 15)
    for idx, row in g_avg.iterrows():
        ax = axs[idx // 3, idx % 3]
        sns.barplot(x=row["male":"female"].index, palette=["Blue", "Red"],
                    y=row["male":"female"].values, ax=ax)
        ax.set_title(labels[idx][0])
        ax.set_ylabel(labels[idx][1])
        ax.axhline(avg[row["category"]], color="g")
        ax.legend(handles=[mlines.Line2D([], [], color="g",
                           label="Overall Average")])
    fig.savefig(f"plots/rq1_{name}.png", bbox_inches="tight")
    plt.close(fig)


def plot_time_spent(data, name="time_spent"):
    """Plots the time spent watching anime

    Parameters
    ----------
    data : DataFrame
        Pandas DataFrame that contains anime user data
    name : String
        File name to be saved as

    Notes
    -----
    Visualization Type: Scatter Plots
    File Path: plots/rq1_{name}.png
    """

    plot_info = {
        "genders": [["Female", "Male"], ["Female"], ["Male"]],
        "colors": [["blue", "red"], ["red"], ["blue"]]
    }

    fig, axs = plt.subplots(3)
    fig.suptitle("Amount of time spent on Anime")
    fig.set_size_inches(9, 12)

    for idx, ax in enumerate(axs):
        sns.scatterplot(x="age", y="user_days_spent_watching", alpha=0.3,
                        hue="gender", ax=ax,
                        palette=plot_info["colors"][idx],
                        data=data[data["gender"]
                                  .isin(plot_info["genders"][idx])])
        ax.set_xlabel("Age")
        ax.set_ylabel("Days Spent Watching")
    fig.savefig(f"plots/rq1_{name}.png", bbox_inches="tight")
    plt.close(fig)


def save_lists(info_list):
    """Saves information into a text file that can be read later

    Parameters
    ----------
    info_list : List
        List of Dictionaries to pretty print into a text file

    Notes
    -----
    File Path: lists/rq1_{name}.txt
    """

    for info in info_list:
        name = info[0]
        data = info[1]
        with open(f"lists/rq1_{name}.txt", "w") as file:
            file.write(json.dumps(data, indent=4))


def plot_gender_genres(anime_data, user_data):
    """Plots the how genres vary by genders

    Parameters
    ----------
    anime_data : DataFrame
        Pandas DataFrame that contains anime data
    anime_data : DataFrame
        Pandas DataFrame that contains MAL user data

    Notes
    -----
    Visualization Type: Bar Plots
    File Path: plots/rq1_gender_genres.png and plots/rq1_gender_genres2.png
    """

    # Uncomment code below if the genre_by_gender.pkl doesn't exist
    # user_lists = pd.read_csv("data/user_animelists_cleaned.csv")
    # lists = user_lists[["anime_id", "username"]].copy()
    # users = user_data[["username", "gender"]].copy()
    # anime = anime_data[["anime_id", "genre", "studio"]].copy()
    # data = pd.merge(lists, users)
    # data = pd.merge(data, anime, how="left")
    # data = data.dropna()
    # data["genre"] = data["genre"].str.split(", ")
    # data = data.explode("genre").groupby(["gender", "genre"]) \
    #     .agg("count").reset_index()[["gender", "genre", "anime_id"]] \
    #     .rename(columns={"anime_id": "count"})
    # with open("data/genre_gender.pkl", "wb") as f:
    #     pickle.dump(data, f)

    # Uncomment code below if the genre_by_gender.pkl does exist
    with open("data/genre_by_gender.pkl", "rb") as f:
        data = pickle.load(f).sort_values("count", ascending=False)

    # Keep This Code!
    fig, ax = plt.subplots()
    fig.set_size_inches(25, 10)
    sns.barplot(x="genre", y="count", hue="gender", palette=["Blue", "Red"],
                data=data, ax=ax)
    fig.suptitle("Genre by genders")
    ax.set_xlabel("Genre")
    ax.set_ylabel("Users")
    plt.xticks(rotation=45, ha="right")
    fig.savefig("plots/rq1_gender_genres.png", bbox_inches="tight")
    plt.close(fig)

    ratios = {
        "genre": [],
        "gender": [],
        "ratio": []
    }
    total_female, total_male = data.groupby("gender").sum()["count"].values
    for genre in data["genre"]:
        male_ratio = data[((data["genre"] == genre) &
                          (data["gender"] == "Male"))]["count"] \
            .squeeze() / total_male
        female_ratio = data[((data["genre"] == genre) &
                            (data["gender"] == "Female"))]["count"] \
            .squeeze() / total_female
        ratios["genre"].append(genre)
        ratios["gender"].append("Male")
        ratios["ratio"].append(male_ratio)
        ratios["genre"].append(genre)
        ratios["gender"].append("Female")
        ratios["ratio"].append(female_ratio)

    ratios = pd.DataFrame.from_dict(ratios) \
        .sort_values("ratio", ascending=False)
    fig, ax = plt.subplots()
    fig.set_size_inches(25, 10)
    sns.barplot(x="genre", y="ratio", hue="gender", palette=["Blue", "Red"],
                data=ratios, ax=ax)
    fig.suptitle("Genre Ratios by Gender")
    ax.set_xlabel("Genre")
    ax.set_ylabel("Ratio of Gender Who Watch")
    plt.xticks(rotation=45, ha="right")
    fig.savefig("plots/rq1_gender_genres2.png", bbox_inches="tight")
    plt.close(fig)


def main(anime_data, user_data):
    """
    Runs all the data analysis and visualization for research question one

    Parameters
    ----------
    user_data : DataFrame
        Pandas DataFrame that contains information about a MAL user
    """

    averages = average_user(user_data)
    gender_averages = average_by_gender(user_data)
    plot_averages(averages, gender_averages)
    plot_time_spent(user_data)
    save_lists([("overall_avg", averages), ("gendered_avg", gender_averages)])
    plot_gender_genres(anime_data, user_data)
