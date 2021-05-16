from flask import Flask, jsonify, request
import time
import urllib.request
from urllib.request import Request, urlopen
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.corpus import wordnet 
from nltk.tokenize import PunktSentenceTokenizer
import en_core_web_sm
nlp = en_core_web_sm.load()




from bs4 import BeautifulSoup


app = Flask(__name__)
url_timestamp = {}
url_viewtime = {}
prev_url = ""
cleaned_sum = ""
synonyms = []



# global variables. Currently keeping track if time, but soon it'll keep track of text





def paraphraseable(tag):
 return tag.startswith('NN') or tag == 'VB' or tag.startswith('JJ')


def pos(tag):
 wordnet.ensure_loaded()
 if tag.startswith('NN'):
  return wordnet.NOUN
 elif tag.startswith('V'):
  return wordnet.VERB


def synonyms(word, tag):
    wordnet.ensure_loaded()
    lemma_lists = [ss.lemmas() for ss in wordnet.synsets(word, pos(tag))]
    lemmas = [lemma.name() for lemma in sum(lemma_lists, [])]
    return set(lemmas)



def synonymIfExists(sentence):
 
 for (word, t) in sentence:
         
   if paraphraseable(t):
    
    syns = synonyms(word, t)

    if syns:
     syns = list(syns)
     if len(syns) > 1:
      yield syns[0]
      print(syns[0])
      continue
   yield word



def paraphrase(sentence):
 return [x for x in synonymIfExists(sentence)]



def detokenize(sentence):
  result = ' '.join(sentence).replace(' , ',',').replace(' .','.').replace(' !','!')
  result = result.replace(' ?','?').replace(' : ',': ').replace(' \'', '\'')
  result = result.replace('_',' ')
  return result



@app.route('/paraphrase_summary', methods=['POST'])
def paraphrase_summary():
    resp_json = request.get_data()
    params = resp_json.decode()
    params = word_tokenize(params)
    params = pos_tag(params)

    final = bob = detokenize(paraphrase(params))


    print(final)
    
    return jsonify(str(final)), 200




@app.route('/get_data', methods = ['POST'])
def get_data():
    #for accepting user input for amount of sentences
    summary = "getting info"

    try: 
        resp_json = request.get_data()
        params = resp_json.decode()
        url = params.replace("url=", "")
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as req:
            s = req.read()

        soup = BeautifulSoup(s, 'html.parser')

        final_text = ""

        for data in soup.find_all("p"):
            sum = data.get_text()
            # I'm guessing this would output the html source code ?
            sum = re.sub(r'\[[0-9]*\]', ' ', sum)
            sum = re.sub(r'\s+', ' ', sum)
            final_text += sum
            #print(sum)


        # Removes special characters AS A COPY
        cleaned_text = re.sub('[^a-zA-Z]', ' ', final_text)
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)


        all_keywords = ""

        doc = nlp(cleaned_text)


        for X in doc.ents:
           print(X.text)
           all_keywords += str((X.text, X.label_)) + "%%%"

    except urllib.error.URLError as error:
            print('We failed to reach a server.')
            print('Reason: ', error.reason)
            return jsonify(error.reason), 200

    except urllib.error.HTTPError as error:
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', error.code)
            return jsonify(error.code), 200
    except ValueError as error:
            print(url)
            print("Cannot Read")
            print("but different now", summary)
            return jsonify("Error: Cannot Read"), 200
    except IndexError as error:
            return jsonify("Buffering"), 200

        
    return jsonify(all_keywords), 200





        
@app.route('/read_page', methods=['POST'])
def read_page():

    summary = "getting info"

    try: 
        resp_json = request.get_data()
        params = resp_json.decode()
        url = params.replace("url=", "")
        summarize_strength = url.split('s.p.l.i.t.t.e.r.4.5.1.9')[1]
        summarize_strength = int(summarize_strength)
        url = url.split('s.p.l.i.t.t.e.r.4.5.1.9')[0]
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



        print("using", summarize_strength, "sentences")

        summary_sentences = heapq.nlargest(summarize_strength, sentence_scores, key=sentence_scores.get)
        summary = ' '.join(summary_sentences)

        summary = summary.replace("“", "\"")

        summary = summary.replace("”", "\"")

        summary = summary.replace("’", "\'")


        # so javascript has like an aneurysm when trying to decipher smartquotes
        # like “” so I just deal with it here. Remember backslash doesnt show


        summcount = ('Approximate number of words: ' + str(number_of_words) +
                     'Estimated reading time of ' + str(round(number_of_words / 250))
                     + ' minutes' + summary)
        

    #-------------------------------------------stop deleting here

            

    except urllib.error.URLError as error:
            print('We failed to reach a server.')
            print('Reason: ', error.reason)
            return jsonify(error.reason), 200

    except urllib.error.HTTPError as error:
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', error.code)
            return jsonify(error.code), 200
    except ValueError as error:
            print(url)
            print("Cannot Read")
            print("but different now", summary)
            return jsonify("Error: Cannot Read"), 200
    except IndexError as error:
            return jsonify("Buffering"), 200


    # for some reason, without the try except the reader only reads like the
    # first sentence of a page. Maybe it forces to do it longer?



            
    return jsonify(summcount), 200

    


# DONT DELETE THIS, THIS IS WHAT ACTUALLY RUNS THE CODE. Easy to forget cause at bottom
app.run(host='0.0.0.0', port=5000)





