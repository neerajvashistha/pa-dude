import aiml
import os

kernel = aiml.Kernel()

kernel.setBotPredicate("name", "Rey")
kernel.setBotPredicate("city", "Bangalore")
kernel.setBotPredicate("email", "reyxi666@gmail.com")
kernel.setBotPredicate("phylum", "computer program")
kernel.setBotPredicate("species", "robot")
kernel.setBotPredicate("nationality", "cyberspace")
kernel.setBotPredicate("language", "python")
kernel.setBotPredicate("favortemovie", "Iron Man")
kernel.setBotPredicate("kindmusic", "Coldplay")
kernel.setBotPredicate("domain", "Robot")
kernel.setBotPredicate("gender", "female")
kernel.setBotPredicate("age","12")
kernel.setBotPredicate("birthday","2016")
kernel.setBotPredicate("botmaster","mycreators")

if os.path.isfile("bot_brain.brn"):
    kernel.bootstrap(brainFile = "bot_brain.brn")
else:
    kernel.bootstrap(learnFiles = "std_startup.xml", commands = "load aiml b")
    kernel.saveBrain("bot_brain.brn")


bot_name = kernel.getBotPredicate("name")
print bot_name
sessionId = 12345
# kernel now ready for use
while True:
    message = raw_input("HUMAN>> ")
    if message == "quit":
        sessionData = kernel.getSessionData(sessionId)
        print sessionData
        exit()
    elif message == "save":
        kernel.saveBrain("bot_brain.brn")
    else:
        bot_response=kernel.respond(message, sessionId)
        # Do something with bot_response
        print "ROBOT> ",bot_response
        