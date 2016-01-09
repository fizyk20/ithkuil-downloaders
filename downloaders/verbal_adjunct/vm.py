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
        return node.tr[2].td[1].__data__ == 'DES'
    except:
        return False
    
print('Parsed.')
print('Filtering for morphology tables...')

result2 = list(filter(test_table, parser.result))

print('Filtered.')
print('Reading data...')

for row in result2[0].tr[1:16]:
    code1 = row.td[1].__data__
    name1 = row.td[2].__data__
    morph1 = row.td[3].__data__.replace(' ', '').split('/')
    
    code2 = row.td[5].__data__
    name2 = row.td[6].__data__
    morph2 = row.td[7].__data__.replace(' ', '').split('/')
    
    category = session.query(ithCategory).filter(ithCategory.name == 'Modality').first()
    slot = session.query(ithSlot).filter(ithSlot.wordtype_id == 2).filter(ithSlot.name == 'Vm').first()
    
    value1 = ithCategValue(category = category, code = code1, name = name1)
    session.add(value1)
    value2 = ithCategValue(category = category, code = code2, name = name2)
    session.add(value2)
    
    for morph in morph1:
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
        newMorphSlot.values.append(value1)
    
        session.add(newMorphSlot)
    
    for morph in morph2:
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
        newMorphSlot.values.append(value2)
    
        session.add(newMorphSlot)
    
    print(value1.code, value2.code)
    
row = result2[0].tr[16]
code1 = row.td[2].__data__
name1 = row.td[3].__data__
morph1 = row.td[4].__data__.replace(' ', '').split('/')

category = session.query(ithCategory).filter(ithCategory.name == 'Modality').first()
slot = session.query(ithSlot).filter(ithSlot.wordtype_id == 2).filter(ithSlot.name == 'Vm').first()

value1 = ithCategValue(category = category, code = code1, name = name1)
session.add(value1)

for morph in morph1:
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
    newMorphSlot.values.append(value1)

    session.add(newMorphSlot)
    
print(value1.code)

session.commit()

print('Committed.')









