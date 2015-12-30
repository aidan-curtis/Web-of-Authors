from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium import webdriver
import bibtexparser
import os
import re
import json
import argparse


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class PaperData:
    author = ''
    paper = ''
    universities = ''
    parentId = ''
    year = ''
    citedReferences = ''
    timesCited = ''

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def __init__(self, universities, parentId, author, paper, year, citedReferences, timesCited):
        self.citedReferences = citedReferences
        self.universities = universities
        self.year = year
        self.timesCited = str(timesCited)
        self.paper = paper
        if parentId == None:
            self.parentId = None
        else:
            self.parentId = parentId
        self.author = author
    def getTimesCited(self):
        return self.timesCited
    def getAuthor(self):
        return self.author
    def getYear(self):
        return self.year
    def getPaper(self):
        return self.paper

    def getUniversities(self):
        return self.universities

    def __str__(self):
        final_string = "---------PAGE------------\n"
        final_string += "Paper Name: " + self.paper + "\n"
        final_string += "Paper Authors:" + self.author + "\n"
        if (self.universities):
            final_string += "Research Location: " + ', ' + self.universities + "\n"
        final_string += "Who does it cite?\n"
        if (self.citedReferences):
            final_string += self.citedReferences
        final_string += "Year published: " + self.year + "\n"
        final_string += "Times Cited: " + str(self.timesCited) + "\n"
        if self.parentId != None:
            final_string += "Parent Node Identification: " + str(self.parentId) + "\n"
        else:
            final_string += "Parent Node Identification: Root Node\n"
        final_string += "----------END-------------\n"
        return final_string


def timesCited(entry):
    times_cited = ''
    try:
        times_cited = str(entry['times-cited'])

    except KeyError:
        return None
    return times_cited


def downloadFromList(driver, FROM, TO):
    selector2 = driver.find_element_by_xpath("//select[@name='saveToMenu']")
    options_for_second_selector = selector2.find_elements_by_tag_name("option")
    for option in options_for_second_selector:
        if (option.get_attribute('value') == 'other'):
            option.click()
            break

    radio_element = driver.find_element_by_name("value(record_select_type)")
    radio_element.click()

    from_element = driver.find_element_by_id("markFrom")
    from_element.send_keys(str(FROM))

    to_element = driver.find_element_by_id("markTo")
    to_element.send_keys(str(TO))

    select = Select(driver.find_element_by_id('bib_fields'))
    select.select_by_index(3)

    select = Select(driver.find_element_by_id('saveOptions'))
    select.select_by_index(1)

    thing = driver.find_element_by_class_name("quickoutput-action")
    thing.click()

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'send'))
    )

    exitbutton = driver.find_element_by_class_name("quickoutput-cancel-action")
    exitbutton.click()


def find_university(entry):
    try:
        full_string = str(entry['affiliation']).lower()
    except KeyError:
        try:
            full_string = str(entry['Affiliation']).lower()
        except KeyError:
            return None

    full_list = full_string.split(", ")
    new_b = None
    done = False
    for aff in full_list:
        sub_list = aff.split(".\n")
        for b in sub_list:
            if ("univ" in b or "corp" in b or "coll" in b or "acad" in b or "inst" in b or " inc" in b or " llc" in b):
                return b


def find_authors(entry):
    try:
        full_string = str(entry['Author'])
    except KeyError:
        try:
            full_string = str(entry['author'])
        except KeyError:
            return None
    return full_string.replace(" and ", ";")


def find_year(entry):
    try:
        full_string = str(entry['Year'])
    except KeyError:
        try:
            full_string = str(entry['year'])
        except KeyError:
            return None
    return full_string


def find_title(entry):
    try:
        full_string = str(entry['title'])
    except KeyError:
        try:
            full_string = str(entry['Title'])
        except KeyError:
            return None
    return full_string


def bibtex_parsing(fileName, parent):
    list_of_instances = []
    with open(fileName) as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
        for entry in bib_database.entries:
            list_of_instances.append(
                PaperData(find_university(entry), parent, find_authors(entry), find_title(entry), find_year(entry),
                          get_cited_references(entry), timesCited(entry)))
    return list_of_instances

def pickleUpdateWithList(thelist, fileName):
    file=open(fileName, 'a')

    for a in thelist:
        if(os.stat(fileName).st_size == 0):
            file.write("[")
        else:
            file.write(",")
        file.write(a.to_JSON());

    file.close()


def store_data(fileNameToAppend, desiredLocation, parent):
    list_of_indexes = bibtex_parsing(fileNameToAppend, parent)
    pickleUpdateWithList(list_of_indexes, desiredLocation)
    


def removeFile(path):
    try:
        os.remove(path)
    except:
        print "no path to remove"


def error_filter(path, destination, parent, driver, start, end):
    print start, end
    removeFile(path)
    downloadFromList(driver, str(start), str(end))
    time.sleep(3)
    try:
        store_data(path, destination, parent)
    except:
        if (end - start > 10):
            error_filter(path, destination, parent, driver, start, start + int((end - start) / 2))
            error_filter(path, destination, parent, driver, start + int((end - start) / 2), end)


def grab_data(driver, parent, destination):
    number_of_files = int(get_number_of_files(driver))
    number_of_pages = float(float(number_of_files) / 500.0)
    if int(number_of_pages) != number_of_pages:
        number_of_pages += 1
    print "Number of pages"+str(int(number_of_pages))
    number_of_pages = int(number_of_pages)
    for i in range(0, number_of_pages):
        print "Retrieving ~500 Files...",
        time.sleep(2)
        if (number_of_files >= 500 + (500 * i)):
            downloadFromList(driver, str(1 + (500 * i)), str(500 + (500 * i)))
        if (number_of_files < 500 + (500 * i)):
            downloadFromList(driver, str(1 + (500 * i)), str(number_of_files))
        print bcolors.OKBLUE + "Files Retrieved" + bcolors.ENDC,
        time.sleep(3)
        path = "/Users/aidancurtis/Downloads/savedrecs.bib"
        try:
            store_data(path, destination, parent)
        except:
            print bcolors.FAIL + "500 files discarded" + bcolors.ENDC
            if (number_of_files >= 500 + (500 * i)):
                removeFile(path)
                error_filter(path, destination, parent, driver, 1 + (500 * i), 500 + (500 * i))
            if (number_of_files < 500 + (500 * i)):
                removeFile(path)
                error_filter(path, destination, parent, driver, 1 + (500 * i), number_of_files)

        removeFile(path)
        print bcolors.OKGREEN + "Files Stored" + bcolors.ENDC

    
def get_number_of_files(driver):
    return driver.find_element_by_xpath("//span[@id='hitCount.top']").text.replace(',', '')


def get_cited_references(entry):
    long_string = ''
    try:
        long_string = entry['Cited-References']
    except:
        try:
            long_string = entry['cited-references']
        except:
            return None
    
    return long_string
if __name__ == '__main__':

    
    parser = argparse.ArgumentParser(description='Process some strings')
    parser.add_argument('URL', metavar='N', nargs='+',help='URL from web of science')
    parser.add_argument('FILE', metavar='N', nargs='+',help='a destination file')
    destination= parser.parse_args().FILE[0]
    theURL=parser.parse_args().URL[0]
    
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get(theURL)
    grab_data(driver, None, destination)
        
    driver.quit()     
    file=open(destination, 'a')
    file.write("]")
    file.close()
            
            
