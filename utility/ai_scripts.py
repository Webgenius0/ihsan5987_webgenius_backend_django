from gnews import GNews
import openai  # Make sure to install openai (pip install openai)
import json
from openai import OpenAI
import re
from googlesearch import search
from newspaper import Article
from decouple import config

# --- Configuration (replace with your actual API keys) ---
NEWS_API_KEY = config('NEWS_API_KEY', default='Your-News-API-Key')
OPENAI_API_KEY = config('OPENAI_API_KEY', default='Your-OpenAI-API-Key')
openai.api_key = OPENAI_API_KEY


def get_news(keywords, num_articles=3):
    google_news = GNews()
    articles = google_news.get_news(keywords)[:num_articles]
    news_str = ""
    if articles is not None:
        for article in articles:
            title = article.get("title", "No Title")
            description = article.get("description", "No Description")
            # published_date = article.get("published date", "No Description")
            # url = article.get("url", "No Description")
            # publisher = article.get("description", "No Description")

            news_str += f"- {title}: {description}\n"
        return articles
    else:
        print('no articles found')


def build_prompt_search_bar(keywords, news, second=False):
    """
      Build the LLM prompt that contains:
        - The instructions/format for the response.
        - A placeholder (the fetched news articles) to be summarized.
    """
    
    prompt = (f'''
        You are the assistant that will help quickly get information on a certain topic to support small talk.
        You will receive:
            1) A set of keywords related to a topic.
            2) Potential news items or descriptions that might or might not match the topic.
              
        Assume the reader knows little about the topic, but needs to be able to keep a high-level conversation.
              
        1. Analyze the user's input keywords and any provided news text.
        2. Determine whether the topic is **singular** (one clear meaning) or **ambiguous** (multiple possible interpretations or 'collisions').


        You will receive raw news descriptions that you must summarize.
        Finally, to keep the user engaged, provide additional keywords that they can use to request more information if desired.
        You must retun the response in the JSON format 
                

        Output Rules
          - If the topic is **distinct** (only one clear meaning):
          - Return the full, detailed JSON object in the **original structure** (with 'further_key_words', 'category', 'topic', 'general_facts', 'news', 'interesting_trivia', 'opinions', 'questions', etc.).

          **
          IMPORTANT: original structure:
                
          {{
              "further_key_words": 3 - 5 key words of the topic and your response,
              
              "category": {{
                              "categorie_name": what is the category of the response
              }},
                
              "subcatetgory": {{
                              "subcatetgory_name": what is the subcategory of the response
              }},
                
              "topic": {{
                              "name": name of the topic,
                              "topic_tags": {{
                                      "tag_names": 3-5 tags of the topic and the response
                      }}
              }},
                
              "general_facts": {{
                              "general_definition": introductory sentence about the topic,
                              "general_points": 3 general key points about the topic that the user must know,
                                                  key points must be provided as separate sentances,
                              "general_fun_fact": one general fun fact about the topic,
                              "key_facts_text": 3 key facts about the topic, they must be written as separate sentances,
                              "key_facts_fun_fact": one fun fact about the key points,
                              "picture_url": url of the picture about this topic
              }},
        
              "news": {{
                      "news_text": 3 bullet points with the news, you will get the news and need to summarise them,
                                  you must provide 3 sentances, the news must be connected to the egeneral information you
                                  provided before, if the news ar ecompletly from the another field, indicate that
                      "news_fun_facts": fun fact about the news,
                      "picture_url": url of the picture about this topic
              }},
                
              "interesting_trivia": {{
                      "trivia_text": 3 interesting anecdotes or stories or memes, they must be provided as separate sentances,
                      "trivia_fun_fact": funcfacts about the trivia,
                      "picture_url":url of the picture about this topic
              }},
                
              "opinions": {{
                      "opinions_text": opinions of the other people about this topic,
                      "opinions_fun_fact": fun cfact about the opinions

              }},
                
              "questions": {{
                      "questions_text": questions about the topic that can be discussed on the forum,
                      "questions_fun_fact": func fact about the questions, or fun question that can be discussed
              }}
          }}
          **
          
      
          Examples:
          Input: All-Star game
          Output:
          {{
              "further_key_words": "NBA, All-Star, Basketball, Entertainment",
              
              "category": {{
                      "categorie_name": "Sports"
              }},
        
              "subcatetgory": {{
                      "subcatetgory_name": "NBA Events"
              }},
        
              "topic": {{
                      "name": "NBA All-Star Game",
                      "topic_tags": {{
                              "tag_names": "Basketball, NBA, All-Star"
                      }}
              }},
                
              "general_facts": {{
                      "general_definition": "The NBA All-Star Game is an annual basketball showcase featuring top players from the Eastern and Western Conference.",
                      "general_points": "Multi-Event Format: All-Star Game, Slam Dunk Contest, Three-Point Shootout, Rising Stars.
                                          Big Show: Blends sports, celebrity culture, music acts.
                                          Money Maker: Generates massive revenue from tickets, TV deals, sponsorships.",
                      "general_fun_fact": "Originally a gamble in 1951, its surprising attendance helped make the All-Star Game a yearly NBA highlight.",
                      "key_facts_text": "First Game (1951): Grew into a major U.S. sports event.
                                          Draft Format (since 2018): Top fan-voted players pick their teams.
                                          LeBron’s Record: Could reach 20 All-Star appearances by 2025.",
                      "key_facts_fun_fact": Four Boston Celtics played in the inaugural 1951 game—fans loved it, setting the stage for this annual tradition.",
                      "picture_url": "https://cdn.warriors.com/events_migration/1005x600__14_-2025-nba-all-star-game-20250216.jpg"
              }},
              
              "news": {{
                      "news_text": "2025 Venue: Chase Center, San Francisco.
                                    Rule Tweak: Fourth-quarter scoring adjustments for more excitement.
                                    New Faces: Wembanyama, Banchero, Scoot Henderson may debut.",
                      "news_fun_facts": "The 2020 “Elam Ending” sparked debates on further innovations to keep the All-Star Game thrilling.",
                      "picture_url": "https://cdn.warriors.com/events_migration/1005x600__14_-2025-nba-all-star-game-20250216.jpg"
              }},
                
              "interesting_trivia": {{
                      "trivia_text": "Kobe at 19: Faced Michael Jordan in his first All-Star appearance (1998).
                                      Wilt’s 42: Highest single-game All-Star scoring record (1962).
                                      Target Score: In 2020, time was irrelevant in the final quarter.",
                      "trivia_fun_fact": "In 1997, legends of multiple eras shared the court for the NBA’s 50th anniversary—a rare convergence of past and present.",
                      "picture_url": "https://cdn.warriors.com/events_migration/1005x600__14_-2025-nba-all-star-game-20250216.jpg"
              }},
              "opinions": {{
                      "opinions_text": "Dunk Contests can be more exciting than the actual game—some moves are jaw-dropping.
                                          I’m eager to see if LeBron still dominates in 2025 or if new stars take the spotlight.",
                      "opinions_fun_fact": "In 1997, legends of multiple eras shared the court for the NBA's 50th anniversary-a rare convergence of past and present."
              }},
              "questions": {{
                      "questions_text": "How do you feel about the All-Star team-drafting format?
                                          Which All-Star Game was your favorite?
                                          Will Steph Curry return in 2025 despite aging?",
                      "questions_fun_fact": "Many recall Vince Carter's 2000 Dunk Contest heroics, which revolutionised aerial creativity. One performance can define an entire AlI-Star generation."
              }}
          }}
          
          Example:
          Input: Da Vinci
          Output:      
          {{
              "further_key_words": "Leonardo, Renaissance, Innovation, Robotics, Art",
              "category": {{
                "categorie_name": "Art & Technology"
              }},
              "subcatetgory": {{
                "subcatetgory_name": "Renaissance Legacy & Modern Innovation"
              }},
              "topic": {{
                "name": "da vinci",
                "topic_tags": {{
                  "tag_names": "Leonardo da Vinci, Renaissance, Innovation, Art, Technology"
                }}
              }},
              "general_facts": {{
                "general_definition": "Da Vinci commonly refers to Leonardo da Vinci, the iconic Renaissance polymath known for his art, scientific discoveries, and innovative ideas.",
                "general_points": "He revolutionized art with masterpieces like the Mona Lisa and The Last Supper. His inventive sketches and scientific observations laid the groundwork for modern engineering and anatomy. His multidisciplinary genius continues to inspire innovation in diverse fields today.",
                "general_fun_fact": "Leonardo often wrote his notes in mirror script, a quirky habit that adds to his mystique.",
                "key_facts_text": "Leonardo's artwork remains some of the most studied and celebrated in history. His conceptual designs predicted inventions like flying machines and armored vehicles. The da Vinci legacy has extended into modern products and institutions bearing his name.",
                "key_facts_fun_fact": "A surprising number of modern technological products, from surgical robots to video editing software, use his name as a mark of innovation.",
                "picture_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Leonardo_da_Vinci_-_presumed_self-portrait_-_WGA12798.jpg/800px-Leonardo_da_Vinci_-_presumed_self-portrait_-_WGA12798.jpg"
              }},
              "news": {{
                "news_text": "A free beginner's guide to Da Vinci Resolve 19 has been released by Blackmagic, emphasizing its status as a leading free video editing software inspired by creative innovation. Intuitive Surgical has issued a Class II recall for its da Vinci 5 foot pedal, causing concerns over product safety and potential impacts on stock performance. In art and heritage news, exhibits inspired by 'The Last Supper' and the upcoming Leonardo da Vinci Museum in North America underline the enduring influence of his legacy.",
                "news_fun_facts": "These news items demonstrate how Leonardo da Vinci's name bridges the gap between historical art and cutting-edge technology.",
                "picture_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/Da_Vinci_robotic_surgery.jpg/800px-Da_Vinci_robotic_surgery.jpg"
              }},
              "interesting_trivia": {{
                "trivia_text": "Leonardo's detailed notebooks reveal sketches of inventions centuries ahead of their time. He was not only a master artist but also a scientist, inventor, and engineer. Modern pop culture frequently references his enigmatic art and visionary ideas in films and literature.",
                "trivia_fun_fact": "A recurring theme in trivia is Leonardo's ability to blend art and science, making him a timeless figure of innovation.",
                "picture_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Leonardo_da_Vinci_-_Codex_Leicester.jpg/800px-Leonardo_da_Vinci_-_Codex_Leicester.jpg"
              }},
              "opinions": {{
                "opinions_text": "Many admire da Vinci as a symbol of genius whose work transcends time, while others critique the modern commercialization of his name in unrelated industries.",
                "opinions_fun_fact": "Some enthusiasts joke that every new 'da Vinci' product is a modern-day homage to his genius, regardless of the field."
              }},
              "questions": {{
                "questions_text": "What do you think makes Leonardo da Vinci's work so enduring? How do modern innovations reflect his visionary ideas? Should more institutions celebrate his legacy in diverse fields?",
                "questions_fun_fact": "A fun discussion point is whether the modern use of his name truly honors his legacy or dilutes it over time."
              }}
          }}
                
          - If the topic is **not distinct** (multiple subtopics or collisions):
            - Return **only** a single JSON object with keys "search1", "search2", "search3", etc.
            - Return from 3 to 5 possible searches. 
            - Each search block must contain the fields: 
              - "key_words"
              - "category"
              - "subcatetgory"
            - Example when multiple subtopics are found:
              {{
                "search1": {{
                  "key_words": "Leonardo da Vinci Painter",
                  "category": "Art & History",
                  "subcatetgory": "Renaissance Legacy"
                }},
                "search2": {{
                  "key_words": "DaVinci Resolve Software",
                  "category": "Technology & Media",
                  "subcatetgory": "Video Editing Tools"
                }},
                "search3": {{
                  "key_words": "da Vinci Surgical System",
                  "category": "Medical Technology",
                  "subcatetgory": "Robotic Surgery"
                }}
              }}

                  Critical Requirements
                  - Always respond in **valid JSON** only (no extra commentary, no markdown).
                  - For **singular** topics  return the **detailed** JSON (your original schema).
                  - For **ambiguous** topics  return the **simplified** JSON (the "searchN" keys format).
                  - If it is the second time generating  is True, output only **detailed** JSON (your original schema), if second time generating  is False, you can decide what output to make.
                  - Do not include any other text or explanation outside the JSON.


              Second time generating: {second}
              Here is the key words input: {keywords}.
              Here are the news: {news}

          ''')
    return prompt


