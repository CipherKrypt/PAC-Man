import pyttsx3
class Voice():
    def __init__(self):
        self.engine = pyttsx3.init() # object creation
        self.engine.setProperty('rate', 150)
        self.ch_v(1)
        # self.engine.setProperty()

    def say(self,text):
        self.engine.say(text)
        self.engine.runAndWait()
    
    def slow_dwn(self, amnt:int = 20):
        rate = int(self.engine.getProperty('rate'))
        if rate == 70:
            return Exception("Speed to Low") 
        else:
            new_rate = 70 if (rate - amnt) < 70 else rate-amnt
            self.engine.setProperty('rate',new_rate)

    def speed_up(self, amnt:int = 20):
        rate = int(self.engine.getProperty('rate'))
        if rate == 250:
            return Exception("Speed to high") 
        else:
            new_rate = 250 if (rate + amnt) > 250 else rate+amnt
            self.engine.setProperty('rate',new_rate)


        # """ RATE"""
        # rate = engine.getProperty('rate')   # getting details of current speaking rate
        # print (rate)                        #printing current voice rate


        # """VOLUME"""
        # volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
        # print (volume)                          #printing current volume level
        # engine.setProperty('volume',0.7)    # setting up volume level  between 0 and 1

        # """VOICE"""
    def ch_v(self,ID):
        voices = self.engine.getProperty('voices') 
        if ID >= 0 and ID <= len(voices):
            self.engine.setProperty('voice', voices[ID].id)   #changing index, changes voices. 1 for female
        



