from openai import OpenAI
import time
from math import ceil

# Initialize the OpenAI client
client = OpenAI(api_key="YOUR OPENAI API KEY HERE")

def generate_qa_batch(batch_number, batch_size):
    # Define the legal areas to cover
    legal_areas = [
        "Constitutional and Administrative Law - covering topics like parliamentary sovereignty, judicial review, and human rights",
        "Criminal Law - including elements of crimes, defenses, and criminal procedure",
        "Contract Law - focusing on formation, terms, breach, and remedies",
        "Tort Law - covering negligence, nuisance, and other civil wrongs",
        "Employment Law - including contracts, discrimination, and workplace rights",
        "Company Law - covering corporate structure, director duties, and shareholder rights",
        "Family Law - including marriage, divorce, child custody, and domestic violence",
        "Intellectual Property Law - covering patents, trademarks, copyright, and design rights"
    ]
    
    # Calculate which legal areas to focus on for this batch
    areas_per_batch = min(batch_size, len(legal_areas))
    selected_areas = legal_areas[(batch_number * areas_per_batch) % len(legal_areas):] + legal_areas[:(batch_number * areas_per_batch) % len(legal_areas)]
    selected_areas = selected_areas[:areas_per_batch]
    
    area_prompt = "\n".join(f"- {area}" for area in selected_areas)
    
    prompt = f"""
    Generate {batch_size} unique question-and-answer pairs about UK legislation, focusing on the following areas of law:
    
    {area_prompt}
    
    Each answer must be detailed and at least two paragraphs long, including:
    - Specific references to relevant legislation and statutes
    - Important case law and precedents
    - Recent amendments or changes
    - Practical implications and real-world applications
    - Common misconceptions or areas of complexity
    
    Number each Q&A pair explicitly as {batch_number * batch_size + 1} through {batch_number * batch_size + batch_size}.
    
    Format each pair like this example:
    
    {batch_number * batch_size + 1}. Q: What are the key elements and defenses in UK criminal law regarding self-defense?
    A: Self-defense in UK criminal law is governed primarily by the Common Law and clarified through Section 76 of the Criminal Justice and Immigration Act 2008. The law establishes that a person may use such force as is reasonable in the circumstances for self-defense, defense of another, defense of property, or prevention of crime. The test for reasonableness is both subjective and objective: the defendant must have honestly believed force was necessary (subjective test) and the force used must be proportionate to the threat as the defendant perceived it (objective test).

    Key case law, including R v Williams (1987) and R v Owino (1996), has established that the defendant's actions must be judged based on the circumstances as they honestly believed them to be at the time, even if their belief was mistaken. However, as demonstrated in R v Clegg (1995), the force used must still be proportionate to the perceived threat. Recent developments, including the Crime and Courts Act 2013, have provided additional protection for householders, allowing them to use disproportionate (but not grossly disproportionate) force when defending themselves against intruders in their homes.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a legal expert specializing in UK legislation. Provide detailed, comprehensive answers that include specific references to legislation, case law, practical implications, and relevant examples. Each answer must be at least two paragraphs long."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=3000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error in batch {batch_number + 1}: {str(e)}")
        return None

def generate_qa_pairs():
    try:
        total_pairs = int(input("Enter the total number of Q&A pairs to generate: "))
        batch_size = 5
        num_batches = ceil(total_pairs / batch_size)
        
        print(f"\nGenerating {total_pairs} Q&A pairs in {num_batches} batches...")
        
        all_qa_pairs = []
        successful_pairs = 0
        
        for batch_num in range(num_batches):
            remaining_pairs = min(batch_size, total_pairs - (batch_num * batch_size))
            
            print(f"\nProcessing batch {batch_num + 1}/{num_batches} (generating {remaining_pairs} pairs)...")
            
            batch_content = generate_qa_batch(batch_num, remaining_pairs)
            
            if batch_content:
                all_qa_pairs.append(batch_content)
                successful_pairs += remaining_pairs
                print(f"Batch {batch_num + 1} completed successfully")
            else:
                print(f"Batch {batch_num + 1} failed")
            
            if batch_num < num_batches - 1:
                print("Waiting 5 seconds before next batch...")
                time.sleep(5)
        
        output_file_path = 'uk_legal_qa_pairs.txt'
        with open(output_file_path, 'w', encoding='utf-8') as file:
            output_content = '\n\n'.join(all_qa_pairs)
            file.write(output_content)
            
        print(f"\nGeneration complete!")
        print(f"Successfully generated {successful_pairs} Q&A pairs")
        print(f"Output written to {output_file_path}")
        
        print("\nFirst 500 characters of output:")
        print(output_content[:500] + "...")
                
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        import traceback
        print("\nFull error traceback:")
        print(traceback.format_exc())

if __name__ == "__main__":
    generate_qa_pairs()
