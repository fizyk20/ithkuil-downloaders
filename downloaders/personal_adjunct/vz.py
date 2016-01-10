#!/usr/bin/env python
from ithkuil.morphology.data import *

session = Session()

wordType = session.query(ithWordType).filter(ithWordType.name == 'Personal adjunct').first()
tone = session.query(ithSlot).filter(ithSlot.wordtype == wordType).filter(ithSlot.name == '[tone]').first()
slotvz = session.query(ithSlot).filter(ithSlot.wordtype == wordType).filter(ithSlot.name == 'Vz').first()

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
    
vzs = ['a', 'u', 'i', 'e', 'o', 'ö', 'ü', 'ai', 'au', 'ei', 'eu', 'oi', 'iu']
vals = ['UNI', 'DPX', 'DPX', 'DCT', 'AGG', 'SEG', 'CPN', 
        'COH', 'COH', 'CST', 'CST', 'MLT', 'MLT']
altvzs = ['a', 'u', 'i', 'e', 'o']
altvals = ['CPN', 'COH', 'COH', 'CST', 'MLT']

falling = morpheme(tone, '\\')
high = morpheme(tone, '¯')
fallrise = morpheme(tone, 'ˇ')
risefall = morpheme(tone, '^')

for i in range(0,13):
    m = morpheme(slotvz, vzs[i])
    atom = Atom(m, falling)
    add_value(atom, 'Configuration', vals[i])
    atom = Atom(m, high)
    add_value(atom, 'Configuration', vals[i])
    
for i in range(0, 5):
    m = morpheme(slotvz, altvzs[i])
    atom = Atom(m, fallrise)
    add_value(atom, 'Configuration', altvals[i])
    atom = Atom(m, risefall)
    add_value(atom, 'Configuration', altvals[i])
    
session.commit()
print('Committed')








