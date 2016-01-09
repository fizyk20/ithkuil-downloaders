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
        return node.tr[2].td[0].__data__ == 'EQU'
    except:
        return False
    
print('Parsed.')
print('Filtering for morphology tables...')

result2 = list(filter(test_table, parser.result))

print('Filtered.')
print('Reading data...')

for row in result2[0].tr[2:]:
    code = row.td[0].__data__
    name = row.td[1].__data__
    morph1 = row.td[2].__data__.replace('-', '')
    morph2 = row.td[3].__data__.replace('-', '').replace(' ', '').split('/')
    
    category = session.query(ithCategory).filter(ithCategory.name == 'Level').first()
    slot = session.query(ithSlot).filter(ithSlot.wordtype_id == 2).filter(ithSlot.name == 'Ve').first()
    
    value1 = ithCategValue(category = category, code = code + 'r', name = name + ' relative')
    session.add(value1)
    value2 = ithCategValue(category = category, code = code + 'a', name = name + ' absolute')
    session.add(value2)
    
    morphemes = session.query(ithMorpheme).filter(ithMorpheme.morpheme == morph1).all()
    morpheme1 = None
    if len(morphemes) > 0:
        morpheme1 = morphemes[0]
    else:
        print('Adding', morph1)
        morpheme1 = ithMorpheme(morpheme = morph1)
        session.add(morpheme1)
        session.commit()
    
    newMorphSlot = ithMorphemeSlot(morpheme = morpheme1, slot = slot)
    newMorphSlot.values.append(value1)
    
    for morph in morph2:
        morphemes = session.query(ithMorpheme).filter(ithMorpheme.morpheme == morph).all()
        morpheme = None
        if len(morphemes) > 0:
            morpheme = morphemes[0]
        else:
            print('Adding', morph)
            morpheme1 = ithMorpheme(morpheme = morph)
            session.add(morpheme)
            session.commit()
        
        newMorphSlot = ithMorphemeSlot(morpheme = morpheme, slot = slot)
        newMorphSlot.values.append(value2)
        session.add(newMorphSlot)
    
    print(value1.code, value2.code)

session.commit()

print('Committed.')









