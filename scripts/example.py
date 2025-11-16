
# #Generate searchabr ourput
# from search_bar import *

# search_bar_obj = search_bar('fifa world cup', allow_options = False) # the options output can be shown  
# # search_bar_obj = search_bar('Formula 1, Racing', allow_options = False) 

# print(search_bar_obj)

# #Generate recommendation output 
# from .recommendation import *

# # #only one output json
# recommendation = generate_recommendation('soccer', prompt_version='v02')
# print(recommendation)

# #List with the recommendation outputs for all subcategories
# import pandas as pd
# categories_file = 'Categories.xlsx'
# df = pd.read_excel(categories_file)
# subcategories = df['Subcategory'].dropna().tolist()

# recommendations = []

# for subcat in subcategories[:2]:

#     recommendations.append(generate_recommendation(subcat, prompt_version='v02'))



# # # generate set of 5 trendning topics 
from .trending import *

trending = generate_trending_set() #set of 5 trending topics

print(trending)




# #geberate set of 3 update me news 

# from .update_me import *
# set = generate_update_me_news_set() # news set, 3 news, list of dictionaries

# print('set result', set)

# #generate output for each topic 

# categories_file = 'Categories.xlsx'
# df = pd.read_excel(categories_file)
# subcategories = df['Subcategory'].dropna().tolist()

# update_me = []

# update_me = []

# for subtopic in subcategories[:2]:  #remove the index 2 if need to generate the update_me elemts for all topics 
#         update_me.append(generate_update_me_element(keywords = subtopic, 
#                                                     prompt_type = 'update_me_general', 
#                                                     categories_file = categories_file,  
#                                                     prompt_version='v01'))     



# # save top 3 news to database
# json_data_list = [
#     {
#         'category': 'Politics & Society',
#         'subcategory': 'Foreign Policy & International Relations',
#         'topic': 'Trump jointly signs Thailand-Cambodia ceasefire agreement at ASEAN summit',
#         'short_info': ['Thailand and Cambodia signed an enhanced ceasefire agreement at the ASEAN summit in Kuala Lumpur in the presence of US President Donald Trump.', 'The agreement builds on a truce reached three months ago, with Trump using the threat of tariffs to broker peace.', 'The deal involves the release of Cambodian soldiers by Thailand and the deployment of Malaysian troops to ensure lasting peace.'],
#         'reference_url': 'https://www.aljazeera.com/news/2025/10/26/trump-jointly-signs-thailand-cambodia-ceasefire-agreement-at-asean-summit?traffic_source=rss',
#         'background_story': {'context_history': 'Thailand and Cambodia have a history of border disputes, with the recent conflict resulting in a deadly five-day clash in July.', 'current_developments': 'The signing of the ceasefire agreement in the presence of Trump marks a significant step towards peace in the region.', 'relevance': 'The agreement not only addresses immediate tensions but also showcases the role of international diplomacy in resolving conflicts.'},
#         'picture_url': 'http://www.bing.com/th?id=OVFT.HF5ylv5-E8IhzpNyOav-py&pid=News'
#     },
#     {
#         'category': 'Politics & Society',
#         'subcategory': 'Foreign Policy & International Relations',
#         'topic': 'Venezuela’s Maduro says the US is ‘fabricating’ a war against him',
#         'short_info': ['Venezuelan President Maduro accuses the US of fabricating a war against him as the US sends its largest warship towards Venezuela.', 'Tensions are escalating in the region amid speculation of an attempt to overthrow the Venezuelan government.', 'US forces have bombed boats in the Caribbean, leading to at least 43 deaths.'],
#         'reference_url': 'https://www.aljazeera.com/news/2025/10/26/venezuelas-maduro-says-the-us-is-fabricating-a-war-against-him?traffic_source=rss',
#         'background_story': {'context_history': 'Venezuela has been in political turmoil with accusations against Maduro of election fraud and calls for his removal.', 'current_developments': 'The US is increasing its military presence in the region, prompting Maduro to conduct military exercises against potential threats.', 'relevance': 'The situation highlights the ongoing power struggle in Venezuela and the broader implications for regional stability.'},
#         'picture_url': 'http://www.bing.com/th?id=OVFT.Q9laYtjtfx48VpZ3Y6Id-S&pid=News'
#     },
#     {
#         'category': 'Science & Technology',
#         'subcategory': 'Natural Sciences',
#         'topic': 'Hurricane Melissa, now Category 3, threatens heavy floods in Jamaica, Haiti',
#         'short_info': ['Hurricane Melissa has rapidly strengthened into a major Category 3 hurricane, posing a significant threat of catastrophic flooding in Jamaica and Haiti.', 'Forecasters warn of potentially devastating consequences as Melissa moves towards Jamaica, prompting authorities to take precautionary measures.', 'The slow-moving storm has already caused casualties and significant damage in the Caribbean region.'],
#         'reference_url': 'https://www.aljazeera.com/news/2025/10/26/hurricane-melissa-now-category-3-threatens-heavy-floods-in-jamaica-haiti?traffic_source=rss',
#         'background_story': {'context_history': 'Hurricane Melissa has rapidly strengthened into a major Category 3 hurricane, with potential catastrophic consequences for Jamaica and Haiti.', 'current_developments': 'Authorities are on high alert as Melissa approaches Jamaica, with forecasts predicting heavy rainfall and dangerous flooding in the region.', 'relevance': 'The slow movement of the storm raises concerns for prolonged impact and potential devastation in the affected areas, highlighting the urgent need for preparedness and response measures.'},
#         'picture_url': 'http://www.bing.com/th?id=OVFT.FjqpsEshcLDUevZtGBJGVy&pid=News'
#     }
# ]

# from apps.home.models import Category, Subcategory, Topic, UpdateMe

# def save_top3_news():
#     for news in json_data_list:
#         try:
#             category, created = Category.objects.get_or_create(
#                 category_name=news["category"]
#             )
#             subcategory, created = Subcategory.objects.get_or_create(
#                 subcategory_name=news["subcategory"]
#             )
#             topic, created = Topic.objects.get_or_create(
#                 name=news["topic"]
#             )
#             UpdateMe.objects.create(
#                 category=category,
#                 subcategory=subcategory,
#                 topic=topic,
#                 short_info=news["short_info"],
#                 reference_url=news["reference_url"],
#                 background_story=news["background_story"],
#                 picture_url=news["picture_url"],
#                 is_top3=True,
#             )
#             print("Top 3 UpdateMe news saved successfully")
#         except Exception as e:
#             print(f"Error saving Top 3 UpdateMe news: {e}")
