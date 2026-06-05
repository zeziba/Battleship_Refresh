__author__ = "Charles Engen"


def pig_latin(a_string):
    return (
        " ".join(
            [
                (word[1:] + word[0] + "ay") if len(word) > 1 else word
                for word in a_string.lower().split()
            ]
        )
        if any(" " == item for item in a_string)
        else (a_string.lower()[1:] + a_string.lower()[0] + "ay")
        if len(a_string) > 2
        else a_string
    )


def pig_2english(a_string):
    return (
        " ".join(
            [
                (word[-3] + word[:-3]) if len(word) > 1 else word
                for word in a_string.split()
            ]
        )
        if any(" " == item for item in a_string)
        else a_string[-3] + a_string[:-3]
        if len(a_string) > 1
        else a_string
    )
