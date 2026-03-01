# Modules
from datetime import datetime
from db import TaskDB
from entity import Task
from state_machine import StateMachine
from exceptions import TaskNotFoundError, StateTransitionError, FilterNotFoundError
from logger import setup_logger

# Task Manager
class TaskManager:
    """
    Application layer that orchestrates all task operations.

    Acts as the bridge between the CLI and the database. All business rules
    (state transitions, validation, guards) are enforced here before any
    data is read or written.
    """

    def __init__(self) -> None:
        """Task Manager Constructor"""
        self.taskdb = TaskDB()
        self.sm = StateMachine()
        self.logger = setup_logger()

    def view_all(self) -> list[list]:
        """
        Retrieve all tasks as numbered rows for display.

        Prepends a 1-based display number to each task row so the CLI
        can show a user-friendly list. This display number is used as
        the identifier for all other commands (update, delete, advance).

        Returns:
            list[list]: Each item is [display_number, task_id, title,
                        created_at, completed_at, note, state].

        Raises:
            TaskNotFoundError: If no tasks exist in the database.
        """
        tasks = self.taskdb.get_all_tasks()

        if not tasks:
            msg = f"Tasks viewed, no task found"
            self.logger.warning(msg)
            raise TaskNotFoundError("No task found")

        numbered_tasks = [[idx + 1] + t.to_list() for idx, t in enumerate(tasks)]

        msg = f"Tasks viewed"
        self.logger.info(msg)

        return numbered_tasks

    def add_task(self, title: str, note: str ="") -> None:
        """
        Create a new task and persist it to the database.

        The task is initialized with state TODO and created_at set to now.
        completed_at is left empty until the task is advanced to DONE.

        Args:
            title (str): The task title. Cannot be empty or blank.
            note (str): Optional note or context for the task. Defaults to "".

        Raises:
            FieldEmptyError: If title is empty or whitespace (raised inside Task).
        """
        task_obj = Task(title, note=note)
        msg = f"Task added with title '{title}' and note '{note}'"
        self.logger.info(msg)

        self.taskdb.create_task(task_obj)

    def get_task_by_display_id(self, display_id: int) -> Task:
        """
        Fetch a single task by its display number from the current list.

        Display IDs are positional (1-based) and reflect the current order
        of tasks in the database. They are not stable across deletions —
        deleting task 2 shifts all subsequent display IDs down by one.

        Args:
            display_id (int): The 1-based position of the task in the list.

        Returns:
            Task: The matching Task object.

        Raises:
            TaskNotFoundError: If display_id is out of range.
        """
        tasks = self.taskdb.get_all_tasks()

        if not (1 <= display_id <= len(tasks)):
            msg = f"Display ID '{display_id}' not found"
            self.logger.warning(msg)
            raise TaskNotFoundError(f"Display ID '{display_id}' not found")

        task = tasks[display_id - 1]

        msg = f"Task with display ID '{display_id}' and title '{task.title}'"
        self.logger.info(msg)

        return task

    def get_task_by_filter(self, filter: str, value: str) -> list[Task]:
        """
        Search for tasks matching a given field and value.

        Delegates to the database layer after validating the filter name.
        Returns all tasks that match, not just the first one.

        Args:
            filter (str): The field to filter by. Must be one of:
                          'TITLE', 'CREATED_ON', 'COMPLETED_ON'.
            value (str): The value to match against.
                         Dates must be in DD-MM-YYYY format.

        Returns:
            list[Task]: All tasks matching the filter. Empty list if none found.

        Raises:
            FilterNotFoundError: If the filter name is not one of the allowed values.
        """
        FILTER = ["TITLE", "CREATED_ON", "COMPLETED_ON"]

        if filter not in FILTER:
            msg = f"Filter '{filter}' not found"
            self.logger.warning(msg)
            raise FilterNotFoundError(
                "Only 'TITLE', 'CREATED_ON', 'COMPLETED_ON' filters allowed"
            )
        tasks = self.taskdb.fetch_task(filter, value)

        msg = f"Tasks called with filter '{filter}' and value '{value}'"
        self.logger.info(msg)
        return tasks

    def delete_task(self, display_id: int) -> None:
        """
        Delete a task permanently by its display number.

        Looks up the task first to confirm it exists, then removes it
        from the database by its internal task_id.

        Args:
            display_id (int): The 1-based position of the task in the list.

        Raises:
            TaskNotFoundError: If no task exists at the given display_id.
        """
        task = self.get_task_by_display_id(display_id)

        if not task:
            msg = f"Task not found"
            self.logger.warning(msg)
            raise TaskNotFoundError("Task not found")

        msg = f"Task with display ID '{display_id}' deleted"
        self.logger.info(msg)

        self.taskdb.delete_task(task.task_id)

    def update_task(self, display_id: int, title: str=None, note: str=None, state: str=None) -> None:
        """
        Update one or more fields of an existing task.

        Handles both metadata updates (title, note) and state transitions.
        State transitions are validated against the state machine before
        being applied. Setting state to DONE automatically fills completed_at.

        All modifications are blocked if the task is already in DONE state.

        Args:
            display_id (int): The 1-based position of the task in the list.
            title (str | None): New title to set. Skipped if None.
            note (str | None): New note to set. Skipped if None.
            state (str | None): Target state to transition to. Skipped if None.
                                Must be a valid transition from the current state.

        Raises:
            TaskNotFoundError: If no task exists at the given display_id.
            StateTransitionError: If the task is already DONE, or if the
                                  requested state transition is not allowed.
        """
        task = self.get_task_by_display_id(display_id)

        if not task:
            msg = f"Task not found"
            self.logger.warning(msg)
            raise TaskNotFoundError("Task not found")

        if task.state == "DONE":
            msg = f"Tried to modify 'DONE' task, '{task.title}'"
            self.logger.error(msg)
            raise StateTransitionError("Cannot modify 'DONE' task")

        if state is not None:
            if not self.sm.can_transition(task.state, state):
                msg = f"Invalid Transition, from '{task.state}' to '{state}'"
                self.logger.error(msg)
                raise StateTransitionError(
                    f"Invalid Transition, from {task.state} to {state}"
                )

            task.state = state
            if task.state == "DONE":
                task.completed_at = datetime.now()

        if title is not None:
            task.title = title
        if note is not None:
            task.note = note

        msg = f"Task modified"
        self.logger.info(msg)

        self.taskdb.update_task(task)


if __name__ == "__main__":
    pass