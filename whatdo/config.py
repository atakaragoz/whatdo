# reads config file
import json


def read_config():
    with open("config.json", "r") as f:
        return json.load(f)


config = read_config()

obsidian_vault_path = config.get("obsidian_vault_path")
obsidian_vault_name = config.get("obsidian_vault_name")
daily_notes_path = config.get("daily_notes_path")
todo_file_path = config.get("todo_file_path")
completed_file_path = config.get("completed_file_path")
hours_per_day = config.get("hours_per_day")
work_weekends = config.get("work_weekends")
