""" Licensing and authorship go here. """

""" This file contains example source code, which can be unit tested
    in tests/ with pytest.  Unit tests for this code are automatically 
    run with each git commit (see .travis.yml). """


def reverse_words(sentence):
    """Returns a word reversed sentence. 

		REQUIRES Sentence ends in singular punctuation.

		Note: the final word is always uncapitalized. 

		# Arguments 
            str (string): Sentence to reverse words of.
    
        # Returns 
            (string): Word-reversed sentence
    """

    punct = sentence[-1]
    words = sentence[:-1].split(" ")
    words.reverse()
    words[0] = words[0].capitalize()
    words[-1] = words[-1].lower()
    rev_sentence = words[0]
    for i in range(1, len(words)):
        rev_sentence += " %s" % words[i]
    rev_sentence += punct

    return rev_sentence
