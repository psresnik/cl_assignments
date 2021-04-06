import json
import re
import sys
import gzip
import codecs
import string
from math import log2
from collections import Counter
from spacy.lang.en import English

# Dunning's llr package, https://github.com/tdunning/python-llr,
# is assumed to be in a python_llr subdirectory of this directory
import python_llr.llr as llr

# The following module is optional but useful for debugging
from traceback_with_variables import activate_by_import

# The tqdm package is handy for progress bars. You can use tqdm around any list or iterator, e.g.:
#   import tqdm
#   for line in tqdm(lines):
#      do stuff
#
from tqdm import tqdm



# Read in congressional speeches jsonlines, i.e. a file with one well formed json element per line.
# Limiting to just speeches where the chamber was the Senate, return a list of strings
# in the following format:
#   '<party>TAB<text>'
# where <party> and <text> refer to the elements of those names in the json.
# Make sure to replace line-internal whitespace (newlines, tabs, etc.) in text with a space.
# That is, any sequence of one or more whitespace characters (\s+) should be replaced
# with a single space character (' ').
#
# For information on how to read from a gzipped file, rather than uncompressing and reading, see
# https://stackoverflow.com/questions/10566558/python-read-lines-from-compressed-text-files#30868178
#
# For info on parsing jsonlines, see https://www.geeksforgeeks.org/json-loads-in-python/.
# (There are other ways of doing it, of course.)
#
def read_and_clean_lines(infile):
    print("\nReading and cleaning text from {}".format(infile))
    lines = []
    with gzip.open(infile,'rt') as f:
        for line in tqdm(f):
            pass   # ASSIGNMENT: replace this with your code
    return(lines)

# Input: lines containing <party> TAB <text>
# Writes just the text to outfile 
def write_party_speeches(lines, outfile, party_to_write):
    print("{} speeches being written to {}".format(party_to_write, outfile))
    with open(outfile, "w") as f:
        for line in tqdm(lines):
            party, text = line.split('\t')
            if party == party_to_write:
                f.write(text + '\n')

# Read a set of stoplist words from filename, assuming it contains one word per line
# Return a python Set data structure (https://www.w3schools.com/python/python_sets.asp)
def load_stopwords(filename):
    stopwords = [] # ASSIGNMENT: replace this with your code
    return set(stopwords)

# Take a list of string tokens and return all ngrams of length n,
# representing each ngram as a list of  tokens.
# E.g. ngrams(['the','quick','brown','fox'], 2)
# returns [['the','quick'], ['quick','brown'], ['brown','fox']]
# Note that this should work for any n, not just unigrams and bigrams
def ngrams(tokens, n):
    # Returns all ngrams of size n in sentence, where an ngram is itself a list of tokens
    return []  # ASSIGNMENT: Replace this with your code

def filter_punctuation_bigrams(ngrams):
    # Input: assume ngrams is a list of ['token1','token2'] bigrams
    # Removes ngrams like ['today','.'] where either token is a punctuation character
    # Returns list with the items that were not removed
    punct = string.punctuation
    return [ngram   for ngram in ngrams   if ngram[0] not in punct and ngram[1] not in punct]

def filter_stopword_bigrams(ngrams, stopwords):
    # Input: assume ngrams is a list of ['token1','token2'] bigrams, stopwords is a set of words like 'the'
    # Removes ngrams like ['in','the'] and ['senator','from'] where either word is a stopword
    # Returns list with the items that were not removed
    return ngrams # ASSIGNMENT: Replace this line with your code.


def normalize_tokens(tokenlist):
    # Input: list of tokens as strings,  e.g. ['I', ' ', 'saw', ' ', '@psresnik', ' ', 'on', ' ','Twitter']
    # Output: list of tokens where
    #   - All tokens are lowercased
    #   - All tokens starting with a whitespace character have been filtered out
    #   - All handles (tokens starting with @) have been filtered out
    #   - Any underscores have been replaced with + (since we use _ as a special character in bigrams)

    normalized_tokens = tokenlist # ASSIGNMENT: replace with your code
    
    return normalized_tokens

