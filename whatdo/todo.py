# manages master todo list and done list
import json


class TodoItem:
    def __init__(
        self,
        item,
        item_id,
        due_date=None,
        priority=None,
        estimated_time=None,
        tags=None,
        completed=False,
        date_completed=None,
        parent_id=None,
    ):
        self.item = item
        self.due_date = due_date
        self.priority = priority
        self.estimated_time = estimated_time
        self.tags = tags
        self.completed = completed
        self.date_completed = date_completed
        self.item_id = item_id
        self.parent_id = parent_id
        self.sub_items = []

    def add_sub_item(self, sub_item):
        sub_item.parent_id = self.item_id
        self.sub_items.append(sub_item)

    def remove_sub_item(self, sub_item_id):
        self.sub_items = [
            sub_item for sub_item in self.sub_items if sub_item.item_id != sub_item_id
        ]
        for sub in self.sub_items:
            sub.remove_sub_item(sub_item_id)

    def to_dict(self):
        return {
            "item": self.item,
            "item_id": self.item_id,
            "due_date": self.due_date,
            "priority": self.priority,
            "estimated_time": self.estimated_time,
            "tags": self.tags,
            "completed": self.completed,
            "date_completed": self.date_completed,
            "parent_id": self.parent_id,
            "sub_items": [sub_item.to_dict() for sub_item in self.sub_items],
        }

    @classmethod
    def from_dict(cls, data):
        item = cls(
            item=data["item"],  # mandatory field
            item_id=data["item_id"],
            due_date=data.get("due_date"),  # optional field
            priority=data.get("priority"),
            estimated_time=data.get("estimated_time"),
            tags=data.get("tags"),
            completed=data.get("completed", False),
            date_completed=data.get("date_completed"),
            parent_id=data.get("parent_id"),
        )
        item.sub_items = [
            cls.from_dict(sub_item) for sub_item in data.get("sub_items", [])
        ]
        return item

    def __repr__(self):
        return f"{self.item} (Completed: {self.completed})"


def load_todos(filename="todos.json"):
    try:
        with open(filename, "r") as f:
            todos = json.load(f)
    except FileNotFoundError:
        todos = []
    return [TodoItem.from_dict(todo) for todo in todos]


def save_todos(todos, filename="todos.json"):
    with open(filename, "w") as f:
        json.dump([todo.to_dict() for todo in todos], f, indent=4)


def remove_completed_items(todo_list):
    def is_completed(item):
        if item.completed and all(
            is_completed(sub_item) for sub_item in item.sub_items
        ):
            return True
        return False

    def filter_items(items):
        return [item for item in items if not is_completed(item)]

    def grab_completed_items(items):
        return [item for item in items if is_completed(item)]

    return filter_items(todo_list), grab_completed_items(todo_list)


def save_to_completed(items, filename="completed.json"):
    with open(filename, "w") as f:
        json.dump([todo.to_dict() for todo in items], f, indent=4)
