class Amplifier: 
    def __init__(self):
        pass
    
    def amplify(self, query, keywords, amp_constant=4):
        amplified_keywords = [keyword.upper() * amp_constant for keyword in keywords]
        amplified_query = ' '.join([query] + amplified_keywords)
        return amplified_query
