import re
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime
import matplotlib.style as style

style.use('bmh')

def get_entries():
    # Define a regular expression to match the log format
    log_regex = r'^(?P<remote_addr>\S+) - (?P<remote_user>\S+) \[(?P<time_local>.+)\] "(?P<request>.+)" (?P<status>\d+) (?P<body_bytes_sent>\d+) "(?P<http_referer>.*)" "(?P<http_user_agent>.*)"$'

    # Compile the regular expression
    pattern = re.compile(log_regex)

    # Open the log file
    log_entries = []
    with open('access.log', 'r') as log_file:
        # Iterate over each line in the log file
        for line in log_file:
            # Try to match the line against the regular expression
            match = pattern.match(line)
            if match:
                # Extract the named groups from the match
                log_data = match.groupdict()
                log_entries.append(log_data)

    return log_entries


def get_traffic(logs):
    data = defaultdict(int)

    for i in logs:
        timestamp = i["time_local"] 
        hour = datetime.strptime(timestamp, '%d/%b/%Y:%H:%M:%S %z').hour
        data[hour] += 1

    return dict(data)

print(get_traffic(get_entries()))
