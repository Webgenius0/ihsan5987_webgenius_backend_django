#!/usr/bin/env python3

import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from SmallTalk.search_bar import search_bar

def test_search_bar_function():
    print("Testing search_bar function...")
    
    # Test with a simple topic
    print("\n1. Testing with topic 'Python programming':")
    try:
        result = search_bar("Python programming", allow_options=False)
        print(f"Result type: {type(result)}")
        if isinstance(result, tuple) and len(result) == 2:
            print(f"Success flag: {result[0]}")
            json_output = result[1]
            print(f"JSON output type: {type(json_output)}")
            if isinstance(json_output, dict):
                print("JSON keys:", list(json_output.keys()))
                # Check if it's in detailed format
                expected_keys = {"further_key_words", "category", "subcatetgory", "topic", 
                               "general_facts", "news", "interesting_trivia", "opinions", "questions"}
                if expected_keys.issubset(set(json_output.keys())):
                    print("✓ Correctly formatted as detailed structure")
                    # Check key_facts_text and trivia_text data types
                    if "general_facts" in json_output and isinstance(json_output["general_facts"], dict):
                        key_facts_text = json_output["general_facts"].get("key_facts_text", "")
                        print(f"key_facts_text type: {type(key_facts_text)}")
                        print(f"key_facts_text value: {key_facts_text}")
                    
                    if "interesting_trivia" in json_output and isinstance(json_output["interesting_trivia"], dict):
                        trivia_text = json_output["interesting_trivia"].get("trivia_text", "")
                        print(f"trivia_text type: {type(trivia_text)}")
                        print(f"trivia_text value: {trivia_text}")
                else:
                    print("✗ Not formatted as detailed structure")
            else:
                print("JSON output is not a dictionary")
        else:
            print("Result is not a tuple with 2 elements")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_search_bar_function()