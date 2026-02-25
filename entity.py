from uuid import uuid4


class Task:

    def __init__(
        self, title, created_at, completed_at, task_id=None, note="", state="TODO"
    ):

        self.task_id = str(task_id) if task_id else uuid4()
        self.title = title
        self.created_at = created_at
        self.completed_at = completed_at
        self.note = note
        self.state = state

    def to_list(self):

        return [
            self.task_id,
            self.title,
            self.created_at,
            self.completed_at,
            self.note,
            self.state,
        ]

    @classmethod
    def from_dict(cls, task_dict):

        return cls(
            task_dict["task_id"],
            task_dict["title"],
            task_dict["created_at"],
            task_dict["completed_at"],
            task_dict["note"],
            task_dict["state"],
        )
