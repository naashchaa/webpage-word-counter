import requests
from bs4 import BeautifulSoup
import string

validcharacters = set(string.ascii_lowercase + string.ascii_uppercase)


#return html from url
def gethtml():
    #loop until a valid URL is given
    while True:
        try:
            url = input('Enter the URL: ')
            request = requests.get(url)
            return request.text
        except Exception as e:
            if 'Failed to establish a new connection' in str(e):
                print('Failed to establish a connection. Perhaps there is a typo in the URL?')
            elif 'No scheme supplied' in str(e):
                print('Invalid URL format. Did you mean http://' + url + '?')
            else:
                print(e)
        
                
#write html to file for troubleshooting
def writehtml(html):
    try:
        with open('html.txt', 'w', encoding='utf-8') as f:
            f.write(html)
    except Exception as e:
        print(e)


#return text from html
def parsehtmltext(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        return soup.get_text()
    except Exception as e:
        print(e)

#write text fetched from html to file for troubleshooting
def writehtmltext(text):
    try:
        with open('html_text.txt', 'w', encoding='utf-8') as f:
            f.write(text)
    except Exception as e:
        print(e)


#removes all invalid characters from one string
def makevalid(word):
    wordtofix = word
    wordtofix = wordtofix.replace('\'s', '')
    wordtofix = wordtofix.replace('\'ve', '')
    wordtofix = wordtofix.replace('n\'t', '')
    
    for char in wordtofix:
        if char not in validcharacters:
            wordtofix = wordtofix.replace(char, "")
    return wordtofix.lower()


#fixes all words in a word set
def fixallwords(wordset):
    fixedwords = wordset
    for i in range(len(fixedwords)):
        fixedwords[i] = makevalid(fixedwords[i])
    return fixedwords


#writes fixed words to a file for troubleshooting
def writefixedwords(fixedwordset):
    try:
        with open('html_text_filtered.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(fixedwordset))
    except Exception as e:
        print(e)


#puts all words into a dictionary,
#where the word is the key and frequency is the value
def hashwords(fixedwordset):
    worddict = {}
    for word in fixedwordset:
        if worddict.get(word):
            worddict[word] += 1
        else:
            worddict[word] = 1

    if '' in worddict:
        worddict.pop('')
    return worddict


#writes the frequency dictionary to a file for troubleshooting
def writedictionary(worddict):
    printabledict = worddict.items()

    try:   
        with open('html_text_filtered_wordcount.txt', 'w', encoding='utf-8') as f:
            for item in printabledict:
                f.write(str(item) + '\n')
    except Exception as e:
        print(e)


#searches the dictionary for the most frequently used word
def findmostfrequentword(worddict):
    frequent_word = ''
    frequent_number = -1
        
    for item in worddict:
            
        if (worddict[item] > frequent_number):
            frequent_word = item
            frequent_number = worddict[item]

    return frequent_word         


#main block of code
sitehtml = gethtml()
writehtml(sitehtml)

htmltext = parsehtmltext(sitehtml)
#writehtmltext(htmltext)

wordset = htmltext.split()

fixedwordset = fixallwords(wordset)
#writefixedwords(fixedwordset)

worddict = hashwords(fixedwordset)
#writedictionary(worddict)

mostfrequentword = findmostfrequentword(worddict)
print('\n')
print('most frequent word is \"' + mostfrequentword +
      '\" with ' + str(worddict[mostfrequentword]) + ' occurences.')
   
    
