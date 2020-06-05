"""
KV Le
CSE 163 AG
Final Project

A script that has multiple functions that manipulate/visualize data about
My Anime List to answer my fourth research question for my final project.
"""

import os
import graphviz
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeRegressor, export_graphviz
from sklearn.metrics import mean_squared_error, mean_absolute_error
sns.set()
# The line below makes it so graphviz works. Please Redirect path if your
# GraphViz files are elsewhere
os.environ["PATH"] += os.pathsep + "D:/Program Files/Graphviz2.38/bin/"


def get_features(data, feature_removed=None):
    """Retrieves the features for a score/popularity machine learning model
    of the given dataset

    Parameters
    ----------
    data : DataFrame
        Pandas DataFrame that contains anime show data
    feature_removed : String
        A feature that will be removed from the data

    Returns
    -------
    DataFrame
        Returns a Pandas DataFrame that contains the features required for the
        Machine learning model
    """

    feature_names = \
        ["type", "episodes", "duration_min", "source", "genre", "studio"]
    if feature_removed:
        feature_names.remove(feature_removed)

    features = data[feature_names].copy()
    if "studio" in feature_names:
        features = features.loc[:, features.columns != "studio"] \
            .join(features["studio"].str.get_dummies(", ")
                  .add_prefix("studio_"))
    if "genre" in feature_names:
        features = features.loc[:, features.columns != "genre"] \
            .join(features["genre"].str.get_dummies(", ").add_prefix("genre_"))
    features = pd.get_dummies(features)
    return features


def train_model(data, max_depth=None, feature_removed=None):
    """Trains a machine learning model to predict popularity and score

    Parameters
    ----------
    data : DataFrame
        Pandas DataFrame that contains anime show data
    max_depth : Integer
        The maximum Decision Tree Depth the model can go. (Hyperparemeter)
    feature_removed : String
        A feature that is removed from consideration for the model

    Returns
    -------
    DecisionTreeRegressor
        Returns a Decision Tree Regressor model for the score model and
        favorites/popularity model
    """

    features = get_features(data, feature_removed)

    score_model = DecisionTreeRegressor(max_depth=max_depth)
    score_model.fit(features, data["score"])

    favorites_model = DecisionTreeRegressor(max_depth=max_depth)
    favorites_model.fit(features, data["favorites"])
    return score_model, favorites_model


def plot_optimal_depth(anime_data, anime_2019):
    """Plots the varying score/favorite model errors of different tree depths

    Parameters
    ----------
    anime_data : DataFrame
        Pandas DataFrame that contains anime show data before 2019
    anime_2019 : DataFrame
        Pandas DataFrame that contains anime show data in 2019

    Notes
    -----
    Visualization Type: Line Plot
    File Path: plots/rq4_optimal_depth.png
    """

    features = get_features(anime_2019). \
        reindex(columns=get_features(anime_data).columns, fill_value=0)

    score_info = {
        "depth": [],
        "error_type": [],
        "error_value": []
    }

    favorites_info = {
        "depth": [],
        "error_type": [],
        "error_value": []
    }

    for max_depth in range(1, 51, 2):
        score_model, favorites_model = \
            train_model(anime_data, max_depth)

        score_predictions, favorite_predictions = \
            score_model.predict(features), favorites_model.predict(features)

        score_info["depth"].append(max_depth)
        score_info["error_type"].append("Mean Absolute Error")
        score_info["error_value"] \
            .append(mean_absolute_error(anime_2019["score"],
                                        score_predictions))

        favorites_info["depth"].append(max_depth)
        favorites_info["error_type"].append("Mean Absolute Error")
        favorites_info["error_value"] \
            .append(mean_absolute_error(anime_2019["score"],
                                        favorite_predictions))

        score_info["depth"].append(max_depth)
        score_info["error_type"].append("Mean Squared Error")
        score_info["error_value"] \
            .append(mean_squared_error(anime_2019["score"],
                                       score_predictions))

    fig, axs = plt.subplots(2)
    fig.set_size_inches(15, 20)

    sns.lineplot(x="depth", y="error_value", hue="error_type",
                 data=score_info, ax=axs[0])
    axs[0].set_title("Relationship between Score Errors and Tree Depth")
    axs[0].set_xlabel("Tree Depth")
    axs[0].set_ylabel("Error Amount")

    sns.lineplot(x="depth", y="error_value", data=favorites_info, ax=axs[1])
    axs[1].set_title("Relationship between Favorites Mean Absolute Error " +
                     "and Tree Depth")
    axs[1].set_xlabel("Tree Depth")
    axs[1].set_ylabel("Error Amount")

    fig.savefig("plots/rq4_optimal_depth.png", bbox_inches="tight")
    plt.close(fig)


