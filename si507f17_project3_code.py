from bs4 import BeautifulSoup
import unittest
import requests
from unidecode import unidecode
import csv

#########
## Instr note: the outline comments will stay as suggestions, otherwise it's too difficult.
## Of course, it could be structured in an easier/neater way, and if a student decides to commit to that, that is OK.

## NOTE OF ADVICE:
## When you go to make your GitHub milestones, think pretty seriously about all the different parts and their requirements, and what you need to understand. Make sure you've asked your questions about Part 2 as much as you need to before Fall Break!


######### PART 0 #########

# Write your code for Part 0 here.
try:
    ntdata = open("newtay.html", 'r').read()
except:
    ntdata = requests.get("http://newmantaylor.com/gallery.html").text
    with open("newtay.html", 'w') as f:
        f.write(ntdata)

soup = BeautifulSoup(ntdata, 'html.parser')
img_elems = soup.find_all('img')

for ele in img_elems :
    if len(ele.get('alt', '')) > 0:
        print (ele.get('alt', ''))
    else:
        print ("No alt text")



######### PART 1 #########

# Get the main page data...

# Try to get and cache main page data if not yet cached
# Result of a following try/except block should be that
# there exists a file nps_gov_data.html,
# and the html text saved in it is stored in a variable
# that the rest of the program can access.

# We've provided comments to guide you through the complex try/except, but if you prefer to build up the code to do this scraping and caching yourself, that is OK.






# Get individual states' data...

# Result of a following try/except block should be that
# there exist 3 files -- arkansas_data.html, california_data.html, michigan_data.html
# and the HTML-formatted text stored in each one is available
# in a variable or data structure
# that the rest of the program can access.

# TRY:
# To open and read all 3 of the files

# But if you can't, EXCEPT:

# Create a BeautifulSoup instance of main page data
# Access the unordered list with the states' dropdown

# Get a list of all the li (list elements) from the unordered list, using the BeautifulSoup find_all method

# Use a list comprehension or accumulation to get all of the 'href' attributes of the 'a' tag objects in each li, instead of the full li objects

# Filter the list of relative URLs you just got to include only the 3 you want: AR's, CA's, MI's, using the accumulator pattern & conditional statements


# Create 3 URLs to access data from by appending those 3 href values to the main part of the NPS url. Save each URL in a variable.


## To figure out what URLs you want to get data from (as if you weren't told initially)...
# As seen if you debug on the actual site. e.g. Maine parks URL is "http://www.nps.gov/state/me/index.htm", Michigan's is "http://www.nps.gov/state/mi/index.htm" -- so if you compare that to the values in those href attributes you just got... how can you build the full URLs?


# Finally, get the HTML data from each of these URLs, and save it in the variables you used in the try clause
# (Make sure they're the same variables you used in the try clause! Otherwise, all this code will run every time you run the program!)


# And then, write each set of data to a file so this won't have to run again.

base_url = 'https://www.nps.gov'

try:
    mpdata = open("nps_gov_data.html", 'r').read()

except:
    mpdata = requests.get("https://www.nps.gov/index.htm").text
    f = open("nps_gov_data.html", 'w')
    f.write(unidecode(mpdata))
    f.close()

try:
    ardata = open('arkansas_data.html', 'r').read()
    midata = open('michigan_data.html', 'r').read()
    cadata = open('california_data.html', 'r').read()

except:
    sp = BeautifulSoup(mpdata, 'html.parser')
    state_ul = sp.find_all('ul')
    state_a = state_ul[2].find_all('a')
    for e in state_a:
        if 'ar' in e['href']:
            f = open ('arkansas_data.html', 'w')
            ar_link = base_url+e['href']
            ardata = requests.get(ar_link).text
            f.write(ardata)
            f.close()
        elif 'ca' in e['href']:
            f = open ('california_data.html', 'w')
            ca_link = base_url+e['href']
            cadata = requests.get(ca_link).text
            f.write(cadata)
            f.close()
        elif 'mi' in e['href']:
            f = open ('michigan_data.html', 'w')
            mi_link = base_url+e['href']
            midata = requests.get(mi_link).text
            f.write(midata)
            f.close()


######### PART 2 #########
# Before truly embarking on Part 2, we recommend you do a few things:
# - Create BeautifulSoup objects out of all the data you have access to in variables from Part 1
# - Do some investigation on those BeautifulSoup objects. What data do you have about each state? How is it organized in HTML?
# HINT: remember the method .prettify() on a BeautifulSoup object -- might be useful for your investigation! So, of course, might be .find or .find_all, etc...
# HINT: Remember that the data you saved is data that includes ALL of the parks/sites/etc in a certain state, but you want the class to represent just ONE park/site/monument/lakeshore.
# We have provided, in sample_html_of_park.html an HTML file that represents the HTML about 1 park. However, your code should rely upon HTML data about Michigan, Arkansas, and Califoria you saved and accessed in Part 1.
# However, to begin your investigation and begin to plan your class definition, you may want to open this file and create a BeautifulSoup instance of it to do investigation on.
# Remember that there are things you'll have to be careful about listed in the instructions -- e.g. if no type of park/site/monument is listed in input, one of your instance variables should have a None value...
# Define your class NationalSite here:

