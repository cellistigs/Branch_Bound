from git_template.strings import reverse_words


def test_reverse_words():
    inputs = [
        "Chicken produces egg.",
        "Reporters cover whales exploding.",
        "Are you as clever as I am?",
        #"Jake defeated Brian.",
    ]
    outputs = [
        "Egg produces chicken.",
        "Exploding whales cover reporters.",
        "Am I as clever as you are?",
        #"Brian defeated Jake.",
    ]

    for i in range(len(inputs)):
        assert reverse_words(inputs[i]) == outputs[i]

    return None


if __name__ == "__main__":
    test_reverse_words()
