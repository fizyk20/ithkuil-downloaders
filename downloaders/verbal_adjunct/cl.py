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
        return node.tr[1].td[1].__data__ == 'MNO'
    except:
        return False
    
print('Parsed.')
print('Filtering for morphology tables...')

result2 = list(filter(test_table, parser.result))

print('Filtered.')
print('Reading data...')

for row in result2[0].tr[1:]:
    code = row.td[1].__data__
    name = row.td[2].__data__
    morph = row.td[3].__data__.replace('-', '').replace('—', '')
    
    morphemes = session.query(ithMorpheme).filter(ithMorpheme.morpheme == morph).all()
    morpheme = None
    if len(morphemes) > 0:
        morpheme = morphemes[0]
    else:
        print('Adding', morph)
        morpheme = ithMorpheme(morpheme = morph)
        session.add(morpheme)
        session.commit()
        
    slot = session.query(ithSlot).filter(ithSlot.wordtype_id == 2 and ithSlot.name == 'Cl').first()
    value = session.query(ithCategValue).filter(ithCategValue.code == code).first()
    
    newMorphSlot = ithMorphemeSlot(morpheme = morpheme, slot = slot)
    newMorphSlot.values.append(value)
    
    session.add(newMorphSlot)
    
    print(value.code)

session.commit()

print('Committed.')









