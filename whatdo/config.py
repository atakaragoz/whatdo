# reads config file
import json
import os


def read_config():
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_path, "r") as f:
        return json.load(f)


config = read_config()

obsidian_vault_path = config.get("obsidian_vault_path")
obsidian_vault_name = config.get("obsidian_vault_name")
daily_notes_path = config.get("daily_notes_path")
todo_file_path = config.get("todo_file_path")
dailies_file_path = config.get("dailies_file_path")
completed_file_path = config.get("completed_file_path")
hours_per_day = config.get("hours_per_day")
work_weekends = config.get("work_weekends")

daily_notes_path = f"{obsidian_vault_path}/{obsidian_vault_name}/{daily_notes_path}"
