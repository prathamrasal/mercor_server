from fuzzywuzzy import process

class Amplifier: 
    def __init__(self):
        pass
    
    def amplify(self, query, keywords, amp_constant=4):
        for entity in keywords:
            query = query+(" "+entity.upper()+" ")*amp_constant
        return query