def collect_bigram_counts(lines, stopwords, remove_stopword_bigrams = False):
    # Input lines is a list of raw text strings, stopwords is a set of stopwords
    #
    # Create a bigram counter
    # For each line:
    #   Extract all the bigrams from the line 
    #   If remove_stopword_bigrams is True:
    #     Filter bigrams that contain at least one stopword
    #   Increment the count for each bigram
    # Return the counter
    #
    # In the returned counter, the bigrams should be represented as string tokens containing underscores.
    # 
    if (remove_stopword_bigrams):
        print("Collecting bigram counts with stopword-filtered bigrams")
    else:
        print("Collecting bigram counts with all bigrams")
    
    # Initialize spacy and an empty counter
    print("Initializing spacy")
    nlp       = English(parser=False) # faster init with parse=False, if only using for tokenization
    counter   = Counter()

    # Iterate through raw text lines
    for line in tqdm(lines):

        pass # ASSIGNMENT: placeholder for your code

        # Call spacy and get tokens

        # Normalize 

        # Get bigrams

        # Filter out bigrams where either token is punctuation
        
        # Optionally filter stopword bigrams
        
        # Increment bigram counts

    return counter

# Given a counter containing underscore-separated bigrams (e.g. "united_states") and their counts,
# return a counter with marginal counts for the unigram tokens for either the 1st or 2nd position.
# For position 0:  freq(a,.) = sum over b freq(a_b)
# For position 1:  freq(.,b) = sum over a freq(a_b)
def get_unigram_counts(bigram_counter, position):
    unigram_counter = Counter()
    for bigramstring in bigram_counter:
        tokens = bigramstring.split('_')
        unigram_counter[tokens[position]] += bigram_counter[bigramstring]
    return unigram_counter

# Given bigram and unigram counters, create a Counter object that maps
# each bigram to its pointwise mutual information, where
# PMI(a_b) = log2(Pr(a_b)/Pr(a_.)Pr(._b)) = log2(N * freq(a_b)/freq(a_.)freq(._b))
# with N = the sum of the bigram frequencies.
# Exclude any bigram whose count is less than min_freq
def compute_pmi(bigram_counts, unigram_w1_counts, unigram_w2_counts, min_freq = 1):
    bigram_pmi   = Counter()
    N            = sum(bigram_counts.values())
    for bigram in bigram_counts:
        freq_bigram  = bigram_counts[bigram]
        if freq_bigram >= min_freq:
            w1, w2       = bigram.split('_')
            freq_w1      = unigram_w1_counts[w1]
            freq_w2      = unigram_w2_counts[w2]
            pmi          = log2( N * freq_bigram / (freq_w1 * freq_w2) )
            bigram_pmi[bigram] = pmi
            print(bigram)
    return bigram_pmi

def print_sorted_items(dict, n=10, order='ascending'):
    if order == 'descending':
        multiplier = -1
    else:
        multiplier = 1
    ranked = sorted(dict.items(), key=lambda x: x[1] * multiplier)
    for key, value in ranked[:n] :
        print(key, value)



################################################################
# Main
################################################################

# Hard-wired variables
#input_speechfile   = "./speeches2020.jsonl.gz"
input_speechfile   = "./speeches2020_jan_to_jun.jsonl.gz"
text_dems          = "./speeches_dem.txt"
text_reps          = "./speeches_rep.txt"
stopwords_file     = "./mallet_en_stoplist.txt"
min_freq_for_pmi   =  5
topN_to_show       = 50

