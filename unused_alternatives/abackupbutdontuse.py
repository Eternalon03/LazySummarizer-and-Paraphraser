from flask import Flask, jsonify, request
import time
import urllib.request
from urllib.request import Request, urlopen
import re
import nltk
from nltk.stem import PorterStemmer
ps = PorterStemmer()
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.corpus import conll2000, conll2002
from nltk.tokenize import PunktSentenceTokenizer




from bs4 import BeautifulSoup


app = Flask(__name__)
url_timestamp = {}
url_viewtime = {}
prev_url = ""
cleaned_sum = ""
synonyms = []



#url = "https://calgaryherald.com/news/local-news/albertas-active-case-rate-is-more-than-twice-the-canadian-average-how-did-the-provinces-third-wave-get-so-bad"

# global variables. Currently keeping track if time, but soon it'll keep track of text




@app.route('/send_url', methods=['POST'])
def send_url():
    resp_json = request.get_data()
    params = resp_json.decode()
    url = params.replace("url=", "")
    print("currently viewing: " + url)


    global url_timestamp
    global url_viewtime
    global prev_url

    print("initial db prev tab: ", prev_url)
    print("initial db timestamp: ", url_timestamp)
    print("initial db viewtime: ", url_viewtime)



    if prev_url != '':
        time_spent = int(time.time() - url_timestamp[prev_url])
        url_viewtime[prev_url] = url_viewtime[prev_url] + time_spent

    x = int(time.time())

    print("final timestamps: ", url_timestamp)
    print("final viewtimes: ", url_viewtime)

    return jsonify({'message': 'success!'}), 200


@app.route('/quit_url', methods=['POST'])
def quit_url():
    resp_json = request.get_data()
    print("Url closed: " + resp_json.decode())
    return jsonify({'message': 'quit success!'}), 200




class BigramChunker(nltk.ChunkParserI):
        def __init__(self, train_sents): 
          train_data = [[(t,c) for w,t,c in nltk.chunk.tree2conlltags(sent)]
                      for sent in train_sents]
          self.tagger = nltk.BigramTagger(train_data) 

        def parse(self, sentence): 
          pos_tags = [pos for (word,pos) in sentence]
          tagged_pos_tags = self.tagger.tag(pos_tags)
          chunktags = [chunktag for (pos, chunktag) in tagged_pos_tags]
          conlltags = [(word, pos, chunktag) for ((word,pos),chunktag)
                     in zip(sentence, chunktags)]
          return nltk.chunk.conlltags2tree(conlltags)


@app.route('/read_page', methods=['POST'])
def read_page():

    try: 
        resp_json = request.get_data()
        params = resp_json.decode()
        url = params.replace("url=", "")
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as req:
            s = req.read()

    # the Request thing gets past some of the annoying web scraper detectors
    # by pretending to be something else (User-Agent)
    # this isn't illegal right?


        soup = BeautifulSoup(s, 'html.parser')

        final_text = ""

        for data in soup.find_all("p"):
            sum = data.get_text()
            # I'm guessing this would output the html source code ?
            sum = re.sub(r'\[[0-9]*\]', ' ', sum)
            sum = re.sub(r'\s+', ' ', sum)
            final_text += sum
            #print(sum)

    # FROM HERE BEFORE THIS, THIS PROGRAM JUST TAKES AND READ TEXT FROM ANY PAGE
    # FROM HERE ON OUT, THIS IS WHERE THE ACTUAL PARAPHRASING IS
    # IF YOU WOULD LIKE TO DOWNLOAD THIS AND USE IT FOR SOMETHING ELSE, DELETE
    # EVERYTHING AFTER THIS BESIDES THE (return jsonify...) AND (app.run...)


        #print(final_text)
        # Removes special characters AS A COPY
        cleaned_text = re.sub('[^a-zA-Z]', ' ', final_text)
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)

        #wordcount
        words_read = final_text.split()
        number_of_words = len(words_read)
        print('Approximate number of words:', number_of_words)
        print('Estimated reading time', round(number_of_words / 250), 'minutes')

        #tokenize (sentences)
        sentence_list = nltk.sent_tokenize(final_text)

        stopwords = nltk.corpus.stopwords.words('english')

        word_frequencies = {}
        for word in nltk.word_tokenize(cleaned_text):
          if word not in stopwords:
            if word not in word_frequencies.keys():
              word_frequencies[word] = 1
            else:
              word_frequencies[word] += 1

        maximum_frequncy = max(word_frequencies.values())

        for word in word_frequencies.keys():
          word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)


        sentence_scores = {}
        for sent in sentence_list:
           for word in nltk.word_tokenize(sent.lower()):
              if word in word_frequencies.keys():
                 if len(sent.split(' ')) < 30:
                   if sent not in sentence_scores.keys():
                     sentence_scores[sent] = word_frequencies[word]
                   else:
                     sentence_scores[sent] += word_frequencies[word]


        import heapq

        summarize_strength = input("How many sentences would you like to use: ")
        summarize_strength = int(summarize_strength)

        summary_sentences = heapq.nlargest(summarize_strength, sentence_scores, key=sentence_scores.get)
        summary = ' '.join(summary_sentences)
        print(summary)


        #stem what was summarized/normalize words

        lemmatizer = WordNetLemmatizer()
        summary = lemmatizer.lemmatize(summary)

        sentence = re.sub('[^a-zA-Z]', ' ', summary)
        sentence = re.sub(r'\s+', ' ', sentence)
        sentence = nltk.word_tokenize(sentence)


        # here


        train_text = conll2000.raw("train.txt")
        sample_text = summary

        custom_sent_tokenizer = PunktSentenceTokenizer(train_text)

        tokenized = custom_sent_tokenizer.tokenize(sample_text)

        tokenized_sents = [word_tokenize(i) for i in tokenized]



        try:
          for i in tokenized:
            words = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(words)
            chunkGram = r"""Chunk: {<RB.?>*<VB.?>*<NNP>+<NN>?}"""
            chunkParser = nltk.RegexpParser(chunkGram)
            chunked = chunkParser.parse(tagged)
            
            print(chunked)


        except Exception as e:
          print(str(e))

        #train_sents = conll2000.chunked_sents(train_text, chunk_types=['NP'])
        #test_sents = conll2000.chunked_sents(sample_text, chunk_types=['NP'])
        #bigram_chunker = BigramChunker(train_sents)

        print("spacer")

        #sent = nltk.corpus.treebank.tagged_sents()
        #print(nltk.ne_chunk(sent, binary=True))
 

       

    
	
	    







    #-------------------------------------------stop deleting here

            

    except urllib.error.URLError as error:
            print('We failed to reach a server.')
            print('Reason: ', error.reason)

    except urllib.error.HTTPError as error:
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', error.code)
    except ValueError as error:
            print("Cannot Read")


    # for some reason, without the try except the reader only reads like the
    # first sentence of a page. Maybe it forces to do it longer?



            
    return jsonify({'message': 'read success!'}), 200

    




# DONT DELETE THIS, THIS IS WHAT ACTUALLY RUNS THE CODE. I DUNNO HOW THIS
# GOT DELETED THE FIRST TIME

app.run(host='0.0.0.0', port=5000)
