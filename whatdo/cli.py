import click
import datetime
from rich.console import Console
from rich.tree import Tree
from .todo import (
    TodoItem,
    load_todos,
    save_todos,
    remove_completed_items,
    save_to_completed,
)
from .config import (
    obsidian_vault_path,
    obsidian_vault_name,
    daily_notes_path,
    todo_file_path,
    completed_file_path,
    hours_per_day,
    work_weekends,
)

from .utils import generate_id

# initialize rich console
console = Console()


@click.group()
def cli():
    """A simple CLI for managing your daily todos."""
    pass


@click.command()
@click.argument("item")
@click.option("--due_date", default=None, help="The due date for the todo item.")
@click.option("--priority", default=None, help="The priority level for the todo item.")
@click.option(
    "--estimated_time",
    default=None,
    help="The estimated time required for the todo item.",
)
@click.option(
    "--tags",
    default=None,
    help="The tags associated with the todo item. expected as a comma separated string",
)
@click.option("--parent_id", default=None, help="The ID of the parent todo item.")
def add(item, due_date, priority, estimated_time, tags, parent_id=None):
    """Add a new todo item."""
    todos = load_todos(todo_file_path)
    tags_list = [tag.strip() for tag in tags.split(",")] if tags else None
    new_item = TodoItem(
        item, generate_id(), due_date, priority, estimated_time, tags=tags_list
    )
    if parent_id is not None:
        for todo_item in todos:
            if todo_item.item_id == parent_id:
                todo_item.add_sub_item(new_item)
                save_todos(todos, todo_file_path)
                click.echo(f"Added sub-item: {item} to parent with ID: {parent_id}")
                return
            for sub_item in todo_item.sub_items:
                if sub_item.item_id == parent_id:
                    sub_item.add_sub_item(new_item)
                    save_todos(todos, todo_file_path)
                    click.echo(
                        f"Added sub-item: {item} to parent sub-item with ID: {parent_id}"
                    )
                    return
        click.echo(f"Parent ID: {parent_id} not found")
    else:
        todos.append(
            new_item,
        )
        save_todos(todos, todo_file_path)
        click.echo(f"Added todo item: {item}")


@click.command()
@click.argument("item_id")
def remove(item_id):
    """Remove a todo item by its ID, including sub-items."""
    todos = load_todos(todo_file_path)
    todos = [todo for todo in todos if todo.item_id != item_id]
    for item in todos:
        item.remove_sub_item(item_id)
    save_todos(todos, todo_file_path)
    click.echo(f"Removed todo item with ID: {item_id}")


@click.command()
def update():
    """Update the status of the todo-list, moving completed items to a separate file."""
    todos = load_todos(todo_file_path)
    todos, completed_items = remove_completed_items(todos)
    save_to_completed(completed_items, completed_file_path)
    save_todos(todos, todo_file_path)
    click.echo("Updated todo list")


@click.command()
def list_items():
    """List all todo items."""
    todo_list = load_todos(todo_file_path)
    if not todo_list:
        console.print("No todo items found.", style="bold red")
        return

    tree = Tree("Todo List", guide_style="bold cyan")
    for item in todo_list:
        add_to_tree(tree, item)

    console.print(tree)


def add_to_tree(tree, item, level=0):
    item_info = (
        f"[bold green]Item:[/bold green] {item.item}\n"
        f"[bold blue]ID:[/bold blue] {item.item_id}\n"
        f"[bold cyan]Due Date:[/bold cyan] {item.due_date}\n"
        f"[bold magenta]Priority:[/bold magenta] {item.priority}\n"
        f"[bold cyan]Estimated Time:[/bold cyan] {item.estimated_time}\n"
        f"[bold cyan]Tags:[/bold cyan] {item.tags}\n"
        f"[bold cyan]Completed:[/bold cyan] {item.completed}\n"
        f"[bold cyan]Date Completed:[/bold cyan] {item.date_completed}"
    )
    branch = tree.add(item_info, guide_style="bold bright_black")

    for sub_item in item.sub_items:
        add_to_tree(branch, sub_item, level + 1)


def mark_item_complete(item, id):
    if item.item_id == id:
        item.completed = True
        item.date_completed = datetime.datetime.now().isoformat()
        return True
    for sub_item in item.sub_items:
        if mark_item_complete(sub_item, id):
            sub_item.parent_id = item.item_id
            return True
    return False


@click.command()
@click.argument("id")
def complete(id):
    """Mark a todo item as complete by ID."""
    todo_list = load_todos()
    for item in todo_list:
        if mark_item_complete(item, id):
            save_todos(todo_list, todo_file_path)
            click.echo(f"Marked todo item with ID: {id} as complete")
            return
    click.echo(f"Todo item with ID: {id} not found")


cli.add_command(add)
cli.add_command(remove)
cli.add_command(update)
cli.add_command(list_items)
cli.add_command(complete)

if __name__ == "__main__":
    cli()