def main():
    
    # Read in the stopword list
    stopwords = load_stopwords(stopwords_file)
    
    # Read input speeches as json, and create one file for each party containing raw text one speech per line.
    # Effectively this is creating a corpus with two subcorpora, one each for Democratic and Republican speeches.
    print("\nProcessing text from input file {}".format(input_speechfile))
    lines = read_and_clean_lines(input_speechfile)

    print("\nWriting Democrats' speeches to {}".format(text_dems))
    write_party_speeches(lines, text_dems, "Democrat")
    
    print("\nWriting Republicans' speeches to {}".format(text_reps))
    write_party_speeches(lines, text_reps, "Republican")

    # Read speeches and get counts for unigrams and bigrams.
    # Note that tokenization and normalization are taking place inside collect_bigram_counts.
    # (It would not be uncommon instead to create an intermediate file with the tokenized/normalized text.)
    # Also note that unigram counts are computed as marginals of bigram counts, not directly from the corpus,
    # which would yield correct results even if bigram counts were smoothed.
    print("\nGetting Dem unigram and bigram counts")
    with open(text_dems) as f:
        dem_speeches = f.readlines()
    dem_bigram_counts     = collect_bigram_counts(dem_speeches, stopwords, True)
    dem_unigram_w1_counts = get_unigram_counts(dem_bigram_counts,0)
    dem_unigram_w2_counts = get_unigram_counts(dem_bigram_counts,1)
    print("\nTop Dem bigrams by frequency")
    print_sorted_items(dem_bigram_counts, topN_to_show, 'descending')

    print("\nGetting Rep unigram and bigram counts")
    with open(text_reps) as f:
        rep_speeches = f.readlines()
    rep_bigram_counts     = collect_bigram_counts(rep_speeches, stopwords, True)
    rep_unigram_w1_counts = get_unigram_counts(rep_bigram_counts,0)
    rep_unigram_w2_counts = get_unigram_counts(rep_bigram_counts,1)
    print("\nTop Rep bigrams by frequency")
    print_sorted_items(rep_bigram_counts, topN_to_show, 'descending')

    # Compute Pointwise Mutual Information (PMI) as a measure of how "sticky" bigrams are.
    
    dem_pmi = compute_pmi(dem_bigram_counts, dem_unigram_w1_counts, dem_unigram_w2_counts, min_freq_for_pmi)
    print("\nStickiest Dem bigrams by PMI")
    print_sorted_items(dem_pmi, topN_to_show, 'descending')

    rep_pmi = compute_pmi(rep_bigram_counts, rep_unigram_w1_counts, rep_unigram_w2_counts, min_freq_for_pmi)
    print("\nStickiest Rep bigrams by PMI")
    print_sorted_items(rep_pmi, topN_to_show, 'descending')

    # Compute log-likelihood ratio (LLR, Dunning 1993) as a statistical association measure to score
    # bigrams by how associated they are with the Democratic or Republican subcorpora.
    #
    # This is computing a test statistic for the following 2x2 contingency table of frequencies:
    #   {this_bigram, not_this_bigram} x {Democrat, Republican}
    # with the null hypothesis being that the bigram is equally likely to be in either set of text.
    # Higher positive values will indicate stronger statistical association with Democrats.
    # More extreme negative values will indicate stronger statistical association with Republicans.
    # See Jurafsky & Martin SLP 3rd ed., Section 20.5.1 (log odds ratio) for discussion of some improvements
    # on this approach that take advantage of a reference corpus. 
    #
    # Note that LLR can also be used with a single corpus as a "stickiness" measure
    # like PMI for a bigram a_b (which is what Dunning did in his 1993 article). For that, the 2x2 table is:
    #   {word1 is a, word1 is not a} x {word2 is b, word2 is not b}
    # Dunning shows that this works a lot better than PMI especially for low-frequency words,
    # which is one of the main reasons a minimum frequency cutoff is used for PMI (min_freq_for_pmi above),
    # typically freq >= 5.
    
    print("\nComputing LLR comparison of Dem and Rep bigrams")
    llr_comparison = llr.llr_compare(dem_bigram_counts, rep_bigram_counts)

    print("\nTop bigrams more statistically associated with Democrats")
    print_sorted_items(llr_comparison, topN_to_show, 'descending')
    
    print("\nTop bigrams more statistically associated with Republicans")
    print_sorted_items(llr_comparison, topN_to_show, 'ascending')

    
if __name__ == "__main__":
    main()

