# recommendation.py
import os
import pandas as pd
from .api_utils import generate_perplexity_output
from .llm_utils import build_prompt, verify_and_fix_json


file_name = "Categories.xlsx"
file_path = os.path.join(os.path.dirname(__file__), file_name)


def generate_recommendation(
    keywords,
    prompt_version="v02",
    categories_file=file_path,
    region="us",
    num_results=15,
    lang="en",
    **model_params,
):
    df = pd.read_excel(categories_file)

    # urls = get_urls_from_google(keywords, region = region, num_results=num_results, lang=lang)
    # articles = get_articles(urls)
    # print(len(" ".join(articles)))
    # articles = " ".join(articles)[0:21000]

    prompt = build_prompt(
        prompt_type='recommendation', 
        prompt_version=prompt_version,
        keywords=keywords, 
        news='', 
        article_text='',
        reference_url=''
    )

    user_input = f'    Here is the subcategory: {keywords}.'
    # response = get_llm_response(prompt)
    raw_response = generate_perplexity_output(prompt, user_input)
    valid, parsed_json = verify_and_fix_json(raw_response['choices'][0]['message']['content'])

    category = df[df['Subcategory'] == parsed_json.get('subcategory', '')]['Category'].values[0] if not df[df['Subcategory'] == parsed_json.get('subcategory', '')].empty else 'General'
    parsed_json['category'] = category

    if valid:
        return parsed_json
    else:
        print("The Error is not fixed")


def validate_recommendation_output(output_json):
    """
    Validate that the recommendation JSON conforms to the expected schema.

    Expected Schema:
    {
      "introduction": "string",
      "key_tips_and_takeaways": {
        "category_name": ["string", ...],
        ...
      },
      "fun_facts": ["string", ...],
      "conclusion": "string"
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
    string_fields = ["introduction", "conclusion"]
    for field in string_fields:
        if field not in output_json:
            errors.append(f"Missing required field: '{field}'.")
        elif not isinstance(output_json[field], str):
            errors.append(f"Field '{field}' must be a string, but found {type(output_json[field]).__name__}.")

    # Check for 'key_tips_and_takeaways' field (dictionary of lists of strings)
    if "key_tips_and_takeaways" not in output_json:
        errors.append("Missing required field: 'key_tips_and_takeaways'.")
    elif not isinstance(output_json["key_tips_and_takeaways"], dict):
        errors.append(f"Field 'key_tips_and_takeaways' must be an object, but found {type(output_json['key_tips_and_takeaways']).__name__}.")
    else:
        for category, tips_list in output_json["key_tips_and_takeaways"].items():
            if not isinstance(tips_list, list):
                errors.append(f"Field 'key_tips_and_takeaways.{category}' must be a list, but found {type(tips_list).__name__}.")
            else:
                for i, tip in enumerate(tips_list):
                    if not isinstance(tip, str):
                        errors.append(f"Element at index {i} in list 'key_tips_and_takeaways.{category}' must be a string, but found {type(tip).__name__}.")
                        break  # Stop checking this list after the first error

    # Check for 'fun_facts' field (list of strings)
    if "fun_facts" not in output_json:
        errors.append("Missing required field: 'fun_facts'.")
    elif not isinstance(output_json["fun_facts"], list):
        errors.append(f"Field 'fun_facts' must be a list, but found {type(output_json['fun_facts']).__name__}.")
    else:
        for i, fact in enumerate(output_json["fun_facts"]):
            if not isinstance(fact, str):
                errors.append(f"Element at index {i} in list 'fun_facts' must be a string, but found {type(fact).__name__}.")
                break  # Stop checking this list after the first error

    is_valid = len(errors) == 0
    return is_valid, errors


def extract_text_from_recommendations_json(json_data):
    texts = []
    if not isinstance(json_data, dict):
        return ""
    texts.append(json_data.get("introduction", ""))
    key_tips = json_data.get("key_tips_and_takeaways", {})
    if isinstance(key_tips, dict):
        for _, tips_list in key_tips.items():
            if isinstance(tips_list, list):
                texts.extend(str(tip) for tip in tips_list)
    fun_facts = json_data.get("fun_facts", [])
    if isinstance(fun_facts, list):
        texts.extend(str(fact) for fact in fun_facts)
    texts.append(json_data.get("conclusion", ""))
    return "\n".join(filter(None, texts)).strip()
