import argparse
import sys
from engine import TaskManager

tm = TaskManager()


def cmd_add(args):
    tm.add_task(args.title, note=args.note or "")
    print(f"Task '{args.title}' added.")


def cmd_list(args):
    tasks = tm.view_all()
    if not tasks:
        print("No tasks found.")
        return
    print(f"\n{'#':<5} {'TITLE':<25} {'STATE':<15} {'CREATED':<22} {'NOTE'}")
    print("-" * 85)
    for t in tasks:
        num, task_id, title, created, completed, note, state = t
        print(f"{num:<5} {title:<25} {state:<15} {created:<22} {note}")
    print()


def cmd_update(args):
    tm.update_task(args.id, title=args.title, note=args.note)
    print(f"Task {args.id} updated.")


def cmd_advance(args):
    tm.update_task(args.id, state=args.state.upper())
    print(f"Task {args.id} advanced to {args.state.upper()}.")


def cmd_delete(args):
    tm.delete_task(args.id)
    print(f"Task {args.id} deleted.")


def cmd_filter(args):
    tasks = tm.get_task_by_filter(args.by.upper(), args.value)
    if not tasks:
        print("No matching tasks found.")
        return
    print(f"\n{'TITLE':<25} {'STATE':<15} {'CREATED':<22} {'NOTE'}")
    print("-" * 75)
    for t in tasks:
        print(
            f"{t.title:<25} {t.state:<15} {t.created_at.strftime('%d-%m-%Y %H:%M:%S'):<22} {t.note}"
        )
    print()


def main():
    parser = argparse.ArgumentParser(prog="taski", description="Task Manager CLI")
    sub = parser.add_subparsers(dest="command")
    sub.required = True

    # add
    p_add = sub.add_parser("add", help="Add a new task")
    p_add.add_argument("title", help="Task title")
    p_add.add_argument("--note", help="Optional note", default="")
    p_add.set_defaults(func=cmd_add)

    # list
    p_list = sub.add_parser("list", help="List all tasks")
    p_list.set_defaults(func=cmd_list)

    # update
    p_update = sub.add_parser("update", help="Update task title or note")
    p_update.add_argument("id", type=int, help="Task display number")
    p_update.add_argument("--title", help="New title", default=None)
    p_update.add_argument("--note", help="New note", default=None)
    p_update.set_defaults(func=cmd_update)

    # advance
    p_advance = sub.add_parser("advance", help="Advance task state")
    p_advance.add_argument("id", type=int, help="Task display number")
    p_advance.add_argument(
        "state", choices=["in_progress", "done", "cancelled"], help="Target state"
    )
    p_advance.set_defaults(func=cmd_advance)

    # delete
    p_delete = sub.add_parser("delete", help="Delete a task")
    p_delete.add_argument("id", type=int, help="Task display number")
    p_delete.set_defaults(func=cmd_delete)

    # filter
    p_filter = sub.add_parser("filter", help="Filter tasks")
    p_filter.add_argument(
        "by", choices=["title", "created_on", "completed_on"], help="Filter field"
    )
    p_filter.add_argument("value", help="Value to match")
    p_filter.set_defaults(func=cmd_filter)

    args = parser.parse_args()

    try:
        args.func(args)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
