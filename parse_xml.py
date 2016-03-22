import xml.etree.ElementTree as ET
tree = ET.parse('transcript_xml')
root = tree.getroot()
for child in root:
    print child.attrib
