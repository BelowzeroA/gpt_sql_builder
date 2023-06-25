
def save_list_to_file(lines, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for line in lines:
            print(str(line).strip(), file=file)


def load_list_from_file(filename, encoding='utf-8', lower_case=False, skip_empty=False):
    lines = []
    with open(filename, 'r', encoding=encoding) as file:
        for line in file:
            line = line.strip()
            if lower_case:
                line = line.lower()
            if line or not skip_empty:
                lines.append(line)
    return lines

