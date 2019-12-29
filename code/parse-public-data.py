'''
This file expects 3 files to be in the same folder

legislators-social-media.json
Which is from https://theunitedstates.io/congress-legislators/legislators-social-media.json

MemberData.xml
Which is from http://clerk.house.gov/xml/lists/MemberData.xml

senators_cfm.xml
Which is from https://www.senate.gov/general/contact_information/senators_cfm.xml

This will tie together twitter handle and party affiliation based on the bioguideID
'''

import json
from xml.dom import minidom

# Store a single senator
class senator:
    def __init__(self, bioguide, twitter):
        self.bioguide = bioguide
        self.twitter = twitter
        self.affiliation = 'U'

# List of senators
senators = []

# Add an affiliation to a senator only if the bioguide matches and they have an unknown affiliation
def AddAffiliation(bioguide, affiliation):
    for s in senators:
        if s.bioguide == bioguide and s.affiliation == 'U':
            s.affiliation = affiliation
            break

# Handle the initial json file to create the list of senators
# This is from
# https://theunitedstates.io/congress-legislators/legislators-social-media.json
with open('legislators-social-media.json') as myFile:
    data = json.load(myFile)

    for d in data:
        if 'twitter' in d['social'] and 'bioguide' in d['id']:
            senators.append(senator(d['id']['bioguide'], d['social']['twitter']))

# Parse the MemberData.xml file and add affiliation
# This is from
# http://clerk.house.gov/xml/lists/MemberData.xml
xmldoc = minidom.parse('MemberData.xml')
memberList = xmldoc.getElementsByTagName('member')

for senator in memberList:
    bid = None
    affiliation = None
    memberInfo = senator.getElementsByTagName('member-info')[0]
    if memberInfo:
        bioguideId = memberInfo.getElementsByTagName('bioguideID')[0]
        party = memberInfo.getElementsByTagName('party')[0]
        if bioguideId and bioguideId.firstChild and party and party.firstChild:
            AddAffiliation(bioguideId.firstChild.nodeValue, party.firstChild.nodeValue)

# Parse the senators_cfm.xml and add affiliation if missing
# This is from
# https://www.senate.gov/general/contact_information/senators_cfm.xml
xmldoc = minidom.parse('senators_cfm.xml')
memberList = xmldoc.getElementsByTagName('member')

for senator in memberList:
    bid = None
    affiliation = None
    bioguideId = senator.getElementsByTagName('bioguide_id')[0]
    party = senator.getElementsByTagName('party')[0]
    if bioguideId and bioguideId.firstChild and party and party.firstChild:
        AddAffiliation(bioguideId.firstChild.nodeValue, party.firstChild.nodeValue)

# Print to pipe into a file
for s in senators:
    print(s.twitter, s.affiliation, s.bioguide)