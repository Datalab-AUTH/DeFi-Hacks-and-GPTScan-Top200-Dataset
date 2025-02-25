import os
import random
import re
import json
from pathlib import Path

data_dir: str = "/Users/elenimandana/Projects/Thesis/MSc-thesis/data/contracts/GPTScan-Top200-dev"
contract_pattern = re.compile(r'contract\s+([a-zA-Z0-9_]+)')
function_pattern = re.compile(
    r'(function\s+[a-zA-Z0-9_]+\s*\(.*?\)[^}]*})', re.DOTALL)

print("Extracting functions, comments, and contract names from Solidity files...")
solidity_files = Path(data_dir).rglob("*.sol")

functions = []
for sol_file in solidity_files:
    with open(sol_file, 'r', encoding='utf-8') as file:
        content = file.read()

        # Extract contract names
        contract_matches = contract_pattern.findall(content)
        contract_name = Path(sol_file).stem

        # Extract functions
        function_matches = function_pattern.findall(content)
        for function_code in function_matches:

            function_name = re.search(
                r'function\s+([a-zA-Z0-9_]+)', function_code).group(1)
            functions.append({
                "contract": contract_name,
                "function": function_name,
                "code": function_code,
            })

output_file = "top200_safe_functions.json"
with open(output_file, 'w') as out:
    json.dump(functions, out, indent=4)

print(f"Extraction complete! Functions saved to {output_file}")

with open(output_file, 'r') as file:
    data = json.load(file)

# Sample 331 unique entries with seed
sample_size = 331
random.seed(69)

weights = [len(entry['code'])**2.6 for entry in data]
if len(data) >= sample_size:
    sampled_data = random.choices(data, weights=weights, k=sample_size)
    sample_output_file = "top200_sampled_functions.json"
    with open(sample_output_file, 'w') as out:
        json.dump(sampled_data, out, indent=4)
    print(
        f"Sampled {sample_size} unique functions saved to {sample_output_file}")
else:
    print(f"Dataset contains fewer than {sample_size} entries. Cannot sample.")
