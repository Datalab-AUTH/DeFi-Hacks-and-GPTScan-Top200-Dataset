import json
import random
import string

random.seed(42)

# Load the dataset
input_file = '/Users/elenimandana/Projects/Thesis/MSc-thesis/data/contracts/top200/top200_sampled_functions.json'
output_file = 'top200_prompts.jsonl'  # Output file

# Load the dataset
with open(input_file, 'r') as file:
    data = json.load(file)

# Define the five prompts
prompts = [
    "Below is an instruction that describes a classification task.\nDevise a label name suitable for categorizing items as either vulnerable or safe.\n### Instruction:\nPlease review the code. Please find out if it is vulnerable.\n### Input:\n```Solidity\n{code}\n```\n### Response:",
    "Below is an instruction that describes a classification task.\nSuggest a label designation that clearly identifies an item's status as either vulnerable or safe.\n### Instruction:\nInspect the following Solidity code. Determine if there are any vulnerabilities present.\n### Input:\n```Solidity\n{code}\n```\n### Response:",
    "Below is an instruction that describes a classification task.\nInvent a naming label that aptly segregates items into vulnerable or safe classifications.\n### Instruction:\nExamine this Solidity script. Identify any potential security risks.\n### Input:\n```Solidity\n{code}\n```\n### Response:",
    "Below is an instruction that describes a classification task.\nFormulate a label descriptor that bifurcates objects into categories of vulnerable and safe.\n### Instruction:\nPlease assess the provided Solidity code for any security vulnerabilities.\n### Input:\n```Solidity\n{code}\n```\n### Response:",
    "Below is an instruction that describes a classification task.\nPropose a label nomenclature that aptly differentiates between vulnerable and safe states.\n### Instruction:\nEvaluate the given Solidity function. Are there any security flaws?\n### Input:\n```Solidity\n{code}\n```\n### Response:"
]

# Prepare the converted dataset
with open(output_file, 'w') as out_file:
    if data:  # Check if data is not empty
        for entry in data:
            if "code" in entry:
                code_snippet = entry["code"].strip()
                label = "safe"
                unique_id = ''.join(random.choices(
                    string.ascii_letters + string.digits, k=5))
                # Generate 5 variations using the prompts
                for prompt in prompts:
                    json.dump({
                        "id": unique_id,  # Use the same ID for all prompts related to this snippet
                        "prompt": prompt.replace("{code}", code_snippet),
                        "completion": f"The label is {label}."
                    }, out_file)
                    out_file.write('\n')
    else:
        print("Input dataset is empty.")

print(f"Converted dataset saved to {output_file}")
