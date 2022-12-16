from flask import render_template, redirect, flash, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

import sqlalchemy
import re
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime
import matplotlib.style as style
import time
import socket
import platform
import os
import subprocess
import psutil

from app import db
from app.bps.api import bp
from app.models import User, UserTag, Recipt, Tag


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address


def get_cpu():
  # Use the "top" command to get a list of the processes using the most CPU
  top_output = subprocess.run(["top", "-b", "-n", "1", "-w", "200"], capture_output=True).stdout.decode()
  lines = top_output.split("\n")
  headings = lines[6]

  # Get the index of the "COMMAND" column
  cmd_index = headings.index("COMMAND")

  # Iterate through the lines, skipping the first (headings) and last (empty) lines
  results = []
  for line in lines[7:7+5]:
    # Get the command field and append it to the results list
    command = line[cmd_index:]
    results.append(command)

  return results


def convert_to_gb(bytes):
    """ Convert to gigabytes and round to two decimals """
    gb = round(bytes / 1024**3, 2)
    return gb


def get_sysinfo():
    sysinf = {}

    # Get the system's uptime
    uptime = psutil.boot_time()
    uptime_seconds = int(time.time()) - uptime
    uptime_hours = round(uptime_seconds / 3600, 2)
    sysinf["uptime"] = f"{uptime_hours}h"

    # Get system ip
    sysinf["ip"] = get_ip_address()

    # Get mysql version
    try:
        sysinf["mysql"] = db.engine.execute("SELECT version()").fetchone()[0]
    except sqlalchemy.exc.OperationalError:
        sysinf["mysql"] = "Not available"

    # Get NGINX version
    try:
        sysinf["nginx"] = subprocess.run(["nginx", "-v"], capture_output=True).stdout.decode().split()[2]
    except FileNotFoundError:
        sysinf["nginx"] = "Not available"

    # Get CPU usage
    cpu_usage = psutil.cpu_percent()
    cpu_top = get_cpu()

    # Get the number of CPU cores
    cpu_count = psutil.cpu_count()

    sysinf["cpu"] = {
            "count": cpu_count,
            "cpu_usage": cpu_usage,
            "top": cpu_top
            }

    # Get the system's hostname
    hostname = socket.gethostname()
    sysinf["hostname"] = hostname

    # Get the operating system name and version
    os_name = platform.system()
    os_release = platform.release()
    sysinf["os"] = f"{os_name} {os_release}"

    # Get memory usage information
    memory_info = psutil.virtual_memory()
    sysinf["memory"] = {
        "total": convert_to_gb(memory_info.total),
        "used": convert_to_gb(memory_info.used),
        "available": convert_to_gb(memory_info.available),
        "percent_used": round(memory_info.used / memory_info.total * 100, 2)
    }

    # Get hard disk usage information
    disk_usage = psutil.disk_usage('/')

    # Calculate the total, used, and free space in GB
    total_space = convert_to_gb(disk_usage.total)
    used_space = convert_to_gb(disk_usage.used)
    free_space = convert_to_gb(disk_usage.free)

    # Calculate the percentage of space being used
    percent_used = round(disk_usage.used / disk_usage.total * 100, 2)

    # Return the results as a dictionary
    sysinf["disk_space"] = {
        "total": total_space,
        "used": used_space,
        "free": free_space,
        "percent_used": percent_used
    }

    return sysinf


def get_entries():
    # Define a regular expression to match the log format
    log_regex = r'^(?P<remote_addr>\S+) - (?P<remote_user>\S+) \[(?P<time_local>.+)\] "(?P<request>.+)" (?P<status>\d+) (?P<body_bytes_sent>\d+) "(?P<http_referer>.*)" "(?P<http_user_agent>.*)"$'

    # Compile the regular expression
    pattern = re.compile(log_regex)

    # Open the log file
    log_entries = []
    with open('tests/access.log', 'r') as log_file:
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
    data = {i+1: 0 for i in range(24)} 

    for i in logs:
        timestamp = i["time_local"] 
        hour = datetime.strptime(timestamp, '%d/%b/%Y:%H:%M:%S %z').hour
        data[hour] += 1

    return data


def get_top(logs):
    # Create a dictionary to store the count of each request
    request_counts = {}
    
    # Iterate through the logs and update the count for each request
    for log in logs:
        request = f"{log['request']} [ {log['status']} ]"
        if request in request_counts:
            request_counts[request] += 1
        else:
            request_counts[request] = 1
    
    # Sort the requests by count in descending order
    sorted_requests = sorted(request_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Return the top 20 requests
    return sorted_requests[:20]


def get_err(logs):
    err_logs = []
    
    # Iterate through the logs and add any entries with a non-200 status code to the list
    for log in logs:
        status = log['status']
        if status != '200':
            err_logs.append(log)
    
    return err_logs


@bp.route('/get_stats')
@login_required
def stats():
    if not current_user.is_admin(): abort(404)

    entries = get_entries()
    traffic = get_traffic(entries)
    top = get_top(entries)
    err = get_err(entries)
    err = get_top(err)
    sysinf = get_sysinfo()

    return jsonify({"traffic": traffic, "top": top, "err": err, "sysinf": sysinf})
