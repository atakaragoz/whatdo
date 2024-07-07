# utility functions for handling id generation, markdown parsing, etc.

import uuid
import os
import re
import datetime
from .todo import TodoItem
from .config import work_weekends


def generate_id():
    return str(uuid.uuid4())


def generate_date_time_name():
    """Generates the date time string for the daily note file name. YYYY-MM-DD.md"""
    return datetime.datetime.now().strftime("%Y-%m-%d")


def check_exists_or_create(path):
    if not os.path.exists(path):
        os.makedirs(path)


def check_weekend():
    return datetime.datetime.today().weekday() in [5, 6]


def parse_markdown_to_todo_list(markdown):
    lines = markdown.split("\n")
    todo_list = []
    stack = []

    for line in lines:
        match = re.match(r"(\s*)- \[( |x)\] (.+)", line)
        if match:
            indent = len(match.group(1))
            completed = match.group(2) == "x"
            item_text = match.group(3)
            item_id = generate_id()
            item = TodoItem(item_text, item_id)
            item.completed = completed

            while stack and stack[-1][0] >= indent:
                stack.pop()

            if stack:
                stack[-1][1].add_sub_item(item)
            else:
                todo_list.append(item)

            stack.append((indent, item))

    return todo_list