def get_llm_response(prompt, OPENAI_API_KEY='Open-AI-API'):
    """
    Call the LLM (using OpenAI's API in this example) to generate a response.
    """
    client = OpenAI(api_key=OPENAI_API_KEY)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or another model if desired
            messages=[
                # {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            # max_completion_tokens = 5000
        )
        llm_output = response.choices[0].message.content.strip()
        return llm_output
    except Exception as e:
        print("Error during LLM call:", e)
        return ""


def verify_and_fix_json(input_str):
    """Attempt to parse `input_str` as JSON. If it fails,
    apply a series of fixes, then re-parse. Return (parse_ok, final_json).
      parse_ok: bool - True if valid JSON was obtained (original or fixed).
      final_json: dict or list or None - The parsed JSON object, or None if fixes failed.
    """

    # Helper: Remove markdown code block markers (``` or ```json)
    def remove_markdown_code_block(s):
        lines = s.splitlines()
        # Remove starting ``` or ```json
        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]
        # Remove ending ```
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        return "\n".join(lines)

    # Helper: Remove literal newlines inside JSON string literals by replacing them with a space.
    # This function preserves double quotes around the string.
    def remove_newlines_in_strings(s):
        pattern = r'"((?:\\.|[^"\\])*)"'  # Regex to match string contents (handles escaped quotes too)

        def replacer(match):
            inner = match.group(1)
            # Replace literal newline characters with a space
            new_inner = inner.replace('\n', ' ')
            return '"' + new_inner + '"'

        return re.sub(pattern, replacer, s, flags=re.DOTALL)

    # STEP 1: Preprocess: remove markdown code fences & newlines in string literals
    preprocessed = remove_markdown_code_block(input_str)
    preprocessed = remove_newlines_in_strings(preprocessed)

    # Attempt to parse the preprocessed JSON
    try:
        parsed = json.loads(preprocessed)
        # If parsing works, return immediately
        return True, parsed
    except json.JSONDecodeError:
        # We'll attempt to fix the JSON below
        pass

    # STEP 2: Try to fix the JSON with heuristics
    try:
        fixed_string = preprocessed

        # 2a. Remove lingering triple backticks (edge case)
        fixed_string = re.sub(r'^```[a-zA-Z]*\s*', '', fixed_string)
        fixed_string = re.sub(r'\s*```$', '', fixed_string)

        # 2b. Fix missing commas between lines that appear to have valid JSON pairs
        lines = fixed_string.splitlines()
        for i in range(len(lines) - 1):
            current_line = lines[i].rstrip()
            next_line = lines[i + 1].lstrip()

            # If current line ends with a literal or true/false/null
            if (current_line.endswith('"') or re.search(r'[0-9]$', current_line) or current_line.endswith('true') or current_line.endswith('false') or current_line.endswith('null')):
                # And next line starts like a key or unquoted text that might be a key
                if (next_line.startswith('"') or re.match(r'^[a-zA-Z_]', next_line)):
                    # If there's no trailing comma, add it
                    if not current_line.endswith(','):
                        lines[i] = current_line + ','

        fixed_string = "\n".join(lines)

        # 2c. Add missing quotes around keys: from { key: "value" } to { "key": "value" }
        fixed_string = re.sub(r'([{,]\s*)([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'\1"\2":', fixed_string)

        # 2d. Remove trailing commas before closing braces/brackets
        fixed_string = re.sub(r',\s*([}\]])', r'\1', fixed_string)

        # 2e. Fix missing quotes around string values (somewhat simplistic)
        # e.g. : key -> : "key"
        fixed_string = re.sub(r':\s*([a-zA-Z0-9_][^{}\[\]"\',:}\]]*[a-zA-Z0-9_])', r': "\1"', fixed_string)

        # 2f. Replace undefined or NaN with null
        fixed_string = re.sub(r':\s*undefined', r': null', fixed_string)
        fixed_string = re.sub(r':\s*NaN', r': null', fixed_string)

        # 2g. Remove newlines inside string literals again
        fixed_string = remove_newlines_in_strings(fixed_string)

        # 2h. Balance braces/brackets if needed
        open_braces = fixed_string.count('{')
        close_braces = fixed_string.count('}')
        open_brackets = fixed_string.count('[')
        close_brackets = fixed_string.count(']')

        if open_braces > close_braces:
            fixed_string += '}' * (open_braces - close_braces)
        if open_brackets > close_brackets:
            fixed_string += ']' * (open_brackets - close_brackets)

        # Final attempt to parse
        parsed_fixed = json.loads(fixed_string)
        return True, parsed_fixed

    except Exception:
        # If we still fail, return parse_ok=False with no JSON
        return False, None


def validate_json_structure_search_bar(json_data):
    """
    Validate that `json_data` conforms to one of two possible schemas:

    1) Distinct Topic Schema (original detailed structure):
       {
         "further_key_words": str,
         "category": {
           "categorie_name": str
         },
         "subcatetgory": {
           "subcatetgory_name": str
         },
         "topic": {
           "name": str,
           "topic_tags": {
             "tag_names": str
           }
         },
         "general_facts": {
           "general_definition": str,
           "general_points": str,
           "general_fun_fact": str,
           "key_facts_text": str,
           "key_facts_fun_fact": str,
           "picture_url": str
         },
         "news": {
           "news_text": str,
           "news_fun_facts": str,
           "picture_url": str
         },
         "interesting_trivia": {
           "trivia_text": str,
           "trivia_fun_fact": str,
           "picture_url": str
         },
         "opinions": {
           "opinions_text": str,
           "opinions_fun_fact": str
         },
         "questions": {
           "questions_text": str,
           "questions_fun_fact": str
         }
       }

    2) Ambiguous/Collision Schema (multiple "searchN" sub-objects):
       {
         "search1": {
           "key_words": str,
           "category": str,
           "subcatetgory": str
         },
         "search2": {
           "key_words": str,
           "category": str,
           "subcatetgory": str
         },
         ...
       }

    Return: (is_valid, error_messages)
      - is_valid: bool
      - error_messages: a list of strings describing any validation errors.
    """

    errors = []

    # --- HELPER FUNCTIONS ---

    def has_distinct_topic_keys(obj):
        """Check if obj has all top-level keys for the distinct topic schema."""
        required_top_keys = {
            "further_key_words",
            "category",
            "subcatetgory",
            "topic",
            "general_facts",
            "news",
            "interesting_trivia",
            "opinions",
            "questions"
        }
        return required_top_keys.issubset(obj.keys())

    def validate_distinct_topic(obj):
        """Validate the detailed structure if it's a single, distinct topic.
           Return True if valid, otherwise False, and append errors to `errors`.
        """
        if not has_distinct_topic_keys(obj):
            missing = {
                "further_key_words",
                "category",
                "subcatetgory",
                "topic",
                "general_facts",
                "news",
                "interesting_trivia",
                "opinions",
                "questions"
            } - set(obj.keys())
            errors.append(f"Missing required top-level fields for distinct schema: {missing}")
            return False

        # Check data types / sub-objects:

        # category
        if not isinstance(obj["category"], dict):
            errors.append("`category` should be an object.")
            return False
        if "categorie_name" not in obj["category"]:
            errors.append("`category` is missing 'categorie_name' field.")
            return False

        # subcatetgory
        if not isinstance(obj["subcatetgory"], dict):
            errors.append("`subcatetgory` should be an object.")
            return False
        if "subcatetgory_name" not in obj["subcatetgory"]:
            errors.append("`subcatetgory` is missing 'subcatetgory_name' field.")
            return False

        # topic
        if not isinstance(obj["topic"], dict):
            errors.append("`topic` should be an object.")
            return False
        if "name" not in obj["topic"] or "topic_tags" not in obj["topic"]:
            errors.append("`topic` is missing 'name' or 'topic_tags'.")
            return False
        if not isinstance(obj["topic"]["topic_tags"], dict):
            errors.append("`topic.topic_tags` should be an object.")
            return False
        if "tag_names" not in obj["topic"]["topic_tags"]:
            errors.append("`topic.topic_tags` is missing 'tag_names'.")
            return False

        # general_facts
        gf = obj["general_facts"]
        if not isinstance(gf, dict):
            errors.append("`general_facts` should be an object.")
            return False
        gf_required = {"general_definition", "general_points", "general_fun_fact",
                       "key_facts_text", "key_facts_fun_fact", "picture_url"}
        missing_gf = gf_required - set(gf.keys())
        if missing_gf:
            errors.append(f"`general_facts` is missing fields: {missing_gf}")
            return False

        # news
        news_obj = obj["news"]
        if not isinstance(news_obj, dict):
            errors.append("`news` should be an object.")
            return False
        news_required = {"news_text", "news_fun_facts", "picture_url"}
        missing_news = news_required - set(news_obj.keys())
        if missing_news:
            errors.append(f"`news` is missing fields: {missing_news}")
            return False

        # interesting_trivia
        it = obj["interesting_trivia"]
        if not isinstance(it, dict):
            errors.append("`interesting_trivia` should be an object.")
            return False
        it_required = {"trivia_text", "trivia_fun_fact", "picture_url"}
        missing_it = it_required - set(it.keys())
        if missing_it:
            errors.append(f"`interesting_trivia` is missing fields: {missing_it}")
            return False

        # opinions
        opin = obj["opinions"]
        if not isinstance(opin, dict):
            errors.append("`opinions` should be an object.")
            return False
        opin_required = {"opinions_text", "opinions_fun_fact"}
        missing_opin = opin_required - set(opin.keys())
        if missing_opin:
            errors.append(f"`opinions` is missing fields: {missing_opin}")
            return False

        # questions
        quest = obj["questions"]
        if not isinstance(quest, dict):
            errors.append("`questions` should be an object.")
            return False
        quest_required = {"questions_text", "questions_fun_fact"}
        missing_quest = quest_required - set(quest.keys())
        if missing_quest:
            errors.append(f"`questions` is missing fields: {missing_quest}")
            return False

        # If all checks passed:
        return True

    def looks_like_ambiguous_schema(obj):
        """
        Check if the top-level keys look like 'search1', 'search2', ...
        Return True if at least one top-level key matches 'search' pattern,
        and no required top-level fields from the distinct schema are present.
        """
        top_keys = set(obj.keys())

        distinct_keys = {
            "further_key_words", "category", "subcatetgory",
            "topic", "general_facts", "news", "interesting_trivia",
            "opinions", "questions"
        }
        # If there's intersection with distinct schema keys, it's not purely ambiguous
        if distinct_keys.intersection(top_keys):
            return False

        # If no key matches 'search\d*' => not ambiguous
        if not any(re.match(r'^search\d*$', k) for k in top_keys):
            return False

        return True

    def validate_ambiguous_schema(obj):
        """
        Validate the ambiguous/collision schema:
        {
          "search1": {"key_words": ..., "category": ..., "subcatetgory": ...},
          "search2": {...}, ...
        }
        Return True if valid, otherwise False, appending errors as needed.
        """
        for key, val in obj.items():
            # Key must match "search\d*"
            if not re.match(r'^search\d*$', key):
                errors.append(f"Unexpected key at top level: '{key}' (expected 'searchN').")
                return False

            if not isinstance(val, dict):
                errors.append(f"'{key}' must map to an object.")
                return False

            required_subfields = {"key_words", "category", "subcatetgory"}
            diff = required_subfields - set(val.keys())
            if diff:
                errors.append(f"'{key}' is missing required fields: {diff}")
                return False

        return True

    # --- MAIN VALIDATION LOGIC ---

    if not isinstance(json_data, dict):
        errors.append("Top-level JSON must be an object.")
        return False, errors

    # 1) Check if it matches the distinct (single-topic) schema
    if has_distinct_topic_keys(json_data):
        is_valid = validate_distinct_topic(json_data)
        return (is_valid, errors if not is_valid else [])

    # 2) Check if it looks like ambiguous/collision schema
    if looks_like_ambiguous_schema(json_data):
        is_valid = validate_ambiguous_schema(json_data)
        return (is_valid, errors if not is_valid else [])

    # 3) If neither schema passes
    errors.append("JSON does not match single-topic or ambiguous schema.")
    return False, errors


def search_bar(input, OPENAI_API_KEY, second=False,):
    """
    Retrieves news based on the given `input` keyword(s), constructs a prompt
    for the LLM, requests a JSON response, and verifies the JSON structure.

    Workflow Steps:
        1. Fetch news:
           - Calls `get_news(input, 3)` to retrieve three relevant news items
             related to the user's `input`.
        2. Build prompt:
           - Uses `build_prompt(input, news_text, second=second)` to create
             a context-rich prompt that includes the keywords and summarized
             news. The `second` parameter can be used to alter the prompt logic
             or style if needed.
        3. Get LLM response and fix JSON (up to 3 attempts):
           - Calls `get_llm_response(prompt)` to invoke a language model.
           - Then uses `verify_and_fix_json(llm_response)` to attempt parsing
             the string as valid JSON, applying heuristic fixes if needed.
           - Validates the fixed JSON structure with `validate_json_structure`.
           - Retries up to 3 times if the JSON is invalid.
        4. Return results or error:
           - If validation succeeds within 3 attempts, returns a tuple:
             (parse_ok, final_json), where:
               - `parse_ok` is a boolean indicating whether the original output
                 was valid or required fixes.
               - `final_json` is the parsed-and-verified JSON structure.
           - If validation is not successful after 3 tries, returns
             "The Error is not fixed".

    Args:
        input (str):
            The topic or keywords to pass into the prompt and fetch news for.
        second (bool, optional):
            A control flag that can alter how `build_prompt` structures the prompt.
            Defaults to False.
        OPENAI_API_KEY (str, optional):
            API key used for the LLM service. Defaults to a placeholder key.

    Returns:
        tuple or str:
            - If valid JSON is produced and passes schema checks:
                (need_choise, json_output)
                where `need_choise` (bool) indicates whether the JSON was initially valid
                or had to be fixed, and `json_output` is the resulting parsed JSON dict.
            - If the JSON could not be validated in 3 attempts: 
                "The Error is not fixed"


    """
    news_text = get_news(input, 3)

    # Build the prompt using the keywords and fetched news.
    prompt = build_prompt_search_bar(input, news_text, second=second)

    validated = False
    iterations = 0

    while not validated and iterations != 3:
        # Get the response from the LLM.
        llm_response = get_llm_response(prompt, OPENAI_API_KEY=OPENAI_API_KEY)
        need_choise, json_output = verify_and_fix_json(llm_response)

        validated = validate_json_structure_search_bar(json_output)[0]
        iterations += 1

    if validated:
        return need_choise, json_output
    else:
        return "The Error is not fixed"


def build_prompt_recommendations(keywords, articles):
    """
    Build the LLM prompt that contains:
      - The instructions/format for the response.
      - A placeholder (the fetched news articles) to be summarized.
    """
  
    prompt = f"""
    You are an assistant that summarizes trending topics into structured, readable briefings.

    You will receive:
    - A **topic** to focus on.
    - A **set of related articles** (titles, summaries, or links).

    Your job is to create an engaging, high-quality overview in a clean JSON format that includes:
    1. Headline
    2. Category
    3. A brief introduction
    4. A section with key tips or takeaways (use multiple labeled sections with bullet points inside)
    5. A section titled **Fun Facts / Did You Know?**, there interesting or fun facts about the topic must be provided. Example could be the meme or anecdote. 
    6. A clear and useful conclusion

    Your response must:
    - Be concise but rich in insights.
    - Use **reliable content from the provided articles** wherever possible.
    - Be written clearly and helpfully, assuming the reader wants to sound informed in casual conversation or benefit personally.
    - Follow the **exact JSON format shown below**. Do not add markdown or any explanation.

    ---
    IMPORTANT: Output format (use this template exactly):

    {{
      "topic": "Remote Work",
      "headline": "Top Tips for Achieving a Work-Life Balance in the Home Office",
      "category": "Career",

      "introduction": "Many people assume working from home automatically boosts work-life balance. However, blurred boundaries between work and personal life can cause stress. These quick tips help keep you motivated and prevent burnout.",

      "key_tips_and_takeaways": {{
        "Fixed Schedules & Breaks": [
          "Follow regular office hours.",
          "Take a proper lunch break (30–60 min every 4 hours).",
          "Leave your desk for breaks to clear your mind."
        ],
        "Set Boundaries": [
          "Avoid checking emails after hours.",
          "Stay offline for personal time unless there’s an emergency."
        ],
        "Time Management": [
          "Tackle difficult tasks first to stay motivated.",
          "Maintain an updated to-do list, divided into smaller milestones.",
          "Schedule 'focus times' with minimal interruptions."
        ],
        "Limit Distractions": [
          "Household chores can wait.",
          "Use apps to block gaming/messaging during work hours.",
          "Stay connected virtually to avoid isolation."
        ],
        "Separate Work & Personal Space": [
          "If possible, have a dedicated workspace.",
          "Clear away work items at day’s end for a mental reset."
        ],
        "Exercise & Relaxation": [
          "Go for short walks before/after work.",
          "Try yoga or meditation for posture and stress relief.",
          "‘Sign off’ by tidying up your desk at day’s end."
        ],
        "Don’t Work When Ill": [
          "Listen to your body; rest is essential to recover.",
          "Working sick can worsen symptoms and harm long-term health."
        ]
      }},

      "fun_facts": [
        "Wearing comfortable yet distinct 'work clothes' can help you mentally transition between work and personal time.",
        "Discuss any changes to your schedule with colleagues to align on availability."
      ],

      "conclusion": "A healthy work-life balance hinges on structure and boundaries. By setting clear work hours, creating a distraction-free environment, and making time for breaks and exercise, you’ll stay motivated and stress-free in your home office."
    }}

    ---
    Now generate a JSON block like the one above for the topic: **{keywords}**

    ### Related Articles:
    {articles}

    Use the article content to enhance your tips, facts, and examples. Only return a valid JSON object with no extra output.
    """
    return prompt


def get_urls_from_google(keywords, region="us", num_results=15, lang="en"):
    results = list(search(keywords, advanced=True, region=region, num_results=num_results, lang=lang))
    return results


def extract_main_text_from_url(url: str) -> str:
    """
    Extracts the main article text from a given URL using newspaper3k.
    
    Args:
        url (str): The URL of the web page to extract content from.
    
    Returns:
        str: The main text content of the page, or an empty string if failed.
    """
    if not url or not url.startswith("http"):
        return ""
    
    try:
        article = Article(url, language='en')
        article.download()
        article.parse()
        
        # Clean up the text: remove multiple newlines
        text_content = re.sub(r'\n+', '\n', article.text).strip()
        return text_content
    
    except Exception as e:
        print(f"Failed to extract content from {url}: {e}")
        return ""


def get_articles(urls, max_articles=5):
    articles = []
    for url in urls:
        try:
            art = extract_main_text_from_url(url.url)
            articles.append(art)
        except Exception:
            print('Invalid URL')
        if len(articles) >= max_articles:
            break
        
    return articles


def recommendations(keywords, region="us", num_results=15, lang="en", OPENAI_API_KEY='Open-AI-API'):   
    urls = get_urls_from_google(keywords, region=region, num_results=num_results, lang=lang)
    articles = get_articles(urls)
    print(len(" ".join(articles)))
    articles = " ".join(articles)[0:21000]
    prompt = build_prompt_recommendations(keywords, articles)
    response = get_llm_response(prompt, OPENAI_API_KEY=OPENAI_API_KEY)
    valid, fixed_json = verify_and_fix_json(response)
    if valid:
        return fixed_json
    else:
        print("The Error is not fixed")


def build_prompt_update_me(keywords, article_text, reference_url=None):
    prompt = (f'''
          
    You are the assistant that will help quickly get information on a certain topic for update briefings.
    You will receive:
        1) A set of keywords related to a topic.
        2) A summary of related news or article text.
          
    Assume the reader needs a concise briefing that can be used in small talk or for quick updates.
          
    1. Analyze the provided keywords and article text.
    2. Determine whether the topic is singular (one clear meaning) or ambiguous (multiple possible subtopics or collisions).

    You will produce a structured update briefing in JSON format.
    Include a reference URL, a background story, and a related picture URL.
    You must return the response in the JSON format exactly as specified.
          
    Output Rules:
    - If the topic is distinct (only one clear meaning):
      Return the full, detailed JSON object with the following structure:
      
      {{
        "category": "<Category, e.g., Global News, Personal Interest, Global Development>",
        "subcategory": "<Subcategory, e.g., NFL, Politics, Tech>",
        "topic": "<Short title of the update>",
        "short_info": [
            "<Bullet point 1: main summary (max 1 sentence)>",
            "<Bullet point 2: supporting detail (max 1 sentence)>",
            "<Bullet point 3: additional development (max 1 sentence)>"
        ],
        "reference_url": "<URL for more information>",
        "background_story": {{
            "context_history": "<Brief context or history (1-2 sentences)>",
            "current_developments": "<Current developments (1-2 sentences)>",
            "relevance": "<Why it matters (1-2 sentences)>"
        }},
        "picture_url": "<URL of a related picture>"
      }}
      

    Critical Requirements:
    - Always respond in valid JSON only (no extra commentary, no markdown).
    - For singular topics, return the detailed JSON object as shown.
    - For ambiguous topics, return the simplified JSON (with the "searchN" keys).
    - If it is the second time generating (second=True), output only the detailed JSON.
    - Do not include any additional text or explanation outside the JSON.

    Below are example JSON outputs for guidance:

    Example:
    {{
      "category": "Global News",
      "subcategory": "Middle East",      
      "topic": "Erdoğan: “No power can expel Palestinians from their homeland”",
      "short_info": [
          "In a recent speech, the Turkish president reaffirmed his support for the Palestinian people and criticized recent developments in the Middle East.",
          "International observers view this statement as another step in strengthening Erdoğan’s role as a regional actor.",
          "At the same time, diplomats urge caution to prevent further tensions in the region."
      ],
      "reference_url": "[More info → Background story]",
      "background_story": {{
          "context_history": "For years, Turkey has played an active role in Middle Eastern politics, repeatedly advocating for the recognition of Palestinian interests.",
          "current_developments": "Recent tensions in the region have reinforced Erdoğan’s political stance as he attempts to position himself as a mediator and protector.",
          "relevance": "This stance could reshape the dynamic between Israel, Palestine, and neighboring states, potentially affecting the broader diplomatic balance in the Middle East."
      }},
      "picture_url": "https://example.com/path-to-erdoogan-news.jpg"
    }}


    Here is the key words input: {keywords}.
    Here are the news: {article_text}
    Reference URL: {reference_url if reference_url else "N/A"}
    ''')
    return prompt


def generate_update_element(keywords, OPENAI_API_KEY, reference_url=None):
    """
    Generates a structured update element in JSON format using OpenAI's API and the tailored prompt.
    """
    article_text = get_news(keywords, 3)
    prompt = build_prompt_update_me(keywords, article_text, reference_url)
    raw_response = get_llm_response(prompt, OPENAI_API_KEY)
    valid, parsed_json = verify_and_fix_json(raw_response)
    if valid:
        return parsed_json
    else:
        print("Could not parse/fix the JSON response.")
        return None


def build_prompt_trending(keywords, article_text, extra_links=None):
    prompt = (f'''
    You are the assistant that will help quickly get exhaustive information on a certain trending topic for update briefings.
    You will receive:
        1) A set of keywords related to a trending topic.
        2) A summary of related news or update detail text.
          
    Your task is to generate an engaging and concise update briefing in JSON format.
    The JSON must include the following elements:
    
    - topic: A short title for the update.
    - category: The main category (e.g., Global News, Sports, Entertainment).
    - subcategory: The subcategory (e.g., NFL, Politics, Tech).
    - description: A brief description of the trending topic.
    - why_is_it_trending: An array with at least 3 bullet points explaining why the topic is trending.
    - key_points: An array with at least 3 bullet points highlighting key facts or details.
    - overlook_what_might_happen_next: An array with at least 3 bullet points with predictions or outlook.
    - links_and_sources: An array containing links and sources.
    
    The JSON must follow this exact structure (no extra commentary, no markdown):
    
    {{
      "topic": "<Short title or topic>",
      "category": "<Category, e.g., Global News, Sports, Entertainment>",
      "subcategory": "<Subcategory, e.g., NFL, Politics, Tech>",
      "description": "<A brief description of the trending topic>",
      "why_is_it_trending": [
          "<Bullet point 1: Explanation of why it's trending>",
          "<Bullet point 2: Explanation of why it's trending>",
          "<Bullet point 3: Explanation of why it's trending>"
      ],
      "key_points": [
          "<Bullet point 1: Key detail>",
          "<Bullet point 2: Key detail>",
          "<Bullet point 3: Key detail>"
      ],
      "overlook_what_might_happen_next": [
          "<Bullet point 1: Outlook or prediction>",
          "<Bullet point 2: Outlook or prediction>",
          "<Bullet point 3: Outlook or prediction>"
      ]
    }}
    
    Critical Requirements:
    - The arrays "why_is_it_trending", "key_points", and "overlook_what_might_happen_next" must contain at least 3 bullet points each.
    - Always respond in valid JSON only (no extra commentary, no markdown).
    
    Below is an example JSON output for guidance:
    
    Example:
    {{
      "topic": "Super Bowl 2025",
      "category": "Sports",
      "subcategory": "NFL",
      "description": "Super Bowl 2025 is the most anticipated event of the year, drawing millions of viewers worldwide.",
      "why_is_it_trending": [
          "The game is just days away, and preparations are in full swing.",
          "High-profile teams are expected to deliver a thrilling performance.",
          "The halftime show lineup, headlined by Kendrick Lamar, is generating buzz."
      ],
      "key_points": [
          "Teams: Philadelphia Eagles vs. Kansas City Chiefs.",
          "Halftime Show: Star performances with potential surprise guests.",
          "Betting Odds: Significant shifts in favor of an underdog."
      ],
      "overlook_what_might_happen_next": [
          "Game Prediction: Analysts lean towards a close contest.",
          "Halftime Surprises: There may be unexpected guest performances.",
          "Viewership: Could set new records in streaming numbers."
      ]
    }}
    
    Here is the key words input: {keywords}.
    Here is the article text: {article_text}.
    {f"Extra links: {extra_links}" if extra_links else ""}
    ''')
    return prompt


def generate_trending_now_element(keywords, OPENAI_API_KEY='Open-AI-API', extra_links=None):
    article_text = get_news(keywords, 3)
    prompt = build_prompt_trending(keywords, article_text, extra_links)
    raw_response = get_llm_response(prompt, OPENAI_API_KEY)
    valid, parsed_json = verify_and_fix_json(raw_response)
    if valid:
        return parsed_json
    else:
        print("Could not parse/fix the JSON response.")
        return None






