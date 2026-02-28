from db import TaskDB
from entity import Task
from datetime import datetime
from state_machine import StateMachine


class TaskManager:

    def __init__(self):
        self.taskdb = TaskDB()
        self.sm = StateMachine()

    def view_all(self):

        tasks = self.taskdb.get_all_tasks()

        numbered_tasks = [[idx + 1] + t.to_list() for idx, t in enumerate(tasks)]
        return numbered_tasks

    def add_task(self, title, note=""):

        task_obj = Task(title, note=note)

        self.taskdb.create_task(task_obj)

    def get_task_by_display_id(self, display_id):

        tasks = self.taskdb.get_all_tasks()

        if not (1 <= display_id <= len(tasks)):
            raise ValueError

        task = tasks[display_id - 1]
        return task

    def get_task_by_filter(self, filter, value):

        if filter not in ["TITLE", "CREATED_ON", "COMPLETED_ON"]:
            raise ValueError(
                "Only 'TITLE', 'CREATED_ON', 'COMPLETED_ON' filters allowed"
            )
        tasks = self.taskdb.fetch_task(filter, value)
        return tasks

    def delete_task(self, display_id):

        task = self.get_task_by_display_id(display_id)

        if not task:
            raise ValueError("Not found")

        self.taskdb.delete_task(task.task_id)

    def update_task(self, display_id, title=None, note=None, state=None):

        task = self.get_task_by_display_id(display_id)
        if task.state == "DONE":
            raise ValueError("Cannot modify 'DONE' task")

        if state is not None:
            if not self.sm.can_transition(task.state, state):
                raise ValueError("Invalid Transition")

            task.state = state
            if task.state == "DONE":
                task.completed_at = datetime.now()

        if title is not None:
            task.title = title
        if note is not None:
            task.note = note

        self.taskdb.update_task(task)


if __name__ == "__main__":

    tm = TaskManager()

    all_tasks = tm.view_all()
    for i in all_tasks:
        print(i)

    # tm.add_task("C++ Programming", note="1 hr")
    # print(tm.get_task_by_display_id(2))
    # print(tm.delete_task(2))
    print(tm.update_task(3, state="DONE"))
