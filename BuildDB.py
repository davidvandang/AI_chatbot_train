from DB import Database
from KB import KnowledgeBase
# Join chatbot session

# Open database session
DB = Database('chatbot.db')
KB = KnowledgeBase("chatbot.db")

# Create tables
# Past conversions
# DB.create_table("conversions", "id INTEGER PRIMARY KEY, bot TEXT, user TEXT")
# KB
# DB.create_table("KB", "id INTEGER PRIMARY KEY, user_input TEXT, answer TEXT")
# KB_Rules
# DB.create_table("KB_Rules", "id INTEGER PRIMARY KEY, condition TEXT, rule TEXT")

# KB
KB.add_user_input_answer(["book", "ticket", "buy", "reserve", "place", "seat"], "Sure, to book a ticket, can you provide these ticket details: From train station, To train station, Time you want to leave")

KB.add_user_input_answer(["predict", "train", "ticket", "late", "delay", "time"], "Sure, to predict a delayed train, can you provide these ticket details: Current station, Destination train station, Delayed time, Expected current station leaving time")






DB.close_connection()