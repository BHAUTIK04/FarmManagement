from BeautifulSoup import BeautifulSoup
import urllib
import os
import json
import csv
import sys

dir_path = sys.argv[1]

if os.path.exists(dir_path):
    pass
else:
    os.mkdir(dir_path)

base_url = "http://www.agriculture.gov.au"
paste_url = "http://www.agriculture.gov.au/pests-diseases-weeds/plant"
main_page_data = urllib.urlopen(paste_url)
soup_obj = BeautifulSoup(main_page_data)
list_pest = soup_obj.find("ul",{"class":"flex-container"})
dict_pest = {}
print "Got page data"
for i in list_pest.findAll("li"):
    dict_pest[i.find("a").getText()] = {}
    dict_pest[i.find("a").getText()]["name"] = i.find("a").getText().strip().encode('utf-8')
    _url = i.find("a")["href"]
    dict_pest[i.find("a").getText()]["url"] = i.find("a")["href"]
    image_name = i.find("img")["src"].split("/")[-1]
    urllib.urlretrieve(base_url+i.find("img")["src"], dir_path+image_name)
    dict_pest[i.find("a").getText()]["img"] = dir_path+image_name


print "available pests {}".format(dict_pest)
for i in dict_pest:
    if dict_pest[i]["url"].startswith("/"):
        _url = base_url + dict_pest[i]["url"]
        dict_pest[i]["url"] = _url
        pest_page_data = urllib.urlopen(_url)
        soup = BeautifulSoup(pest_page_data)
        if soup.find("div",{"class":"pest-header-content"}):
            dict_pest[i]["origin"] = soup.find("div",{"class":"pest-header-content"}).findAll("strong")[1].nextSibling.strip()
        else:
            dict_pest[i]["origin"] = ""
        if soup.findAll('h3', {"class":"trigger"}):
            for j in soup.findAll('h3', {"class":"trigger"}):
                if j.getText() == "Check what can legally come into Australia":
                    dict_pest[i][j.getText()] = j.nextSibling.getText().encode('utf-8')
                elif j.getText() == "Secure any suspect specimens":
                    dict_pest[i][j.getText()] = j.nextSibling.getText().encode('utf-8')
                elif j.getText() == "See if you can identify the pest":
                    dict_pest[i][j.getText()] = j.nextSibling.getText().encode('utf-8')
                else:
                    dict_pest[i]["Check what can legally come into Australia"] = ""
                    dict_pest[i]["Secure any suspect specimens"] = ""
                    dict_pest[i]["See if you can identify the pest"] = ""

    else:
        dict_pest[i]["origin"] = ""
        dict_pest[i]["Check what can legally come into Australia"] = ""
        dict_pest[i]["Secure any suspect specimens"] = ""
        dict_pest[i]["See if you can identify the pest"] = ""
        # _url = dict_pest[i]["url"]

dicts = dict_pest.values()
headers = dicts[0].keys()
print json.dumps(dicts)
with open(dir_path+'pests.csv', 'wb') as fw:
    dict_writer = csv.DictWriter(fw, headers)
    dict_writer.writeheader()
    dict_writer.writerows(dicts)
