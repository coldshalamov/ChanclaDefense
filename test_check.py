import re

with open("index.html") as f:
    text = f.read()

# Make sure shop items actually fit on the screen in playmode without overlapping the back button.
# Also double check that they don't break verification due to old tests using removed mechanics (which memory said we can ignore).
