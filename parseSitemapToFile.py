#this program parses an xml-sitemaps.com generated xml file to an file with URLs seperated by newlines
#just edit the xml_root and target_file path
xml_root="not_there_yet_Melinda.xml"
target_file="websitesUrlMelinda"
import xml.etree.ElementTree as ET 
tree = ET.parse(xml_root)
root = tree.getroot()
for i in range (0,len(root)):
    url = str (root[i][0].text)
    with open(target_file, 'a+') as f :
        f.write(url + '\n')
print ("Total:",len(root),"URLs")
