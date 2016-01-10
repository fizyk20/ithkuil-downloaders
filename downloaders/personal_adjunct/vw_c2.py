#!/usr/bin/env python
from ithkuil.morphology.data import *

session = Session()

wordType = session.query(ithWordType).filter(ithWordType.name == 'Personal adjunct').first()
vwslot = session.query(ithSlot).filter(ithSlot.wordtype == wordType).filter(ithSlot.name == 'Vw').first()
c2slot = session.query(ithSlot).filter(ithSlot.wordtype == wordType).filter(ithSlot.name == 'C2').first()

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
    
vws = ['', 'ö', 'î', 'a', 'ü', 'o', 'e', 'u', 'ë']
vwvals = ['UNI', 'DPX', 'DCT', 'AGG', 'SEG', 'CPN', 'COH', 'CST', 'MLT']

c2s = ['h', 'w', 'y', 'hw']
c2vals = ['CSL', 'ASO', 'VAR', 'COA']

for i in range(0,9):
    m = morpheme(vwslot, vws[i])
    atom = Atom(m)
    add_value(atom, 'Configuration', vwvals[i])

for i in range(0,4):
    m = morpheme(c2slot, c2s[i])
    atom = Atom(m)
    add_value(atom, 'Affiliation', c2vals[i])
    
session.commit()
print('Committed')








