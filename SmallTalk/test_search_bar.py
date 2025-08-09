#!/usr/bin/env python3

import os
import sys
import django

# Add the project root to the path
sys.path.append('/home/badsha/code_hydra/ihsan5987_django')

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from SmallTalk.search_bar import search_bar

def test_search_bar_consistency():
    print("Testing search_bar function consistency...")
    
    # Test with a distinct topic
    print("\n1. Testing with distinct topic 'Python programming':")
    try:
        result = search_bar("Python programming", allow_options=True)
        print(f"Result type: {type(result)}")
        if isinstance(result, tuple) and len(result) == 2:
            print(f"Success flag: {result[0]}")
            json_output = result[1]
            print(f"JSON output type: {type(json_output)}")
            if isinstance(json_output, dict):
                print("JSON keys:", list(json_output.keys()))
                # Check if it's in search options format
                if any(key.startswith('search') for key in json_output.keys()):
                    print("✓ Correctly formatted as search options")
                else:
                    print("✗ Not formatted as search options")
            else:
                print("JSON output is not a dictionary")
        else:
            print("Result is not a tuple with 2 elements")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test with allow_options=False
    print("\n2. Testing with allow_options=False:")
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
                else:
                    print("✗ Not formatted as detailed structure")
            else:
                print("JSON output is not a dictionary")
        else:
            print("Result is not a tuple with 2 elements")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_search_bar_consistency()