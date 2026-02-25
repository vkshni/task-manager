from pathlib import Path
import csv

from entity import Task

BASE_DIR = Path(__file__).parent


class CSVFile:

    def __init__(self, file_name):
        self.file_path = self.create(file_name)

    def create(self, file_name):

        path = BASE_DIR / "database" / file_name
        if not path.exists():
            with open(path, "x") as f:
                pass
        return path

    def read_all(self):

        with open(self.file_path, "r") as f:

            reader = csv.reader(f)
            rows = [row for row in reader]
            return rows

    def write_all(self, rows: list[list]):

        with open(self.file_path, "w", newline="") as f:

            writer = csv.writer(f)
            writer.writerows(rows)

    def append_row(self, row: list):

        with open(self.file_path, "a", newline="") as f:

            writer = csv.writer(f)
            writer.writerow(row)


class JSONFile:

    def __init__(self, file_name):
        self.file_path = self.create(file_name)

    def create(self, file_name):

        path = BASE_DIR / "database" / file_name
        if not path.exists():
            with open(path, "x") as f:
                pass
        return path


class TaskDB:

    def __init__(self):
        self.csv_handler = CSVFile("tasks.csv")
        self.initialize()

    def __initial_data(self):

        header = ["task_id", "title", "created_at", "completed_at", "note", "state"]
        return header

    def initialize(self):

        try:
            self.csv_handler.read_all()
        except:
            row = self.__initial_data()
            self.csv_handler.append_row(row)

    def get_all_tasks(self, skip_header=True):

        rows = self.csv_handler.read_all()
        if skip_header:
            rows = rows[1:]

        tasks = [Task(r[1], r[2], r[3], r[0], r[4], r[5]) for r in rows]
        return tasks

    def create_task(self):
        pass

    def update_task(self):
        pass

    def delete_task(self):
        pass

    def fetch_task(self):
        pass


if __name__ == "__main__":

    taskdb = TaskDB()
    all_task = taskdb.get_all_tasks()
    for task in all_task:
        print(task.task_id, task.title)
