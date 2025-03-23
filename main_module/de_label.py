import os

# Set this to your labels directory (where all .txt files are)
LABELS_DIR = "../datasets/Grape Disease Dataset.v2 cleaned/"

# The class index for 'leaf' in your original dataset
ORIGINAL_LEAF_CLASS_ID = "3"
NEW_CLASS_ID = "0"

for root, _, files in os.walk(LABELS_DIR):
    for filename in files:
        if filename.endswith(".txt"):
            filepath = os.path.join(root, filename)
            with open(filepath, "r") as file:
                lines = file.readlines()

            new_lines = []
            for line in lines:
                line = line.strip()
                if not line:
                    continue  # skip empty lines

                parts = line.split()
                if len(parts) != 5:
                    print(f"Skipping malformed line in {filename}: {line}")
                    continue

                if parts[0] == ORIGINAL_LEAF_CLASS_ID:
                    parts[0] = NEW_CLASS_ID
                    new_lines.append(" ".join(parts) + "\n")

            with open(filepath, "w") as file:
                file.writelines(new_lines)