import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
import string

# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('porter_test')

# Test string before using user_input
test_string = "Hello, I would like to book a train from Weymouth to Waterloo tommorrow at 2:00PM"


def processing(input_string):
    # Split into separate tokens
    tokens = word_tokenize(input_string)

    # Lowercase
    tokens = [w.lower() for w in tokens]

    # Remove punctuation except ':'
    punctuation_to_remove = string.punctuation.replace(':', '')  # all punctuation except ':'
    table = str.maketrans('', '', punctuation_to_remove)
    stripped = [w.translate(table) for w in tokens]

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    filtered_words = [w for w in stripped if not w in stop_words]

    # Stemming
    ps = PorterStemmer()
    stemmed_words = [ps.stem(word) for word in filtered_words]

    print(stemmed_words)


processing(test_string)
