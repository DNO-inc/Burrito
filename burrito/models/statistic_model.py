from peewee import AutoField, CharField, IntegerField

from burrito.models.basic_model import BurritoBasicModel


class StatusesStatistic(BurritoBasicModel):
    status_id = AutoField()
    name = CharField(32)
    tickets_count = IntegerField(null=False)

    def __str__(self) -> str:
        return f"{self.status_id} {self.name} {self.tickets_count}"


class FacultyScopesStatistic(BurritoBasicModel):
    faculty_id = AutoField()
    name = CharField()
    reports_count = IntegerField(column_name="Reports")
    qa_count = IntegerField(column_name="Q/A")
    suggestion = IntegerField(column_name="Suggestion")

    def __str__(self) -> str:
        return f"{self.faculty_id} {self.name}"


class ScopesStatistic(BurritoBasicModel):
    scope = CharField()
    tickets_count = IntegerField()

    def __str__(self) -> str:
        return f"{self.scope} {self.tickets_count}"


class FacultyTicketsStatistic(BurritoBasicModel):
    created_tickets_count = IntegerField()
    faculty_id = IntegerField()
    name = CharField()
