# Jonathan Bunch
# 12 September 2021
# Bellevue University
# DSC550-T301

# Import libraries.
import pandas as pd
import unicodedata
import sys
import nltk
import sklearn


# Pre-processing Text: For this part, you will start by reading the
# controversial-comments.jsonl file into a DataFrame.
df = pd.read_json("week-2/controversial-comments.jsonl", lines=True, nrows=5000)


# Then,
# A. Convert all text to lowercase letters.
# B. Remove all punctuation from the text.
# C. Remove stop words.
# D. Apply NLTK’s PorterStemmer.

# Create a translation table that maps punctuation characters to None values.
punc_tbl = dict.fromkeys(i for i in range(sys.maxunicode) if unicodedata.category(chr(i)).startswith('P'))
# Load the list of stop words from the nltk library.
# nltk.download('stopwords')
stop_words = nltk.corpus.stopwords.words('english')
# Create a Stemmer from the nltk PorterStemmer function.
porter = nltk.stem.porter.PorterStemmer()


def prep_text(t):
    """ This function will convert all text to lowercase letters, remove all punctuation, tokenize the text into words,
    remove all stop words, apply the PorterStemmer function to each word, and finally recombine the tokenized words."""
    # Strip any leading or following white spaces and convert all text to lowercase.
    text = t.strip().lower()
    # Apply the translation table to the text to remove punctuation characters.
    text = text.translate(punc_tbl)
    # Next, we will tokenize the text into individual words.
    tok_text = nltk.tokenize.word_tokenize(text)
    # Create a new list of tokenized words that are NOT stop words.
    tok_text_nsw = [word for word in tok_text if word not in stop_words]
    # Now we can apply the nltk PorterStemmer function to stem the tokenized words.
    tok_text_fin = [porter.stem(word) for word in tok_text_nsw]
    # Combine the cleaned and stemmed words back into a string.
    text_fin = " ".join(tok_text_fin)
    return text_fin


# 2. Now that the data is pre-processed, you will apply three different techniques to get it into a usable form
# for model-building. Apply each of the following steps (individually) to the pre-processed data.

# Apply the pre-processing function to the text data and add the results to the table as a new column.
df['prepped_text'] = df['txt'].apply(prep_text)
# It might also be useful to add the tokenized version of this pre-processed text as another new column.
df['prepped_tokens'] = df['prepped_text'].apply(nltk.tokenize.word_tokenize)

# A. Convert each text entry into a word-count vector
# (see sections 5.3 & 6.8 in the Machine Learning with Python Cookbook).

# Create a vectorizer from the sklern CountVectorizer() function.
count = sklearn.feature_extraction.text.CountVectorizer()
# Apply the vectorizer to the prepared text feature.
wcv = count.fit_transform(df.prepped_text)


# B. Convert each text entry into a part-of-speech tag vector
# (see section 6.7 in the Machine Learning with Python Cookbook).

# Create a list that will store the part of speech tag for each word in each observation.
tagged_list = []

# Loop through the tokenized words in each observation, tagging each word with its part of speech.
# Add the part of speech tags, per each observation, to the tagged_list.
for val in df.prepped_tokens.values:
    tags = nltk.pos_tag(val)
    tagged_list.append([tag for word, tag in tags])

# Create a one-hot binarizer from the sklearn MultiLabelBinarizer() function.
one_hot_multi = sklearn.preprocessing.MultiLabelBinarizer()
# Apply the binarizer to the tagged_list to create one-hot encoded part-of-speech vectors.
psv = one_hot_multi.fit_transform(tagged_list)


# C. Convert each entry into a term frequency-inverse document frequency (tfidf) vector
# (see section 6.9 in the Machine Learning with Python Cookbook).

# Create the tfidf vectorizer.
tfidf = sklearn.feature_extraction.text.TfidfVectorizer()
# Apply the vectorizer to create a tfidf feature matrix.
tfv = tfidf.fit_transform(df.prepped_text)


# Follow-Up Question
# For the three techniques in problem (2) above, give an example where each would be useful.
