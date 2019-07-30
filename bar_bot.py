# basic bartender chat bot that responds based on regex given

from nltk.chat.util import Chat, reflections

user_greetings = (r"Hi", r"Hello", r"Howdy")
bar_bot_greetings = ["How do you do?", "Mhmm.", "Parched?", "Fancy a drink?",
                     "You new around these parts?"]
bar_bot_farewells = ["Fair enough.", "Salutations, friend.", "That's just how it is." 
                     "Bye now, cowpoke.", "A damn shame."]
bar_bot_neutral = ["Good for you.", "Alrighty, then.", "*Nods*", "Interesting.",
                   "Uh-huh."]

dialogue = (
    (
        r"hi", (bar_bot_greetings)
    ),
    (
        r"(.*) whiskey(.*)", ("%1 whiskey coming right up.", "Sure thing cowpoke.")
    ),
    (
        r"(.*) have?", ("We got beer, spirits and a whole lotta whiskey.")
    ),
    (
        r"(.*)recommend(.*)", ("Other than whiskey, An old Chattanooga beer.")
    ),
    (
        r"where am(.*)", ("The Salty Spitoon.", "The one and only: Salty Spitoon.")
    ),
    (
        r"(.*)\?", ("What was that?", "Can you repeat the question?",
                   "I didn't quite catch that.", "Could you speak a little louder?")
    ),
    (
        r"quit", (bar_bot_farewells)
    ),
    (
        r"(.*)", (bar_bot_neutral)
    ),
)

bar_bot = Chat(dialogue, reflections)


def bar_demo():
    print("Welcome to the Salty Spitoon. Home of the best whiskey for the next 100 miles!")
    print("*" * 78)
    print("'Howdy cowpoke. What can I get you?'")

    bar_bot.converse()

bar_demo()
