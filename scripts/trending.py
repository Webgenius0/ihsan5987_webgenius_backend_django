# trending.py
import os
from .api_utils import *
from .llm_utils import *
from datetime import datetime, timedelta


file_name = "Categories.xlsx"
file_path = os.path.join(os.path.dirname(__file__), file_name)
template_dir = os.path.join(os.path.dirname(__file__), "prompts")


def generate_trending_element(keywords, prompt_version="v02", categories_file = file_path, **model_params):

    df = pd.read_excel(categories_file)

    #news = get_news_from_google_news(keywords)

    #news_content = [news_item['content'] for news_item in news if 'content' in news_item]
    #links = [news_item['url'] for news_item in news if 'url' in news_item]

    date = (datetime.now()- timedelta(days=30)).strftime("%d.%m.%Y")

    system_prompt  = f''' You are the assistant that will help quickly get exhaustive information on a certain trending topic for update briefings.
           Output Rules:
              Return the full, detailed JSON object with the following structure:

              {{
      "topic": "Short title for the topic containing 2-3 words (e.g., 'Remote Work', 'Electric Vehicles').",
      "category": "<Placeholder>",
      "subcategory": "<Subcategory, e.g., NFL, Politics, Tech>",
      "description": "<Description of the trending topic, 2-3 sentances>",
      "why_is_it_trending": {{"<Subheader 1>":  "<Explanation of why it's trending>",
                              "<Subheader 2>":  "<Explanation of why it's trending>",
                              "<Subheader 3>":  "<Explanation of why it's trending>" 
     }},
      "key_points": {{"<Subheader 1>":  "<Key detail",
                      "<Subheader 2>":  "<Key detail>",
                      "<Subheader 3>":  "<Key detail>" 
     }},
      "overlook_what_might_happen_next": {{"<Subheader 1>":  "<Outlook or prediction>",
                                          "<Subheader 2>":  "<Outlook or prediction>",
                                           "<Subheader 3>":  "<Outlook or prediction>" 
     }},
        "picture_url": "placeholder"
    }}


            Critical Requirements:
            - Always respond in valid JSON only (no extra commentary, no markdown).
            - Do not include any additional text or explanation outside the JSON.

            Be precise and coincise, Dont use Wikipedia or Wikimedia
            The latest news can be from the {date}.

        '''
        


    user_input = build_prompt(prompt_type = 'trending',     
                          prompt_version = prompt_version,
                            keywords=keywords, news = "", #news_content, 
                            article_text= '',
                            reference_url = '',
                            extra_links = "",#links,
                            subcategories = df['Subcategory'].dropna().tolist())


    raw_response = generate_perplexity_output(system_prompt, user_input)
    #return raw_response
    valid, parsed_json = verify_and_fix_json(raw_response['choices'][0]['message']['content'])
    parsed_json['picture_url'] = get_image_url(parsed_json['topic'])
    #valid = True
    #parsed_json = raw_response
    #parsed_json['picture_url'] = news[0]['image'] 
    #parsed_json['links_and_sources'] = links
    
    category = df[df['Subcategory'] == parsed_json.get('subcategory', '')]['Category'].values[0] if not df[df['Subcategory'] == parsed_json.get('subcategory', '')].empty else 'General'
    parsed_json['category'] = category

    if valid:
        return parsed_json
    else:
        print("Could not parse/fix the JSON response.")
        return None


def generate_trending_set(keywords = None , num_elements=5, prompt_version="v02", categories_file = file_path, **model_params):
 
    if not keywords:
        keywords = get_trending_topics()
    trending = []
    print(keywords)

    for trend in keywords:
        print(f'generating trend for: {trend}')

        trend_json = generate_trending_element(trend, prompt_version=prompt_version, categories_file=categories_file, **model_params)
        if trend_json:
            trending.append(trend_json)


    return trending

def validate_trending_output(output_json):
    """
    Validate that the trending JSON conforms to the expected schema.

    Expected Schema:
    {
      "topic": "string",
      "category": "string",
      "subcategory": "string",
      "description": "string",
      "why_is_it_trending": ["string", ...],
      "key_points": ["string", ...],
      "overlook_what_might_happen_next": ["string", ...]
    }

    Args:
        output_json: The JSON object to validate.

    Returns:
        tuple: A tuple containing:
            - is_valid (bool): True if the JSON is valid, False otherwise.
            - errors (list): A list of strings describing any validation errors.
    """
    errors = []

    if not isinstance(output_json, dict):
        errors.append("Top-level JSON must be an object.")
        return False, errors

    # Check for required string fields
    string_fields = ["topic", "category", "subcategory", "description"]
    for field in string_fields:
        if field not in output_json:
            errors.append(f"Missing required field: '{field}'.")
        elif not isinstance(output_json[field], str):
            errors.append(f"Field '{field}' must be a string, but found {type(output_json[field]).__name__}.")

    # Check for required list of strings fields
    list_fields = ["why_is_it_trending", "key_points", "overlook_what_might_happen_next"]
    for field in list_fields:
        if field not in output_json:
            errors.append(f"Missing required field: '{field}'.")
        elif not isinstance(output_json[field], list):
            errors.append(f"Field '{field}' must be a list, but found {type(output_json[field]).__name__}.")
        else:
            # Check if all elements in the list are strings
            for i, item in enumerate(output_json[field]):
                if not isinstance(item, str):
                    errors.append(f"Element at index {i} in list '{field}' must be a string, but found {type(item).__name__}.")
                    # Stop checking this list after the first error
                    break 

    is_valid = len(errors) == 0
    return is_valid, errors


def extract_text_from_trending_now_json(json_data):
    texts = []
    if not isinstance(json_data, dict): return ""
    texts.append(json_data.get("topic", ""))
    texts.append(json_data.get("category", ""))
    texts.append(json_data.get("subcategory", ""))
    texts.append(json_data.get("description", ""))
    if isinstance(json_data.get("why_is_it_trending"), list): texts.extend(json_data.get("why_is_it_trending"))
    if isinstance(json_data.get("key_points"), list): texts.extend(json_data.get("key_points"))
    if isinstance(json_data.get("overlook_what_might_happen_next"), list): texts.extend(json_data.get("overlook_what_might_happen_next"))
    return "\n".join(filter(None, texts)).strip()
