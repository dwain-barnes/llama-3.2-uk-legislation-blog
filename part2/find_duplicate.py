import json

def remove_duplicates(alpaca_file, cleaned_file):
    try:
        with open(alpaca_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except Exception as e:
        raise Exception("Error reading the file. Ensure it's a valid JSON.") from e

    seen_questions = set()
    seen_answers = set()
    cleaned_data = []

    for entry in data:
        question = entry.get("instruction", "").strip()
        answer = entry.get("output", "").strip()

        # Check if the question or answer is a duplicate
        if question in seen_questions or answer in seen_answers:
            continue

        # If unique, add to the cleaned data and track seen questions and answers
        cleaned_data.append(entry)
        seen_questions.add(question)
        seen_answers.add(answer)

    # Save the cleaned data to a new file
    try:
        with open(cleaned_file, 'w', encoding='utf-8') as file:
            json.dump(cleaned_data, file, indent=2, ensure_ascii=False)
    except Exception as e:
        raise Exception("Error writing to the cleaned file.") from e

    print(f"Duplicates removed. Cleaned data saved to {cleaned_file}.")
    print(f"Original entries: {len(data)}. Cleaned entries: {len(cleaned_data)}.")

# Example usage
remove_duplicates(' test.json', 'alpaca_cleaned_test.json')
