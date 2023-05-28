import pandas as pd
from DB import Database


class ReasoningEngine:
    def __init(self, db_name):
        self.db = Database(db_name)