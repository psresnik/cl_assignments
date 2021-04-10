
## Normalizing text and exploring collocations in a corpus

### Overview
In this assignment, you'll get experience with:

- Starting with a typical "raw" dataset 
	- We'll be using a dataset of speeches from the U.S. Congressional Record during 2020, acquired using code at [https://github.com/ahoho/congressional-record](https://github.com/ahoho/congressional-record).  This is publicly available material.
- Extracting relevant text to create one or more corpora
	- We'll restrict ourselves to the Senate, and create subcorpora of speeches by Democrats and Republicans.
- Tokenizing text
	- We'll use the spaCy tokenizer
- Normalizing text
	- We'll use case folding and also a stopword list
- Extracting potentially useful ngrams
	- In this assignment we'll focus on bigrams
- Answering questions like:
	- Which bigrams are frequent?
	- Which bigrams are "stickiest" as phrases?
	- Which bigrams are statistically more associated with one group than another?

### The files you'll be working with  
You'll be working with the following:

- Files in [jsonlines](https://jsonlines.org/) format containing raw data
	- `test_speeches.jsonl.gz` - small example data for testing
	- `speeches2020_jan_to_jun.jsonl.gz` - main data you'll run on
- Files containing code
	- `assignment.py` - code skeleton that you'll fill in
	- `public_tests_obj.py` - code to run for unit testing
- Other resources
	- `mallet_en_stoplist.txt` - the stopword list from the widely used [Mallet](http://mallet.cs.umass.edu/) toolkit
	- `python_llr` - Ted Dunning's [python-llr](https://github.com/tdunning/python-llr) package for computing log-likelhood ratio stats

### What you should do

- Check out this repo
        - As a reminder, although the repo is publicly available, please do not post public solutions to the problems (e.g., please do not create a public fork of the repository where you work on solutions).

- Execute `python assignment.py`
	- It should run successfully from end to end with progress messages on the output
	- If it does not, most likely it's because it is using packages you don't have installed. Install them (see: requirements.txt)
		- If you use conda, we recommend installing a fresh conda env and putting your classwork dependencies there.
		- Execute 

				conda create --name YOURCONDAENVIRONMENT python=3.8
				conda activate YOURCONDAENVIRONMENT
				which pip
				
		- Ensure that your `pip` lives in its own env, like: `/anaconda3/envs/YOURCONDANEVIRONMENT/bin/pip`
		- Execute `pip install -r requirements.txt`

- Execute `python public_tests_obj.py -v`
	- The code should run, but will report on tests that have failed.

- Read and modify `assignment.py`.  
	- Each function has a detailed comment about input, output, and what it does.
	- You can look at `public_tests_obj.py` for examples of the function calls.
	- You will find a comment like `# ASSIGNMENT: replace this with your code` everywhere you have work to do.
	- Keep working until all the tests pass when you run `public_tests_obj.py`.

- **Code to be graded (50%).** Once all tests pass, submit `assignment.py` to the autograder. This will be the basis for grading your code.  Here are the point values for the tests.
    - Public: `test_read_and_clean_lines` (5%)
    - Public: `test_filter_stopword_bigrams` (5%)
    - Public: `test_normalize_tokens` (5%)
    - Private: `test_bigrams` (5%)
    - Private: `test_fourgrams` (5%)
    - Private: `test_normalize_tokens` (10%)
    - Private: `test_bigram_frequency` (15%)

- **Analysis to be graded (50%).** For the analysis part of the assignment, look at the output of `assignment.py` and submit brief but clear written answers to the following questions, as PDF.  Note that, particularly if you are not very familiar with U.S. politics, you are welcome to discuss the data you're looking at with other other people -- as long as you state explicitly in your writeup that you have done so, and of course you need to write your answers in your own words. *For all responses make sure to support your answers with examples.*


	1. **Looking at frequency.** The first set of outputs are lists of the top Democratic and Republican bigrams by frequency. 

		**Question 1 to answer (15%).**  Looking at these lists, how similar or different are the most-frequent bigrams used by members of the two parties?  Are there any generalizations you can make about the two parties, at least during this time period, based on this information? If yes, discuss. If you think the answer is no, clearly explain why. Support your answer with examples.

	
	2. **Associations between words: "sticky" bigrams.** For the second set of outputs, we have computed *pointwise mutual information* (PMI) for each bigram. You don't need to know a lot about PMI, though you can read the discussion in Jurafsky and Martin  (SLP 3rd ed), Section 6.6, for a description. Here's a short summary of what youj'll want to know.

		The very straightforward intuition for PMI is this: if you want to know how strongly associated two words are, then you can ask, do they occur together a lot  more often than you'd expect by chance? For a bigram of two words, *w1 w2* (e.g., say, *linguistics professor*), you estimate their probability of occurring together as a bigram, Pr(w1,w2), in your corpus. (In this assignment we're using a maximum likelihood estimate, no smoothing.) Chance co-occurrence is estimated assuming the words are independent, not associated, so it's just the product of the individual words' probabilities Pr(w1)Pr(w2).  
		
		The core of mutual information is simply the ratio of the two probabilities, Pr(w1,w2)/[Pr(w1)Pr(w2)].  The higher that ratio is, the more often you're seeing these two words co-occurring together, in that order as a bigram, compared to what you'd expect by chance. PMI actually takes the log of that ratio; this has the nice effect of making PMI positive when the words co-occur more often than expected by chance, and it's also closely connected to the quantity I(X;Y) in information theory, which is the "average mutual information" between two random variables, often just called "mutual information". (The connection to information theory is why the log is usually log2.)

		With that as the definition, you can see that the PMI value for a phrase can be thought of as how "sticky" words in the phrase are with each other. A bigram like *linguistics professor* is not particularly "sticky", because *linguistics* occurs before lots of other words, *professor* occurs after lots of other things. On the other hand, a bigram like *White House* is incredibly "sticky" in the sense that, at least in a news or political context, these words go together a whole lot more than you'd expect just by chance. (That's even more true if you didn't normalize by lowercasing!) 
		
		And you'll notice something else, too: the meaning of *linguistics professor* is pretty much fully determined by the meanings of the two words -- a linguistics professor is a professor who is in the field of linguistics.  The meaning is [*compositional*](https://iep.utm.edu/composit/) in the sense that it's build up out of the meanings of its parts and not anything else. But *White House* is something else entirely. Yes, the meaning of *White House* is connected with a white-colored domicile in Washington D.C. But the meanings of *White House* are not really built from those parts. It's not just *any* white house, it's the home of the U.S. President, the seat of government, the executive department of the government, etc. Those elements of meaning are associated with *White House* as a *unit*; you don't get to a meaning of *White House* just from the meanings of the individual words. 
		
		The distributional "stickiness", as measured by quantities like PMI, is actually a way of identifying phrases that behave as units that are not just combined together from their pieces. Sticky units like this are often referred to as "collocations", although that term is also sometimes used just to refer to "words that occur close to the word you're intersted in".
		
		**Question 2 to answer (20%).**  
		
		2.1 Looking at the stickiest bigrams as measured by PMI in the Democratic and Republican subcorpora, what kinds of bigrams/phrases do you see showing up, and how do the top items compare with the top items you get just using frequency?  
		
		2.2 Is PMI identifying things that might be useful in working with language in this domain or understanding differences between Democrats and Republicans?  
		
	3. **Statistical associations between words and groups.**  Finally, the last pair of outputs you'll see are bigrams ranked by how strongly they are statistically associated with Democrats or Republicans.  

		Again, you don't need to know details about the statistical measure that's been implemented here. But in case you're interested, the score you're seeing is similar in spirit to PMI: it's quantifying how different something is from chance.  Except this time, it's not looking at *word-to-word* associations, it's looking at *bigram-to-subcorpus* associations. If a bigram is up near the top of the "Top bigrams more statistically associated with Republicans" list, for example, that means that it's being said by Republicans much more than you'd expect if it had no particular associations with either party. 
		
		The particular statistical measure we've implemented here is the log-likelihood ratio, which was introduced by [Dunning (1993)](https://www.aclweb.org/anthology/J93-1003/), and in fact we're using [Ted Dunning's implementation](https://github.com/tdunning/python-llr). If you've had some stats before, you can think of this in the same way as a chi-squared test for looking at the association between two binary variables, except that Dunning's 1993 article showed that this test is better when you're dealing with low frequencies.  Jurafsky and Martin (SLP, 3rd ed.) discuss the idea of using this kind of test to distinguish between two different groups in Section 20.5.1. They talk about using this kind of statistic to find terms that distinguish positive from negative movie reviews; here we're looking at the same thing but distinguishing Democratic versus Republican speeches.

		**Question 3 to answer (15%).**

		Looking at the bigrams that are strongly associated with Democrats versus Republicans, what does this tell you about Democrats and Republicans in the Senate during this time period, for example their roles in the Senate and the issues they are concerned with?
