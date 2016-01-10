#!/usr/bin/env python
from ithkuil.morphology.data import *

from downloaders.table_parser import TableParser

import requests

session = Session()

site = requests.get('http://ithkuil.net/08_adjuncts.html')

print('Downloaded.')
print('Parsing...')

parser = TableParser()
parser.feed(site.text)

wordType = session.query(ithWordType).filter(ithWordType.name == 'Personal adjunct').first()
tone = session.query(ithSlot).filter(ithSlot.wordtype == wordType).filter(ithSlot.name == '[tone]').first()
referent = session.query(ithSlot).filter(ithSlot.wordtype == wordType).filter(ithSlot.name == 'C1').first()

def morpheme(slot, content):
    morph = None
    existing = session.query(ithMorpheme)\
        .filter(ithMorpheme.morpheme == content).all()
    if len(existing) == 0:
        morph = ithMorpheme(morpheme = content)
        session.add(morph)
    else:
        morph = existing[0]
    
    existing = session.query(ithMorphemeSlot)\
        .filter(ithMorphemeSlot.slot == slot)\
        .filter(ithMorphemeSlot.morpheme.has(morpheme=content))\
        .all()
    if len(existing) == 0:
        result = ithMorphemeSlot(slot = slot, morpheme = morph)
        session.add(result)
    else:
        result = existing[0]
    session.commit()
    return result

def Atom(*morphemes):
    query = session.query(ithAtom)
    for m in morphemes:
        query = query.filter(ithAtom.morpheme_slots.contains(m))
    existing = query.all()
    result = None
    if len(existing) == 0:
        result = ithAtom()
        for m in morphemes:
            result.morpheme_slots.append(m)
        session.add(result)
    else:
        result = existing[0]
    return result

def add_value(atom, category, value):
    values = session.query(ithCategValue)\
        .filter(ithCategValue.code == value)\
        .all()
    if len(values) == 0:
        categ = session.query(ithCategory).filter(ithCategory.name == category).first()
        value = ithCategValue(category = categ, code = value)
        session.add(value)
    else:
        value = values[0]
    atom.values.append(value)

def test_table(node):
    try:
        return node.tr[0].td[0].table[0].tr[2].td[0].__data__ == 't'
    except:
        return False
    
print('Parsed.')
print('Filtering for morphology tables...')

result2 = list(filter(test_table, parser.result))

print('Filtered.')

table_falling = result2[0].tr[0].td[0].table[0]
table_high = result2[0].tr[0].td[1].table[0]

falling = morpheme(tone, '\\')
high = morpheme(tone, '¯')
rising = morpheme(tone, '/')
low = morpheme(tone, '_')

for row in table_falling.tr[2:]:
    C1 = morpheme(referent, row.td[0].__data__)
    atom = Atom(C1, falling)
    add_value(atom, 'Personal referent', row.td[1].__data__)
    atom = Atom(C1, low)
    add_value(atom, 'Personal referent', row.td[1].__data__)
    
for row in table_high.tr[2:]:
    C1 = morpheme(referent, row.td[0].__data__)
    atom = Atom(C1, high)
    add_value(atom, 'Personal referent', row.td[1].__data__)
    atom = Atom(C1, rising)
    add_value(atom, 'Personal referent', row.td[1].__data__)
    
session.commit()
print('Committed')








