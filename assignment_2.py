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



#main code
def main():
    wikipedia = MediaWiki()

    #intro so user understands what is happening
    print("Hi! Please enter two Wikipedia pages that you would like to compare, for example bananas and apples.")

#get first page from user
#create a loop so user can re-enter a wiki page if there first choice does not exsist
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
            print("Invalid entry. Try again")
            continue

        if (page2.title != ""):
            done = True
        else:
            print("No page found, please try again")


#to get the number of times a word is on a page
    print(f"There are {len(page1.content)} words on the {wiki1} Wikipedia page")
    print(f"There are {len(page2.content)} words on the {wiki2} Wikipedia page")

#to get the number of times the title(there entry) appears on a page
    h1 = word_frequencies(page1.content)
    h2 = word_frequencies(page2.content)

    print(f"The number of times {wiki1} appears on its page is {h1[wiki1]}")
    print(f"The number of times {wiki2} appears on its page is {h2[wiki2]}")

#compare the two wikipages based on the fuzz ratio
    print(f"The Fuzz Ratio between {wiki1} and {wiki2} is {fuzz.ratio(page1.content, page2.content)}")


if __name__ == "__main__":
    main()
