"""
user puts in 2 wiki pages
text similarity btwn two wiki pages to compare
text clustering or word frequency

input wiki pages
    assign names: wiki1 and wiki2





    hist = {}
    fp = open(wiki1)

    if skip_header:
        skip_wiki1(fp)

    strippables = string.punctuation + string.whitespace

    for line in fp:
        if line.startswith('SEE ALSO'):
            break

        line = line.replace('-', ' ')

        for word in line.split():
            # word could be 'Sussex.'
            word = word.strip(strippables)
            word = word.lower()

            # update the dictionary
            hist[word] = hist.get(word, 0) + 1

    return hist


for each page-
    create a dict
        keys = words
        value = frequency

count = 0
for frequency in different_words not in excluding_stopwords:
    count += 1
return list(frequency, WORD)


"""
from ctypes.wintypes import WORD
import random
import string
from mediawiki import MediaWiki
from thefuzz import fuzz
from thefuzz import process
from flask import Flask, escape
from nltk.sentiment.vader import SentimentIntensityAnalyzer


#generate hist to find words on wiki page
def word_frequencies(page):
    hist = {} #create dict

    #filter the words to become more readable
    strippables = string.punctuation + string.whitespace
    page = page.replace('-', ' ')

#decided against stopping the dict from taking words at a certain point

    for word in page.split():
        # word could be 'apple.'
        word = word.strip(strippables)
        word = word.lower()

        # update the dictionary
        hist[word] = hist.get(word, 0) + 1

    return hist



#users enter wiki pages
def user_inputs():
    wikipedia = MediaWiki()

    #intro so user understands what is happening
    print("Hi! Please enter two Wikipedia pages that you would like to compare, for example bananas and apples.")


    #create a loop so user can re-enter a wiki page if there first choice does not exsist
    #get first page from user
    done = False
    while done == False:
        try:
            wiki1 = input("Enter first page: ")
            page1 = wikipedia.page(wiki1)
        except:
            print("Invalid entry. Try again")
            continue

        if (page1.title != ""):
            done = True
        else:
            print("No page found, please try again")
            
    #loop for second page
    done = False
    while done == False:
        try:
            wiki2 = input("Enter second page: ")
            page2 = wikipedia.page(wiki2)
        except:
            print("Invalid entry or may not be recgonized in MediaWiki. Try again")
            continue

        if (page2.title != ""):
            done = True
        else:
            print("No page found, please try again")
    
    return wiki1, wiki2, page1, page2, wikipedia



app = Flask(__name__)



@app.route("/")
def webpage(name=None):
    wiki1, wiki2, page1, page2, wikipedia = user_inputs()

    if wikipedia:
        #to get the number of times a word is on a page
        #return render_template('index.html')
        yield(f"<h1> The comparison between the {escape(wiki1)} Wikipedia page and the {escape(wiki2)} Wikipedia page: <h1>")
        yield(f"<h1> There are {escape(len(page1.content))} words on the {escape(wiki1)} Wikipedia page. <h1>")
        yield(f"<h1> There are {len(escape(page2.content))} words on the {escape(wiki2)} Wikipedia page. <h1>")

        #to get the number of times the title(there entry) appears on a page
        h1 = word_frequencies(page1.content)
        h2 = word_frequencies(page2.content)

        yield(f"<h1> The number of times {escape(wiki1)} appears on its page is {escape(h1[wiki1])}. <h1>")
        yield(f"<h1> The number of times {escape(wiki2)} appears on its page is {escape(h2[wiki2])}. <h1>")

        #compare the two wikipages based on the fuzz ratio
        yield(f"<h1> The Fuzz Ratio between {escape(wiki1)} and {escape(wiki2)} is {escape(fuzz.ratio(page1.content, page2.content))}. <h1>")

        #to get  the Natural Langauge processor
        score = SentimentIntensityAnalyzer().polarity_scores(escape(page1.content))
        score1 = SentimentIntensityAnalyzer().polarity_scores(escape(page2.content))

        yield(f"<h1> The Natural Language Processor Score for the {wiki1} page is {score}. <h1>")
        yield(f"<h1> The Natural Language Processor Score for the {wiki2} page is {score1}. <h1>")

    else:
        #incase there is a mistake
        return "<h1>Hello, World</h1> <p>There is an error</p>"


if __name__ == "__main__":
    app.run(port=5001, debug=True)