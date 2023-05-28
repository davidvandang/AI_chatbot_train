from NLP import NaturalLanguageProcessing
from KB import KnowledgeBase
from DB import Database

# Create instances of the required classes
NLP = NaturalLanguageProcessing()
DB = Database("chatbot.db")
KB = KnowledgeBase("chatbot.db")

class Chatbot:
    def __init__(self, db):
        self.db = db
        self.nlp = NaturalLanguageProcessing()

    def get_input_from_frontend(self, user_input):
            # Process the user's input
            tokens = self.nlp.nlpMethod(user_input)
            print(tokens)

            # Check the KnowledgeBase for a suitable response
            kb_response = KB.find_response(tokens)

            # With the matched answer, add the important words to build the KB
            KB.add_tokens_matched_answer(kb_response)

            # If the KnowledgeBase has a response, use that
            if kb_response is not None:
                return kb_response

# Main program
if __name__ == "__main__":
    chatbot = Chatbot(KB)
    # ... rest of the code

