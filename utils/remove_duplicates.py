def remove_duplicate_lines(file_path):
    seen = set()
    unique_lines = []

    # Read and collect unique lines
    with open(file_path, 'r', encoding='utf-8') as infile:
        for line in infile:
            if line not in seen:
                seen.add(line)
                unique_lines.append(line)

    # Write the unique lines back to the file
    with open(file_path, 'w', encoding='utf-8') as outfile:
        outfile.writelines(unique_lines)

if __name__ == "__main__":
    file_path = 'data/2025-04-03.csv'
    remove_duplicate_lines(file_path)
    print(f"Duplicate lines removed. {file_path}")
