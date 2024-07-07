# utility functions for handling id generation, markdown parsing, etc.

import uuid
import os
import re
from todo import TodoItem


def generate_id():
    return str(uuid.uuid4())


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
