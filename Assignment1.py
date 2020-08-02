"""
This is Assignment One, this program asks for a text file and returns the number of words, unique words, adjectives,
adverbs, and the sums of the evaluation, activity, and potency values for the adjectives and adverbs in the file

This program uses Natural Language Tool Kit (NLTK) to analyze text

For CISC 121, Summer 2020
By Cormac Doyle, student number 20152002
"""
"""
Importing the necessary NLTK libraries and modules.
"""
import nltk
from nltk.tag import StanfordPOSTagger
from nltk.corpus import wordnet
from nltk import pos_tag, word_tokenize
from nltk.corpus import words
from nltk.tokenize import word_tokenize

import string
import pprint


"""
To identify the part-of-speech of the words retrieved from
Word2vec, we used the conditional frequency feature of the NLTK module
which returns a frequency-ordered list of the possible parts of speech associated
with all of the English words that are found in the Brown Corpus. Our sys-
tem uses the Brown Corpus to generate the frequency-ordered list because
of the fact that the words contained in the Brown Corpus are annotated with
part-of-speech tags.
"""

wordtags = nltk.ConditionalFreqDist((w.lower(), t) 
        for w, t in nltk.corpus.brown.tagged_words(tagset="universal"))


def findPOS(word):

    """
    This is a function that accepts a word as its parameter and returns the part-of-speech of the word.
    The function considers adjectives, adverbs and nouns.
    """
	
    lisPOS = list(wordtags[word])
    if "ADJ" in lisPOS:
        return "ADJECTIVE"
    if "ADV" in lisPOS:
        return "ADVERB"
    if "NN" in lisPOS:
        return "NOUN"

def readFile(filename):

    """
    This is a function that accepts a path to a file as its parameter, reads in and returns the file
    """
    speechFile = open(filename, "r")
    speech = speechFile.read()
    speechFile.close()
    return speech


def getWords(speech):
    """
    This is a function that segments the words in a document
    """
    return speech.split()

def removePunctuation(word_list):
    """
    This function strips punctuation from each element of the list of seperated words (parameter/input) and
    returns the list of seperated words without punctuation (output)
    """
    clean_list = []
    for item in word_list:
        clean_list.append(item.strip(string.punctuation))
    return(clean_list)
        

def prepareSemanticDifferential():

    """
    This is a function that reads in the EPA values from the Osgood wordlist and stores the values in 
    a Python dictionary.
    """
	
    filename = ("OsgoodOriginal.csv") 
    fileIn = open(filename, 'r')
    allData = []
    line = fileIn.readline()
    while line != "":
        line = fileIn.readline().strip()
        if line != "":
            values = line.split(',')
            wordData = {}
            wordData['word'] = str(values[0])
            wordData['evaluation'] = float(values[1])
            wordData['activity'] = float(values[2])
            wordData['potency'] = float(values[3])
            allData.append(wordData)
    fileIn.close()
    return allData

def countWords(cleaned_words):
    """
    This function simply counts the number of words in the speech, it's parameter is a list of words that
    do not contain punctuation
    """
    return len(cleaned_words)

def getUniqueWords(clean_words):
    """
    This function takes the cleaned list as its parameter which contains all of the words in the speech and counts all
    of the unique words in the list
    it puts the list into lower case so that the counter is not case sensitive (Dog and dog should be
    counted as the same)
    """
    words = []
    for word in clean_words:
        words.append(word.lower())
    return len(set(words))

def countAdjectives(cleaned_words):
    """
    This function has a counter for the number of times the previously defined findPOS function indicates
    if a word is an adjective from the parameter which is a list of cleaned words
    """
    adjective_count = 0
    for word in cleaned_words:
        if findPOS(word) == "ADJECTIVE":
            adjective_count += 1
    return adjective_count
        
def countAdverbs(cleaned_words):
    """
    This function has a counter for the number of times the previously defined findPOS function indicates
    if a word is an adverb from the paramter which is a list of cleaned words
    """
    adverb_count = 0
    for word in cleaned_words:
        if findPOS(word) == "ADVERB":
            adverb_count += 1
    return adverb_count

def calculateSD():
    
    """
    This function finds the sum of evaluation, activity, and potency values for all adjectives and adverbs in the speech
    """

    #creating sum variables
    evaluationSum = 0
    activitySum = 0
    potencySum = 0

    #creating adj_adv list to store cleaned adjectives and adverbs only
    adj_adv = []
    
    #this input takes the name of the speech file as a prompted user input
    speech_name = input("Hi there,\n Welcome to assignment one \n Please upload your text file to the work environment and enter the exact name of your file without quotation marks \n")
    # this try except statement says that if there is no error in the file name the process can continue and if not an error message will appear
    try:
        readFile(speech_name)
    except:
        print("That doesn't seem right, quit (Cntrl + C) and try again.")

    """
    by running previously defined functions we clean the text in the file and a cleaned (individual and free of
    punctuation) version of the text is returned
    """
    opened_speech = readFile(speech_name)
    word_list = getWords(opened_speech)
    cleaned_list = removePunctuation(word_list)

    """
    here we add all adjectives and adverbs to a list because we only consider them according to the assignment
    """
    for word in cleaned_list:
        if findPOS(word) == "ADJECTIVE":
            adj_adv.append(word)
        if findPOS(word) == "ADVERB":
            adj_adv.append(word)
    
    """
    this block takes the dictionary loaded in prepareSemanticDifferential() and tries to see if they match the adjectives
    and adverbs in the file, if they do their evaluation, activity, and potency values are added to their respective sum
    variables
    """
    semanticDifferentialData = prepareSemanticDifferential()
    for word in adj_adv:
        for item in semanticDifferentialData:
            if item["word"] == word:
                evaluationSum += float(item["evaluation"])
                activitySum += float(item["activity"])
                potencySum += float(item["potency"])
    
    # These print statements simply output all of the data
    print("Here is your analysis")
    print("There are", countWords(cleaned_list), "words in the file")
    print("There are", getUniqueWords(cleaned_list), "unique words in the file")
    print("There are", countAdjectives(cleaned_list), "adjectives in the file")
    print("There are", countAdverbs(cleaned_list), "adverbs in the file")
    print("Evaluation Score:", round(evaluationSum,2))
    print("Activity Score:",round(activitySum,2))
    print("Potency Score:",round(potencySum,2))
        
"""
The main function only calls calculateSD() since all other functions are within eachother
"""
def main():
    calculateSD()

if __name__ == "__main__":
    main()
