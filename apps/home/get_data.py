import os
import pandas as pd
from SmallTalk.update_me import *


import pandas as pd
from SmallTalk.update_me import generate_update_me_element
from SmallTalk.recommendation import generate_recommendation
from SmallTalk.trending import generate_trending_set

categories_file = "Categories.xlsx"
categories_path = os.path.join(os.path.dirname(__file__), categories_file)

# Read the Excel file
df = pd.read_excel(categories_path)

# print(df.head())

# categories_data = os.path.join('Categories>xlsx')

# print(categories_data)
# print(categories_file)
# df = pd.read_excel(categories_file)


def get_update_me (categories):
    update_me = []
    for subtopic in categories:
        update_me.append(
            generate_update_me_element(
                keywords=subtopic,
                prompt_type="update_me_general",
                categories_file=categories_path,
                prompt_version="v01",
            )
        )

    return update_me

def get_recommendations(categories):
    recommendations = []
    for subcat in categories:
        recommendations.append(
            generate_recommendation(
                subcat, prompt_version="v02", categories_file=categories_path
            )
        )
    return recommendations

# def get_trending_now():
#     import concurrent.futures
#     # categories_file = os.path.join(os.path.dirname(__file__), 'Categories.xlsx')
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         future = executor.submit(generate_trending_set)
#         data = future.result()  # Waits for the result

#     if data:
#         print("generated data", data)
#         return data
#     return []

import concurrent

def get_trending_now():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(generate_trending_set)
        data = future.result()  # Waits for the result

    if data:
        return data
    return []
