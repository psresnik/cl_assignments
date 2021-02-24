import unittest
from collections import Counter
# import correct_solution as solution
import assignment as solution
from spacy.lang.en import English


class TestBigramPublic(unittest.TestCase):

    def setUp(self):
        # This code runs before the tests are run
        pass

    def test_read_and_clean_lines(self):
        # Note that example_line contains a TAB not, a space, after the word Republican"
        infile        = "./test_speeches.jsonl.gz"
        correct_lines = 317
        example_line  = 'Republican\tMr. President, I ask unanimous consent that the order for the quorum call be rescinded.'
        lines         = solution.read_and_clean_lines(infile)
        self.assertEqual(len(lines), correct_lines,
            "Test failed: Count of Senate speeches in {} is incorrect, should be {}".format(infile,correct_lines))
        self.assertTrue(example_line in lines,
            "Test failed: lines did not contain '{}'. Was whitespace handled properly?".format(example_line))

    def test_load_stopwords(self):
        correct_stopwords = set(['a','able','about','above','according','accordingly','across','actually','after','afterwards','again','against','all','allow','allows','almost','alone','along','already','also','although','always','am','among','amongst','an','and','another','any','anybody','anyhow','anyone','anything','anyway','anyways','anywhere','apart','appear','appreciate','appropriate','are','around','as','aside','ask','asking','associated','at','available','away','awfully','b','be','became','because','become','becomes','becoming','been','before','beforehand','behind','being','believe','below','beside','besides','best','better','between','beyond','both','brief','but','by','c','came','can','cannot','cant','cause','causes','certain','certainly','changes','clearly','co','com','come','comes','concerning','consequently','consider','considering','contain','containing','contains','corresponding','could','course','currently','d','definitely','described','despite','did','different','do','does','doing','done','down','downwards','during','e','each','edu','eg','eight','either','else','elsewhere','enough','entirely','especially','et','etc','even','ever','every','everybody','everyone','everything','everywhere','ex','exactly','example','except','f','far','few','fifth','first','five','followed','following','follows','for','former','formerly','forth','four','from','further','furthermore','g','get','gets','getting','given','gives','go','goes','going','gone','got','gotten','greetings','h','had','happens','hardly','has','have','having','he','hello','help','hence','her','here','hereafter','hereby','herein','hereupon','hers','herself','hi','him','himself','his','hither','hopefully','how','howbeit','however','i','ie','if','ignored','immediate','in','inasmuch','inc','indeed','indicate','indicated','indicates','inner','insofar','instead','into','inward','is','it','its','itself','j','just','k','keep','keeps','kept','know','knows','known','l','last','lately','later','latter','latterly','least','less','lest','let','like','liked','likely','little','look','looking','looks','ltd','m','mainly','many','may','maybe','me','mean','meanwhile','merely','might','more','moreover','most','mostly','much','must','my','myself','n','name','namely','nd','near','nearly','necessary','need','needs','neither','never','nevertheless','new','next','nine','no','nobody','non','none','noone','nor','normally','not','nothing','novel','now','nowhere','o','obviously','of','off','often','oh','ok','okay','old','on','once','one','ones','only','onto','or','other','others','otherwise','ought','our','ours','ourselves','out','outside','over','overall','own','p','particular','particularly','per','perhaps','placed','please','plus','possible','presumably','probably','provides','q','que','quite','qv','r','rather','rd','re','really','reasonably','regarding','regardless','regards','relatively','respectively','right','s','said','same','saw','say','saying','says','second','secondly','see','seeing','seem','seemed','seeming','seems','seen','self','selves','sensible','sent','serious','seriously','seven','several','shall','she','should','since','six','so','some','somebody','somehow','someone','something','sometime','sometimes','somewhat','somewhere','soon','sorry','specified','specify','specifying','still','sub','such','sup','sure','t','take','taken','tell','tends','th','than','thank','thanks','thanx','that','thats','the','their','theirs','them','themselves','then','thence','there','thereafter','thereby','therefore','therein','theres','thereupon','these','they','think','third','this','thorough','thoroughly','those','though','three','through','throughout','thru','thus','to','together','too','took','toward','towards','tried','tries','truly','try','trying','twice','two','u','un','under','unfortunately','unless','unlikely','until','unto','up','upon','us','use','used','useful','uses','using','usually','uucp','v','value','various','very','via','viz','vs','w','want','wants','was','way','we','welcome','well','went','were','what','whatever','when','whence','whenever','where','whereafter','whereas','whereby','wherein','whereupon','wherever','whether','which','while','whither','who','whoever','whole','whom','whose','why','will','willing','wish','with','within','without','wonder','would','would','x','y','yes','yet','you','your','yours','yourself','yourselves','z','zero'])
        infile = "./mallet_en_stoplist.txt"
        stopwords = solution.load_stopwords(infile)
        self.assertTrue(all(x in stopwords for x in correct_stopwords))

        
    def test_ngrams(self):

        input_tokens    = ['the','pretty','brown','fox', 'in', 'the', 'pretty', 'woods']
        correct_bigrams = [['the','pretty'], ['pretty','brown'], ['brown','fox'],
                           ['fox','in'], ['in','the'], ['the','pretty'],['pretty','woods']]
        bigrams         = solution.ngrams(input_tokens, 2)

        self.assertEqual(bigrams, correct_bigrams,
            "Test failed: test_ngrams got the wrong bigrams")

        correct_trigrams = [['the','pretty','brown'], ['pretty','brown','fox'],
                           ['brown','fox','in'], ['fox','in','the'],
                           ['in','the','pretty'],['the','pretty','woods']]
        trigrams         = solution.ngrams(input_tokens, 3)
        self.assertEqual(trigrams, correct_trigrams,
            "Test failed: test_ngrams got the wrong trigrams")

    def test_filter_stopword_bigrams(self):

        stopwords      = solution.load_stopwords("./mallet_en_stoplist.txt")
        input_bigrams  = [['the','pretty'], ['pretty','brown'], ['brown','fox'],
                          ['fox','in'], ['in','the'], ['the','pretty'],['pretty','woods']]
        output_bigrams = [['pretty','brown'], ['brown','fox'], ['pretty','woods']]
        filtered_bigrams = solution.filter_stopword_bigrams(input_bigrams, stopwords)
        self.assertCountEqual(filtered_bigrams, output_bigrams,
            "Test failed: test_filter_stopword_bigrams")

    def test_normalize_tokens(self):

        input           = 'I saw @psresnik\'s page at http://umiacs.umd.edu/~resnik/this_url'
        correct_output  = ['i', 'saw', "'s", 'page', 'at', 'http://umiacs.umd.edu/~resnik/this+url']
        nlp             = English(parser=False) # faster init with parse=False, if NP chunks are not needed
        spacy_analysis  = nlp(input)
        spacy_tokens    = [token.orth_ for token in spacy_analysis]
        normalized_toks = solution.normalize_tokens(spacy_tokens)
        self.assertListEqual(normalized_toks, correct_output,
            "Test failed: test_normalize_tokens")

    def test_get_unigram_counts(self):
        bigram_counter             = Counter({'a_b':2, 'a_c':1, 'b_c':1, 'c_d':1})
        correct_w1_unigram_counter = Counter({'a':3, 'b':1, 'c':1})
        correct_w2_unigram_counter = Counter({'b':2, 'c':2, 'd':1})
        w1_unigram_counter         = solution.get_unigram_counts(bigram_counter,0)
        w2_unigram_counter         = solution.get_unigram_counts(bigram_counter,1)
        self.assertEqual(correct_w1_unigram_counter, w1_unigram_counter,
            "Test failed: test_get_unigram_counts for w1 unigrams")
        self.assertEqual(correct_w2_unigram_counter, w2_unigram_counter,
            "Test failed: test_get_unigram_counts for w2 unigrams")

    def test_compute_pmi(self):
        bigram_counts     = Counter({'a_b': 5, 'a_c': 1, 'b_c': 1, 'c_d': 1})
        unigram_w1_counts = Counter({'a': 6, 'b': 1, 'c': 1})
        unigram_w2_counts = Counter({'b': 5, 'c': 2, 'd': 1})
        correct_pmi       = Counter({'c_d': 3.0, 'b_c': 2.0, 'a_b': 0.41503749927884376, 'a_c': -0.5849625007211563})
        pmi               = solution.compute_pmi(bigram_counts, unigram_w1_counts, unigram_w2_counts)
        self.assertAlmostEqual(correct_pmi['a_b'], pmi['a_b'], 3,
            "Test failed: test_compute_pmi got wrong value for bigram 'a_b': {}".format(pmi['a_b']))
        self.assertAlmostEqual(correct_pmi['c_d'], pmi['c_d'], 3,
            "Test failed: test_compute_pmi got wrong value for bigram 'c_d': {}".format(pmi['c_d']))

        
if __name__ == '__main__':
    unittest.main()
