#!/usr/bin/env python
from ithkuil.morphology import Session
from ithkuil.morphology.data import *

session = Session()

ext = {
    '¯': 'PRX',
    '/': 'ICP',
    '_': 'TRM',
    'ˇ': 'DPL',
    '^': 'GRA'
}

slot = session.query(ithSlot).filter(ithSlot.wordtype_id == 2 and ithSlot.name == '[tone]').first()

for morph, code in ext.items():
    
    morphemes = session.query(ithMorpheme).filter(ithMorpheme.morpheme == morph).all()
    morpheme = None
    if len(morphemes) > 0:
        morpheme = morphemes[0]
    else:
        print('Adding', morph)
        morpheme = ithMorpheme(morpheme = morph)
        session.add(morpheme)
        session.commit()
        
    value = session.query(ithCategValue).filter(ithCategValue.code == code).first()
    
    newMorphSlot = ithMorphemeSlot(morpheme = morpheme, slot = slot)
    newMorphSlot.values.append(value)
    
    session.add(newMorphSlot)
    
    print(value.code)

session.commit()

print('Committed.')









