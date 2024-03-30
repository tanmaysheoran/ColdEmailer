from classes.MotherClass import MotherClass


class PublicPrompt(MotherClass):
    name: str
    description: str
    tags: list[str]


class Prompt(PublicPrompt):
    prompt: str