def plot_optimal_features(anime_data, anime_2019):
    """Plots change of score/favorite model errors of certain features removed

    Parameters
    ----------
    anime_data : DataFrame
        Pandas DataFrame that contains anime show data before 2019
    anime_2019 : DataFrame
        Pandas DataFrame that contains anime show data in 2019

    Notes
    -----
    Visualization Type: Bar Plot
    File Path: plots/rq4_optimal_features.png
    """

    score_info = {
        "feature_removed": [],
        "error_type": [],
        "error_value": []
    }

    favorites_info = {
        "feature_removed": [],
        "error_type": [],
        "error_value": []
    }

    for feature_removed in [None, "type", "episodes", "duration_min",
                            "source", "genre", "studio"]:
        score_model, favorites_model = \
            train_model(anime_data, 7, feature_removed)

        features = get_features(anime_2019). \
            reindex(columns=get_features(anime_data, feature_removed).columns,
                    fill_value=0)

        score_predictions, favorite_predictions = \
            score_model.predict(features), favorites_model.predict(features)

        score_info["feature_removed"].append(str(feature_removed))
        score_info["error_type"].append("Mean Absolute Error")
        score_info["error_value"] \
            .append(mean_absolute_error(anime_2019["score"],
                                        score_predictions))

        favorites_info["feature_removed"].append(str(feature_removed))
        favorites_info["error_type"].append("Mean Absolute Error")
        favorites_info["error_value"] \
            .append(mean_absolute_error(anime_2019["score"],
                                        favorite_predictions))

        score_info["feature_removed"].append(str(feature_removed))
        score_info["error_type"].append("Mean Squared Error")
        score_info["error_value"] \
            .append(mean_squared_error(anime_2019["score"],
                                       score_predictions))

    for col in score_info:
        if col == "error_value":
            og_error = score_info[col][0]
            score_info[col] = [error - og_error for error in score_info[col]]
        score_info[col] = score_info[col][2:]

    for col in favorites_info:
        if col == "error_value":
            og_error = favorites_info[col][0]
            favorites_info[col] = \
                [error - og_error for error in favorites_info[col]]
        favorites_info[col] = favorites_info[col][1:]

    fig, axs = plt.subplots(2)
    fig.set_size_inches(15, 20)

    axs[0].set_title("Change in Score Errors When Removing Features")
    sns.barplot(x="feature_removed", y="error_value", hue="error_type",
                data=score_info, ax=axs[0])
    axs[0].set_xlabel("Feature Removed")
    axs[0].set_ylabel("Error Change")
    axs[0].set_ylim(-.15, 0.15)
    axs[0].legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0)

    axs[1].set_title("Change in Favorite Mean Absolute Error " +
                     "When Removing Features")
    sns.barplot(x="feature_removed", y="error_value", palette=["Blue"],
                data=favorites_info, ax=axs[1])
    axs[1].set_xlabel("Feature Removed")
    axs[1].set_ylabel("Error Change")

    fig.savefig("plots/rq4_optimal_features.png", bbox_inches="tight")
    plt.close(fig)


def plot_tree(model, features, labels):
    """Plots the decision tree of a given machine learning model

    Parameters
    ----------
    model : SciKit Learn Decision Tree
        Machine Learning model that contains the tree schematic
    features : DataFrame
        The features for the learning model
    labels : DataFrame
        The label(s) for the learning model

    Notes
    -----
    Visualization Type: Decision Tree Plot
    File Path: plots/rq4_decision_tree.png
    """

    test = export_graphviz(model, feature_names=features.columns,
                           class_names=labels.unique(), leaves_parallel=True,
                           impurity=False, proportion=True, rounded=True,
                           filled=True, rotate=True,
                           special_characters=True)
    graph = graphviz.Source(test)
    png_bytes = graph.pipe(format='png')
    with open(f"plots/rq4_decision_tree.png", "wb") as f:
        f.write(png_bytes)


def main(anime_data, anime_2019):
    """
    Runs all the data analysis and visualization for research question four

    Parameters
    ----------
    anime_data : DataFrame
        Pandas DataFrame that contains anime show data before 2018
    data_2019 : DataFrame
        Pandas DataFrame that contains anime show data in 2019
    """

    plot_optimal_features(anime_data, anime_2019)
    plot_optimal_depth(anime_data, anime_2019)
    plot_tree(train_model(anime_data, 7)[0],
              get_features(anime_data), anime_data["score"])
