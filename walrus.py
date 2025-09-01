import course
import re

if match := re.match(r"^(\d+)-(\d+)$", "12-34"): # error
    # Use match
    print(match.group(1), match.group(2))
