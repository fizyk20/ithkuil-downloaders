#!/usr/bin/env python
from ithkuil.morphology.data import *

session = Session()

wordType = session.query(ithWordType).filter(ithWordType.name == 'Personal adjunct').first()
vxc = session.query(ithSlot).filter(ithSlot.wordtype_id == 1).filter(ithSlot.name == 'VxC').first()
csvs = session.query(ithSlot).filter(ithSlot.wordtype == wordType).filter(ithSlot.name == 'CsVs').first()

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

for mold in vxc.morphemes:
    m = morpheme(csvs, mold.morpheme.morpheme)
    atom = Atom(m)
    for val in mold.atoms[0].values:
        atom.values.append(val)
    
session.commit()
print('Committed')








