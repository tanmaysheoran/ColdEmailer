from classes.MotherClass import MotherClass


class UserEmailTemplate(MotherClass):
    to: str
    cc: list[str] = []
    subject: str
    body: str
    sent: bool = False
