import pandas as pd
from nltk.corpus import cmudict
import string

phoneme_dict = dict(cmudict.entries())

# Storing file paths
stop_words_file = './StopWords/StopWords_All.txt'
positive_words_file = './MasterDictionary/positive-words.txt'
negative_words_file = './MasterDictionary/negative-words.txt'

personal_pronouns_list = ["i", "we", "my", "ours", "us"]

# Storing master dictionary and stopwords in lists and converting them to lower case
with open(stop_words_file, 'r') as f_object:
    stop_word_list = f_object.read().split()

stop_word_list = [stop_word.lower() for stop_word in stop_word_list]

with open(positive_words_file, 'r') as f_object:
    positive_word_list = f_object.read().split()

positive_word_list = [positive_word.lower() for positive_word in positive_word_list]

with open(negative_words_file, 'r', encoding = "ISO-8859-1") as f_object:
    negative_word_list = f_object.read().split()

negative_word_list = [negative_word.lower() for negative_word in negative_word_list]

# Reading dataset
output = pd.read_csv("Output_Data_Structure.csv")

def syllables_in_word(word):
    # To get the number of syllables in a word
    if word in phoneme_dict:   
        return len( [ph for ph in phoneme_dict[word] if ph.strip(string.ascii_letters)] )
    else:        
        return 0

for id in range(37,151):

    positive_words = 0
    negative_words = 0
    polarity = 0
    subjective_score = 0
    avg_sentence_length = 0
    percentage_complex_words = 0
    fog_index = 0
    complex_word_count = 0
    word_count = 0
    syllable_count = 0
    syllable_per_word = 0
    personal_pronouns = 0
    avg_word_length = 0

    # Opening text files and storing the words in a list
    filename = str(id)+".txt"
    with open(filename, 'r') as f_object:
        file_word_list = f_object.read().split()

    # Filtering the word list and calculating the positive and negative score
    filtered_word_list = []
    for word in file_word_list:
        if word.lower() in stop_word_list:
            filtered_word_list.append(word)
        if word.lower() in positive_word_list:
            positive_words += 1
        if word.lower() in negative_word_list:
            negative_words += 1

    # Converting the filtered word list ot lower case
    filtered_word_list = [filtered_word.lower() for filtered_word in filtered_word_list]

    # Calculating polarity and subjective score
    polarity = (positive_words - negative_words)/((positive_words + negative_words) + 0.000001)
    subjective_score = (positive_words + negative_words)/(len(filtered_word_list) + 0.000001)

    # Calculating word length
    word_count = len(filtered_word_list)

    # Calculating average sentence length
    wordcounts = []
    with open(filename) as f:
        text = f.read()
        sentences = text.split('.')     # Creating a list of all sentences
        for sentence in sentences:      # Iterating through all sentences
            words = sentence.split(' ')     # Creating a list of all words in a sentence
            wordcounts.append(len(words))       # Appending length of each word in a sentence to a list
    avg_sentence_length = sum(wordcounts)/len(wordcounts)

    # Calculating the number of complex words
    character_count = 0
    for word in filtered_word_list:
        d = {}.fromkeys('aeiou',0)
        haslotsvowels = False
        for w in filtered_word_list:
            if w in d:
                d[w] += 1
        for q in d.values():
            if q > 2:
                haslotsvowels = True
        if haslotsvowels:
            complex_word_count += 1

        # Total number of syllables
        syllable_count += syllables_in_word(word)

        # Counting number of personal pronouns
        if word.lower() in personal_pronouns_list:
            personal_pronouns += 1

        # Counting the number of characters in each word and adding them
        character_count += len(word)

    # Calculating syllable per word, percentage of complex words, average word length, and fog index
    syllable_per_word = syllable_count/len(filtered_word_list)
    percentage_complex_words = (complex_word_count/len(file_word_list))
    avg_word_length = character_count/len(filtered_word_list)
    fog_index = 0.4*(avg_sentence_length + percentage_complex_words)

    index = id - 37

    # Storing the calculated values in the pandas dataframe
    output.loc[index, 'POSITIVE_SCORE'] = positive_words
    output.loc[index, 'NEGATIVE_SCORE'] = negative_words
    output.loc[index, 'POLARITY_SCORE'] = polarity
    output.loc[index, 'SUBJECTIVITY_SCORE'] = subjective_score
    output.loc[index, 'AVG_SENTENCE_LENGTH'] = avg_sentence_length
    output.loc[index, 'PERCENTAGE_OF_COMPLEX_WORDS'] = percentage_complex_words
    output.loc[index, 'FOG_INDEX'] = fog_index
    output.loc[index, 'AVG_NUMBER_OF_WORDS_PER_SENTENCE'] = avg_sentence_length
    output.loc[index, 'COMPLEX_WORD_COUNT'] = complex_word_count
    output.loc[index, 'WORD_COUNT'] = word_count
    output.loc[index, 'SYLLABLE_PER_WORD'] = syllable_per_word
    output.loc[index, 'PERSONAL_PRONOUNS'] = personal_pronouns
    output.loc[index, 'AVG_WORD_LENGTH'] = avg_word_length

# Saving the pandas dataframe to a csv file
output.to_csv("Output.csv")