#!/usr/bin/env python
from ithkuil.morphology.data import *

from downloaders.table_parser import TableParser, replace_h

import requests

session = Session()

site = requests.get('http://ithkuil.net/08_adjuncts.html')

print('Downloaded.')
print('Parsing...')

parser = TableParser()
parser.feed(site.text)

wordType = session.query(ithWordType).filter(ithWordType.name == 'Personal adjunct').first()
tone = session.query(ithSlot).filter(ithSlot.wordtype == wordType).filter(ithSlot.name == '[tone]').first()
ckslot = session.query(ithSlot).filter(ithSlot.wordtype == wordType).filter(ithSlot.name == 'Ck').first()
c1slot = session.query(ithSlot).filter(ithSlot.wordtype == wordType).filter(ithSlot.name == 'C1').first()

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
        return node.tr[1].td[0].__data__ == 'ma'
    except:
        return False
    
print('Parsed.')
print('Filtering for morphology tables...')

result2 = list(filter(test_table, parser.result))

print('Filtered.')

tab = result2[0]

tones = ['\\', '/', '¯', '_']
tone1 = ['\\', '\\', '¯', '¯']
tone2 = ['\\', '¯', '¯', '\\']

def purify(s):
    return s.replace('\n', '').replace(' ', ''). replace('\r', '').replace('\u00a0', '')

for i, row in enumerate(tab.tr[1:]):
    for j, td in enumerate(row.td[3:]):
        ref = replace_h(purify(td.__data__))
        if not ref or len(ref) > 3: continue
        ref1 = purify(tab.tr[i+1].td[2].__data__)
        ref2 = purify(tab.tr[0].td[j+3].__data__)
        
        for k, t in enumerate(tones):
            t1 = tone1[k]
            t2 = tone2[k]
            atomRef1 = Atom(morpheme(c1slot, ref1), morpheme(tone, t1))
            atomRef2 = Atom(morpheme(c1slot, ref2), morpheme(tone, t2))
            
            newAtom = Atom(morpheme(ckslot, ref), morpheme(tone, t))
            for v in atomRef1.values:
                newAtom.values.append(v)
            for v in atomRef2.values:
                newAtom.values.append(v)
                
session.commit()
print('Committed.')









