from pathlib import Path
import csv

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

        with open(self.file_path, "w") as f:

            writer = csv.writer(f)
            writer.writerows(rows)

    def append_row(self, row: list):

        with open(self.file_path, "a") as f:

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


class StateTransitionDB:

    def __init__(self):
        self.json_handler = JSONFile("state_transitions.json")

    def __initial_data(self):

        data = {0: [1, 3], 1: [0, 2, 3], 2: [0], 3: []}
        return data

    def initialize(self):

        data = self.__initial_data()
        self.json_handler


if __name__ == "__main__":

    stdb = StateTransitionDB()
    taskdb = TaskDB()
