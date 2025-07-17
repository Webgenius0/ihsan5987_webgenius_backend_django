import os
from SmallTalk.update_me import *


import pandas as pd
from SmallTalk.update_me import generate_update_me_element
from SmallTalk.recommendation import generate_recommendation

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
    for subtopic in categories:  # remove the index 2 if need to generate the update_me elemts for all topics
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

