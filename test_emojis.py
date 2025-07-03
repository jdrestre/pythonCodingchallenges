import emoji

print(emoji.emojize("I love Python :snake:"))
print(emoji.emojize("Let's code! :laptop: :rocket:"))

language = "Python"
if language == "Python":
    print(emoji.emojize("Happy Coding :thumbs_up: :cow:"))

text = emoji.demojize("Good job! 😘")
print(text)
