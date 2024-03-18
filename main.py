from APIs import get_weather
from voice import Voice
from listener import Listener
from difflib import get_close_matches

ai = Voice()
ai.slow_dwn(50)
try:
    listener = Listener()
except Exception as Err:
    print("Error Occurred!",Err)
result = listener.listen()
results = result.split()
print(results)
ai.say(result)

# if len(get_close_matches('weather',results)) != 0:
#     ai.say("Hello there.")

#     ai.say("I shall tell you the current weather in Sharjah")
#     ai.say(get_weather("Sharjah"))