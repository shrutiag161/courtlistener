import logging

# Reads a file as a string
# Returns "" if empty and allow_empty_file = True
# Raises Exception if file doesn't exist
def read_file_as_string(file_name: str, *, allow_empty_file: bool):
    with open(file_name) as file:
            content = file.read().strip()
    if not allow_empty_file and not content:
        raise Exception(f"{file_name} is empty")
    return content

# Reads a file as a list
# Returns [] if empty and allow_empty_file = True
# Raises Exception if file doesn't exist
def read_file_as_list(file_name: str, *, ignore_blank_lines: bool, allow_empty_file: bool):
    with open(file_name) as file:
        if ignore_blank_lines:
            content = [line.strip() for line in file if line.strip()] # line.strip() returns true if the line is not empty/not only whitespace
        else:
            content = [line.strip() for line in file]
        if not allow_empty_file and not content:
             raise Exception(f"{file_name} is empty")
        return content
     