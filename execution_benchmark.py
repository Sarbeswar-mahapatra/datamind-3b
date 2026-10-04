import requests
import json

QUESTIONS = [
    {
        "name": "Reverse Vowels",
        "prompt": 'Write a Python function `def reverse_vowels(s: str) -> str:` that takes a string and reverses only the vowels in it.',
        "tests": [
            'assert reverse_vowels("hello") == "holle"',
            'assert reverse_vowels("leetcode") == "leotcede"',
            'assert reverse_vowels("aA") == "Aa"'
        ]
    },
    {
        "name": "Sum to Zero",
        "prompt": 'Write a Python function `def sum_to_zero(l: list) -> bool:` that takes a list of integers. It returns True if any two distinct elements in the list sum to zero, otherwise False.',
        "tests": [
            'assert sum_to_zero([1, 2, -2, 4]) == True',
            'assert sum_to_zero([1, 2, 3, 4]) == False',
            'assert sum_to_zero([0, 0]) == True'
        ]
    },
    {
        "name": "Largest Prime Factor",
        "prompt": 'Write a Python function `def largest_prime_factor(n: int) -> int:` that returns the largest prime factor of a given number n. Assume n > 1.',
        "tests": [
            'assert largest_prime_factor(15) == 5',
            'assert largest_prime_factor(27) == 3',
            'assert largest_prime_factor(29) == 29'
        ]
    },
    {
        "name": "Remove Duplicates",
        "prompt": 'Write a Python function `def remove_duplicates(numbers: list) -> list:` that removes all elements that occur more than once in the list, keeping only unique elements in their original order.',
        "tests": [
            'assert remove_duplicates([1, 2, 3, 2, 4]) == [1, 3, 4]',
            'assert remove_duplicates([1, 1, 1]) == []',
            'assert remove_duplicates([5, 6, 7]) == [5, 6, 7]'
        ]
    },
    {
        "name": "Sort by Length",
        "prompt": 'Write a Python function `def sort_by_length(strings: list) -> list:` that sorts a list of strings by their length, from shortest to longest.',
        "tests": [
            'assert sort_by_length(["a", "ccc", "bb"]) == ["a", "bb", "ccc"]',
            'assert sort_by_length(["apple", "pie", "is", "good"]) == ["is", "pie", "good", "apple"]'
        ]
    }
]

MODELS = ["qwen2.5-coder:3b", "datamind:latest"]

def get_code(model, prompt):
    url = 'http://localhost:11434/api/generate'
    data = {
        "model": model,
        "prompt": prompt + "\nProvide only the Python code inside ```python and ``` blocks.",
        "stream": False,
        "options": {"temperature": 0.1}
    }
    response = requests.post(url, json=data).json()['response']
    
    # Extract code from markdown blocks
    if "```python" in response:
        code = response.split("```python")[1].split("```")[0].strip()
    elif "```" in response:
        code = response.split("```")[1].split("```")[0].strip()
    else:
        code = response
    return code

print("=== AUTOMATED EXECUTION SANDBOX (Big Tech Pass@1 Test) ===")

results = {m: {"pass": 0, "fail": 0} for m in MODELS}

for q in QUESTIONS:
    print(f"\nTesting: {q['name']}")
    for model in MODELS:
        print(f"  [{model}] Generating code...")
        try:
            code = get_code(model, q['prompt'])
            
            # Combine generated code with hidden unit tests
            test_script = code + "\n\n" + "\n".join(q['tests'])
            
            # Execute the code in a sandbox (exec)
            exec(test_script, {})
            print(f"  [{model}] -> PASS (All Unit Tests Succeeded)")
            results[model]["pass"] += 1
            
        except AssertionError:
            print(f"  [{model}] -> FAIL (Logic Error: Failed a Unit Test)")
            results[model]["fail"] += 1
        except Exception as e:
            print(f"  [{model}] -> FAIL (Syntax/Execution Error: {type(e).__name__})")
            results[model]["fail"] += 1

print("\n=== FINAL PASS@1 SCORECARD ===")
for model in MODELS:
    total = results[model]['pass'] + results[model]['fail']
    score = (results[model]['pass'] / total) * 100
    print(f"{model}: {score}% ({results[model]['pass']}/{total} passed)")
