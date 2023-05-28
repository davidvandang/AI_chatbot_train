import pandas as pd
from DB import Database
from NLP import NaturalLanguageProcessing
import sqlite3
class KnowledgeBase:
    def __init__(self, db):
        self.db = db
        self.conn = sqlite3.connect(db)  # Get the database connection
        self.cursor = self.conn.cursor()

    # Get the table needed for function in KB
    def get_all_data_KB(self):
        self.cursor.execute(f"SELECT * FROM KB")
        all_data = self.cursor.fetchall()
        return all_data

    # def store_train_information(self, ):
    # def store_user_input_conversations(self, user_input):


    def find_response(self, npl_input_tuple):
        npl_input_list, _ = npl_input_tuple  # Extract the list from the tuple
        npl_input_string = ' '.join(npl_input_list)  # Convert list to string
        print(npl_input_string)

        # Create a new connection and cursor object
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()

        query = "SELECT answer, user_input FROM KB"
        cursor.execute(query)
        results = cursor.fetchall()

        match_counts = {}  # Dictionary to store match counts for each response
        total_match_count = 0  # Total count of matching words across all responses

        best_response = None
        highest_probability = 0.0

        # Iterate through the results
        for (answer, user_input) in results:
            # Split the user input and the user_input column into individual words
            input_words = user_input.split()

            # Calculate the count of matching words
            match_count = sum(1 for word in npl_input_list if word in input_words)

            # Update match counts and total match count
            match_counts[(answer, user_input)] = match_count
            total_match_count += match_count

            # Calculate the probability of matching for each response
            if total_match_count != 0:
                probability = match_count / total_match_count
            else:
                probability = 0

            # Update the best response if the current probability is higher
            if probability > highest_probability:
                highest_probability = probability
                best_response = answer

        # Check if there is a best response with non-zero probability
        if best_response is not None and highest_probability > 0:
            return best_response
        else:
            try_again = "Sorry, can you send another message?"
            return try_again

    def add_tokens_matched_answer(self, best_response):
        # Create a new connection and cursor object
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()

        query = "SELECT answer, user_input FROM KB"
        cursor.execute(query)
        results = cursor.fetchall()

        # Iterate through the results
        for answer, user_input in results:
            if best_response == answer:
                # Split the user_input and best_response into individual tokens
                user_input_tokens = user_input.split()
                best_response_tokens = best_response.split()

                # Combine the old user_input and new tokens
                updated_user_input_tokens = user_input_tokens + best_response_tokens

                # Convert the updated tokens back to a string
                updated_user_input = " ".join(updated_user_input_tokens)

                # Update the user_input in the KB table
                update_query = "UPDATE KB SET user_input = ? WHERE answer = ?"
                cursor.execute(update_query, (updated_user_input, answer))
                conn.commit()

        # Close the connection
        cursor.close()
        conn.close()
    def add_user_input_answer(self, user_input, answer):
        # Convert the array of words to a string
        user_input_str = " ".join(user_input)
        query = f"INSERT INTO KB (user_input, answer) VALUES (?, ?)"
        self.cursor.execute(query, (user_input_str, answer))
        self.conn.commit()
    def add_rule_KB(self, condition, rule):
        self.cursor.execute("INSERT INTO KB_Rules (conditions, rules) VALUES (?, ?)", (condition, rule))
        self.conn.commit()

    # Remove rule
    def remove_rule_KB(self, condition, rule):
        query = f"DELETE FROM KB_Rules WHERE condition = ? AND rule = ?"
        self.cursor.execute(query, (condition, rule))
        self.conn.commit()


    # Webscraping with user information to get the ticket



    # Get all rules

def test_knowledge_base():
    kb = KnowledgeBase('chatbot.db')

    # Test getting all data from KB
    print("\nGetting all data from KB:")
    print(kb.get_all_data_KB())

    # Test adding user input and answer
    # user_input = ('this', 'is', 'a', 'test')  # Input as a tuple
    # answer = "This is the test answer"
    # kb.add_user_input_answer(user_input, answer)

    # Test finding response
    nlp_input_tuple = (['to', 'book', 'ticket', 'dog', 'cat', 'fly'], [])  # Input as a tuple
    print("\nFinding response for NLP input string 1:")
    print(kb.find_response(nlp_input_tuple))
    kb.add_tokens_matched_answer(nlp_input_tuple)
    # Test finding response
    nlp_input_tuple2 = (['help', 'book', 'ticket', 'tomorrow'], [])  # Input as a tuple
    print("\nFinding response for NLP input string 2:")
    print(kb.find_response(nlp_input_tuple2))


if __name__ == "__main__":
    test_knowledge_base()