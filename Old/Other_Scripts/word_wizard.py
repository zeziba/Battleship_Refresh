__author__ = "Charles Engen"


class WordWizard:
    def __init__(self):
        self.name = "Word Wizard"

    def _remove_vowels_spell(self, word):
        return "".join([letter for letter in word if letter.lower() not in "aeiou"])

    def _cast_spell(self, *spell):
        words = []
        for word in spell:
            words.append(self._remove_vowels_spell(word))
        return words

    def __call__(self, *args, **kwargs):
        print(
            "I will change your words! For the better of course. See: ",
            *self._cast_spell(*args)
        )

    def __str__(self):
        return "My name is %s, nice to meet you!" % self.name