class NationalSite(object):
    """docstring for NationalSite."""
    def __init__(self, site_html):
        self.location = site_html.find('h4').text
        self.name = site_html.find('a').text
        try:
            self.type = site_html.find('h2').text
        except :
            self.type = None
        try:
            self.description = site_html.find('p').text
        except :
            self.description = ''
        for ele in site_html.find_all('a'):
            if 'basicinfo' in ele['href']:
                self.binfo_url = ele['href']
        self.addr = ''

    def __str__(self):
        return "{} | {}".format(self.name, self.location)

    def get_mailing_address(self):
        binfo = requests.get(self.binfo_url).text
        binfo_soup = BeautifulSoup(binfo, 'html.parser')
        try:
            staddr = binfo_soup.find_all('span', {"itemprop":"streetAddress"})[0].text
        except:
            staddr = "P.O. Box"+binfo_soup.find_all('span', {"itemprop":"postOfficeBoxNumber"})[0].text
        zcode = binfo_soup.find_all('span', {"itemprop":"postalCode"})[0].text
        loc = binfo_soup.find_all('span', {"itemprop":"addressLocality"})[0].text
        reg = binfo_soup.find_all('span', {"itemprop":"addressRegion"})[0].text
        addr = staddr.rstrip()+'/'+loc+'/'+reg+'/'+zcode
        return addr

    def __contains__(self, inp):
        return inp in self.name
## Recommendation: to test the class, at various points, uncomment the following code and invoke some of the methods / check out the instance variables of the test instance saved in the variable sample_inst:
#f = open("sample_html_of_park.html",'r')
#soup_park_inst = BeautifulSoup(f.read(), 'html.parser') # an example of 1 BeautifulSoup instance to pass into your class
#sample_inst = NationalSite(soup_park_inst)
#print (sample_inst)
#f.close()


######### PART 3 #########

# Create lists of NationalSite objects for each state's parks.

# HINT: Get a Python list of all the HTML BeautifulSoup instances that represent each park, for each state.

mi_html = BeautifulSoup(midata, 'html.parser')
ar_html = BeautifulSoup(ardata, 'html.parser')
ca_html = BeautifulSoup(cadata, 'html.parser')
mi_raw_sites = mi_html.find_all(id='list_parks')
ar_raw_sites = ar_html.find_all(id='list_parks')
ca_raw_sites = ca_html.find_all(id='list_parks')
california_natl_sites = []
arkansas_natl_sites = []
michigan_natl_sites = []
for e in mi_raw_sites[0]:
    try:
        new_site = NationalSite(e)
        michigan_natl_sites.append(new_site)
    except :
        pass
for e in ar_raw_sites[0]:
    try:
        new_site = NationalSite(e)
        arkansas_natl_sites.append(new_site)
    except :
        pass

for e in ca_raw_sites[0]:
    try:
        new_site = NationalSite(e)
        california_natl_sites.append(new_site)
    except :
        pass
#Code to help you test these out:
#for p in california_natl_sites:
#    print(p.name)
#for a in arkansas_natl_sites:
#    print(a)
#for m in michigan_natl_sites:
#    print(m)

with open ('arkansas.csv', 'w') as f:
    arwriter = csv.writer(f)
    arwriter.writerow(("Name", "Location", "Type", "Address", "Description"))
    for e in arkansas_natl_sites:
        if e.type == None:
            typ = "None"
        else:
            typ = e.type
        arwriter.writerow((e.name, e.location, typ, e.get_mailing_address().strip(), e.description.strip()))

with open ('michigan.csv', 'w') as f:
    miwriter = csv.writer(f)
    miwriter.writerow(("Name", "Location", "Type", "Address", "Description"))
    for e in michigan_natl_sites:
        if e.type == None:
            typ = "None"
        else:
            typ = e.type
        miwriter.writerow((e.name, e.location, typ, e.get_mailing_address().strip(), e.description.strip()))


with open ('california.csv', 'w') as f:
    cawriter = csv.writer(f)
    cawriter.writerow(("Name", "Location", "Type", "Address", "Description"))
    for e in california_natl_sites:
        if e.type == None:
            typ = "None"
        else:
            typ = e.type
        cawriter.writerow((e.name, e.location, typ, e.get_mailing_address().strip(), e.description.strip()))

######### PART 4 #########

## Remember the hints / things you learned from Project 2 about writing CSV files from lists of objects!

## Note that running this step for ALL your data make take a minute or few to run -- so it's a good idea to test any methods/functions you write with just a little bit of data, so running the program will take less time!

## Also remember that IF you have None values that may occur, you might run into some problems and have to debug for where you need to put in some None value / error handling!
