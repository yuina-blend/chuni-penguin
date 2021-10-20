import re
tweet = "aaa16aaa"
for level in re.findall("1[0-5]\+|1[0-5]\.[0-9]|1[0-5]", tweet):
    print(level)
