#!/usr/bin/env python
from ithkuil.morphology import Session
from ithkuil.morphology.data import *

from downloaders.table_parser import TableParser

import requests

session = Session()

site = requests.get('http://ithkuil.net/06_verbs_2.html')

print('Downloaded.')
print('Parsing...')

parser = TableParser()
parser.feed(site.text)

def test_table(node):
    try:
        return node.tr[4].td[1].__data__ == 'RTR'
    except:
        return False
    
print('Parsed.')
print('Filtering for morphology tables...')

result2 = list(filter(test_table, parser.result))

print('Filtered.')
print('Reading data...')
            
slot = session.query(ithSlot).filter(ithSlot.wordtype_id == 2).filter(ithSlot.name == 'Vs').first()

for row in result2[0].tr[4:]:
    code = row.td[1].__data__.replace(' ', '')
    name = row.td[2].__data__
    morphs = row.td[3].__data__.replace(' ', '').split('/')
    
    value = session.query(ithCategValue).filter(ithCategValue.code == code).first()
    
    for morph in morphs:
        morphemes = session.query(ithMorpheme).filter(ithMorpheme.morpheme == morph).all()
        morpheme = None
        if len(morphemes) > 0:
            morpheme = morphemes[0]
        else:
            print('Adding', morph)
            morpheme = ithMorpheme(morpheme = morph)
            session.add(morpheme)
            session.commit()
        
        newMorphSlot = ithMorphemeSlot(morpheme = morpheme, slot = slot)
        newMorphSlot.values.append(value)
        
        session.add(newMorphSlot)
    
    print(value.code)

session.commit()

print('Committed.')









