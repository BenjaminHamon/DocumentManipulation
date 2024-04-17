import datetime


class DocumentComment:


    def __init__(self, region_identifier: str, author: str, date: datetime.datetime, text: str) -> None:
        self.region_identifier = region_identifier
        self.author = author
        self.date = date
        self.text = text
