import re

# Check if the title is relevant. True if relevant, false if not                
def relevant_title(title, bad_words):
    edited = str(title).lower()

    for word in bad_words:
        match = re.match(word, edited)
        if match:
            return False
    return True

# Remove characters that can cause problems with the sql-query
def clean_string(s):
    # Pattern to match harmful characters
    pattern = r'[\'\"]'

    s = re.sub(pattern, '', s)

    return s
