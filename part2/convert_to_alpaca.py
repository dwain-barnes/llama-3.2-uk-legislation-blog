import json
import re

def convert_to_alpaca_format(input_file, output_file, debug=False):
    alpaca_data = []
    skipped = []

    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except UnicodeDecodeError as e:
        raise Exception("Error reading the file. Ensure it's encoded in UTF-8.") from e

    current_instruction = ""
    current_output = ""

    for line in lines:
        line = line.strip()

        # Skip markers like "### 761."
        if re.match(r"^###\s*\d+\.", line):
            continue

        # Detect a question line (starts or contains "Q:")
        if "Q:" in line:
            # Save the previous Q&A if it exists
            if current_instruction and current_output:
                alpaca_data.append({
                    "instruction": current_instruction.strip(),
                    "input": "",
                    "output": current_output.strip()
                })
                current_instruction = ""
                current_output = ""

            # Extract the question after "Q:"
            current_instruction = line.split("Q:", 1)[1].strip()
        
        # Detect an answer line (starts with "A:")
        elif line.startswith("A:"):
            # Start a new answer
            current_output = line[2:].strip()
        elif current_output:
            # Append continuation lines to the current output
            current_output += " " + line.strip()
        else:
            # If the line doesn't fit the Q&A structure, log it for debugging
            if debug:
                skipped.append(line)

    # Append the last Q&A
    if current_instruction and current_output:
        alpaca_data.append({
            "instruction": current_instruction.strip(),
            "input": "",
            "output": current_output.strip()
        })

    # Save the output
    try:
        with open(output_file, 'w', encoding='utf-8') as out_file:
            json.dump(alpaca_data, out_file, indent=2, ensure_ascii=False)
    except Exception as e:
        raise Exception("Error writing to output file.") from e

    if debug:
        with open("skipped_lines.txt", 'w', encoding='utf-8') as debug_file:
            debug_file.write("\n".join(skipped))

    print(f"Conversion complete. Processed {len(alpaca_data)} Q&A pairs.")
    if debug:
        print(f"{len(skipped)} lines were skipped. Check 'skipped_lines.txt' for details.")

# Example usage
convert_to_alpaca_format('combined.txt', 'alpaca_formatted.json', debug=True)
