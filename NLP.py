import csv
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
import string
import spacy


# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('porter_test')

class NaturalLanguageProcessing:
    def __init__(self):
        self.stations = self.load_stations()
        self.nlp = spacy.load('en_core_web_sm') # Loading Spacy model in constructor

    def load_stations(self):
        stations = []
        with open('stations.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                stations.append(row[0].lower())  # Convert station name to lowercase
        return stations


    def processing(self, input_string):
        # Split into separate tokens
        tokens = word_tokenize(input_string)

        # Lowercase
        tokens = [w.lower() for w in tokens]

        # Remove punctuation except ':', '/', '-'
        unwanted_punct = [p for p in string.punctuation if p not in [':', '/', '-']]
        table = str.maketrans('', '', ''.join(unwanted_punct))
        stripped = [w.translate(table) for w in tokens]

        # Custom stop words list
        stop_words = set(stopwords.words('english'))
        except_word = {'to', 'from'}  # add more if necessary
        stop_words = [word for word in stop_words if word not in except_word]

        # Remove stop words
        filtered_words = [w for w in stripped if not w in stop_words]

        # Stemming
        ps = PorterStemmer()
        stemmed_words = [ps.stem(word) for word in filtered_words]

        # print(stemmed_words)

        return stemmed_words

    def getTokens(self, input_words):
        # Create a SpaCy doc from the words
        doc = self.nlp(' '.join(input_words))

        # Extract important tokens
        important_tokens = []
        for token in doc:
            if token.pos_ == 'PROPN':
                important_tokens.append(token.text)

            if token.pos_ == 'NUM' and token.ent_type_ == 'TIME':
                important_tokens.append(token.text)

            #Check for words 'from', 'to', 'tomorrow', and time
            if token.text in ['from', 'to', 'tomorrow', 'today', 'book', 'train', 'ticket']:
                important_tokens.append(token.text)

            if ':' in token.text:  # Detect time
                important_tokens.append(token.text)

            if '/' in token.text or '-' in token.text:  # Detect dates
                important_tokens.append(token.text)

            # Check if token contains a word from stations.csv
            if any(station.lower() in token.text.lower() for station in self.stations):
                important_tokens.append(token.text)

        return important_tokens

    def getMatchedTokens(self, tokens):
        matched_tokens = []
        for station in self.stations:
            # Split the station name into separate words
            station_words = station.split()
            # Check if any of the tokens is in the list of station words
            for token in tokens:
                if token.upper() in station_words:
                    matched_tokens.append(station)
        return matched_tokens

    def nlpMethod(self, input):
        step_1 = nlp.processing(input)
        #print("Step 1 - Preprocessed Tokens:", step_1)
        step_2 = nlp.getTokens(step_1)
        #print("Step 2 - Important Tokens:", step_2)
        step_3 = nlp.getMatchedTokens(step_2)
        # print("Step 3 - Matched Trains:", step_3)
        return step_2, step_3

nlp = NaturalLanguageProcessing()

#test_string1 = "Hello, I would like to book a train from Southampton to Waterloo tomorrow at 2:00PM"
#test_string2 = "book a train from Southampton to Waterloo 26/12/2023 at 2:00PM"

#nlp.nlpMethod(test_string1)
#nlp.nlpMethod(test_string2)




