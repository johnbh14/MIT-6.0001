# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
        
    def get_guid(self):
        return self.guid
    
    def get_title(self):
        return self.title
    
    def get_description(self):
        return self.description
    
    def get_link(self):
        return self.link
    
    def get_pubdate(self):
        return self.pubdate


#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase.lower()
       
    def is_phrase_in(self, text):
        text = text.lower()
        replace_characters = "!@#$%^&*()-_+={}[]|\:;'<>?,./\""
        for character in replace_characters:
            text = text.replace(character, ' ')
        text = text.split()
        words_in_phrase = self.phrase.split()
        for word in words_in_phrase:
            if not word in text:
                return False
        first_word_in_phrase = words_in_phrase[0]
        start_point = text.index(first_word_in_phrase)
        phrase_index = 0
        for i in range(start_point, start_point + len(words_in_phrase)):
            try:
                #print('text = ' + text[i] + ' phrase = ' + words_in_phrase[phrase_index])
                if not words_in_phrase[phrase_index] == text[i]:
                    return False
            except IndexError:
                return False
            phrase_index += 1
        return True
        

# Problem 3
class TitleTrigger(PhraseTrigger):
    
    def evaluate(self, story):
        return PhraseTrigger.is_phrase_in(self, story.get_title())

# Problem 4
class DescriptionTrigger(PhraseTrigger):
    def evaluate(self, story):
        return PhraseTrigger.is_phrase_in(self, story.get_description())

# TIME TRIGGERS

# Problem 5
class TimeTrigger(Trigger):
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
    def __init__(self, time):
        self.time = datetime.strptime(time, "%d %b %Y %H:%M:%S").replace(tzinfo=pytz.timezone("EST"))

# Problem 6
class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        if story.get_pubdate().replace(tzinfo=None) < self.time.replace(tzinfo=None):
            return True
        else:
            return False

class AfterTrigger(TimeTrigger):
    def evaluate(self, story):
        if story.get_pubdate().replace(tzinfo=None) > self.time.replace(tzinfo=None):
            return True
        else:
            return False

# COMPOSITE TRIGGERS

# Problem 7
class NotTrigger(Trigger):
    def __init__(self, other_trigger):
        self.other_trigger = other_trigger

    def evaluate(self, story):
        return not self.other_trigger.evaluate(story)

# Problem 8
class AndTrigger(Trigger):
    def __init__(self, first_trigger, second_trigger):
        self.first_trigger = first_trigger
        self.second_trigger = second_trigger

    def evaluate(self, story):
        return self.first_trigger.evaluate(story) and self.second_trigger.evaluate(story)

# Problem 9
class OrTrigger(Trigger):
    def __init__(self, first_trigger, second_trigger):
        self.first_trigger = first_trigger
        self.second_trigger = second_trigger

    def evaluate(self, story):
        return self.first_trigger.evaluate(story) or self.second_trigger.evaluate(story)
 


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    triggered_stories = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                triggered_stories.append(story)
    return triggered_stories



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)
    print('HERE')
    for line in lines:
        #TITLE​ : one phrase
        #DESCRIPTION​ : one phrase
        #AFTER​ : one correctly formatted time string
        #BEFORE​ : one correctly formatted time string
        #NOT​ : the name of the trigger that will be NOT
        #AND​ : the names of the two triggers that will be AND
        #OR​ : the names of the two triggers that will be OR
        line = line.split(',')
        trigger_list = []
        if line[0] == 'ADD':
            for element in line[1:]:
                exec('trigger_list.append(' + element + ')')
        if line[1] == 'TITLE':
            exec(line[0] + ' = TitleTrigger("' + line[2] + '")')
        if line[1] == 'DESCRIPTION':
            exec(line[0] + ' = DescriptionTrigger("' + line[2] + '")')
        if line[1] == 'AFTER':
            exec(line[0] + ' = AfterTrigger("' + line[2] + '")')
        if line[1] == 'BEFORE':
            exec(line[0] + ' = BeforeTrigger("' + line[2] + '")')
        if line[1] == 'NOT':
            exec(line[0] + ' = NotTrigger(' + line[2] + ')')
        if line[1] == 'AND':
            exec(line[0] + ' = AndTrigger(' + line[2] + ', ' + line[3] + ')')
        if line[1] == 'OR':
            exec(line[0] + ' = OrTrigger(' + line[2] + ', ' + line[3] + ')')
    return trigger_list



SLEEPTIME = 2 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("coronavirus")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("US")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        triggerlist = read_trigger_config('triggers.txt')

        print('Active Triggers = ' + str(triggerlist))
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            #for story in stories:
            #    print(story.get_description())
            
            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

