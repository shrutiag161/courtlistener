import logging

# Reads a file as a string
# Returns "" if empty
def read_file_as_string(file_name):
    with open(file_name) as file:
            content = file.read().strip()
    return content

# Reads a file as a list
# Returns [] if empty
# If ignore_blank_lines is True, blank lines will not be included
# If ignore_blank_lines is False, blank lines will be included
def read_file_as_list(file_name, ignore_blank_lines):
    with open(file_name) as file:
        if ignore_blank_lines:
            content = [line.strip() for line in file if line.strip()] # line.strip() returns true if the line is not empty/not only whitespace
        else:
            content = [line.strip() for line in file]
        return content
     