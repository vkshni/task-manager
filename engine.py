from db import TaskDB
from entity import Task
from datetime import datetime


class TaskManager:

    def __init__(self):
        self.taskdb = TaskDB()

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

    def delete_task(self, display_id):

        task = self.get_task_by_display_id(display_id)

        if not task:
            raise ValueError("Not found")

        self.taskdb.delete_task(task.task_id)


if __name__ == "__main__":

    tm = TaskManager()

    all_tasks = tm.view_all()
    for i in all_tasks:
        print(i)

    # tm.add_task("C++ Programming", note="1 hr")
    # print(tm.get_task_by_display_id(2))
    # print(tm.delete_task(2))
