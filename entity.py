from uuid import uuid4
from datetime import datetime
from state_machine import StateMachine


class Task:

    def __init__(
        self,
        title,
        created_at=None,
        completed_at=None,
        task_id=None,
        note="",
        state="TODO",
    ):

        self.task_id = str(task_id) if task_id else str(uuid4())
        self.title = title
        self.created_at = (
            datetime.strptime(created_at, "%d-%m-%Y %H:%M:%S")
            if created_at
            else datetime.now()
        )
        self.completed_at = (
            datetime.strptime(completed_at, "%d-%m-%Y %H:%M:%S")
            if completed_at
            else None
        )
        self.note = note
        self.state = state

        self.validate_fields()

    def to_list(self):

        return [
            self.task_id,
            self.title,
            self.created_at.strftime("%d-%m-%Y %H:%M:%S"),
            (
                self.completed_at.strftime("%d-%m-%Y %H:%M:%S")
                if self.completed_at
                else ""
            ),
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

    def validate_fields(self):

        if not self.title or self.title.isspace():
            raise ValueError("Field cannot be empty")

        if self.state not in StateMachine.transitions.keys():
            raise ValueError("Invalid state")

        if not self.completed_at and self.state == "DONE":
            raise ValueError("Completed time should be created when task 'DONE'")

        if self.state != "DONE" and self.completed_at:
            raise ValueError("Cannot create Completed time when state is not 'DONE'")
