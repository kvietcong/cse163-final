# An Analysis of Anime and Anime Consumers Based on MyAnimeList (MAL)

Report by KV Le

CSE 163: Intermediate Data Programming

Professor: Hunter Schafer

Project Mentor: Trinh Nguyen

The following contents of this file will be the instructions on how to use the code written for my CSE163 Final Project about MAL users. The full report can be found within this directory named "report.pdf"

> **Note:** If you happen to only have this README or are missing files, you can get all the required files at https://github.com/derpyasianpanda/cse163-final

## Required Libraries

- Pandas
- GraphViz
    - Note: You must also install the GraphViz Executable Packages here https://www.graphviz.org/download/ and redirect any os pathing to that directory
- Seaborn
- MatPlotLib
- SciKit Learn

> **Installation Line:** pip install pandas graphviz seaborn matplotlib sklearn

## Required Data

You will need to have the following Original Data:
- anime_cleaned.csv ==> data/original_data/anime_azathoth.csv
    - Contains cleaned information on Anime released before 2019 by Azathoth
- animelists_cleaned.csv ==> data/original_data/users_animelists_azathoth.csv
    - Contains cleaned MAL user anime lists by Azathoth
- users_cleaned.csv ==> data/original_data/animelist_azathoth.csv
    - Contains cleaned information about many MAL users by Azathoth

> **Note:** All original Data retrieved from https://www.kaggle.com/azathoth42/myanimelist was renamed to match the files above and put into a new directories

## Steps for Result Reproduction
1. Retrieve original data. Refer to the "Required Data" and retrieve the cleaned sets from https://www.kaggle.com/azathoth42/myanimelist. Download, rename, and relocate the cleaned data in to the proper folders.

    > **Note:** If you want a premade data folder without any renaming or processing, download it at https://drive.google.com/drive/folders/1-HOV_2Xe9E9mNgtxm6sE6K0pD750JebP?usp=sharing
2. Make sure there are the proper files and the correct folder structure
    ```
    Main Directory
    │   data_analyzing.py
    │   data_retrieve_cleaning.py
    │   ...
    │
    └───data
    │   │
    │   └───original_data
    │       │   anime_cleaned.csv
    │       │   animelists_cleaned.csv
    │       │   users_cleaned.csv
    │
    └───lists
    │
    └───plots
        │
        └───rq3_genres
    ```
3. Run data_retrieve_cleaning.py to filter out uneeded details and retrieve more data.
    - This will take a long time due to needing to retrieve hundreds of anime from 2019 on an API that rate limits
4. Run data_analyze.py to generate all necessary data analysis and visualizations
    - In the rq_one.py file, please read the function comments within "plot_gender_genres" to see if you must create a new pickle
    - The first run through will be pretty long due to rq_one.py. You can comment out lines in data_analyzing.py to fit your needs
5. Hopefully Enjoy the Results!