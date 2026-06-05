__author__ = "Charles Engen"

response = {
    1: "BEFORE: Value ID: %s, List[Index} ID: %s, Match: %s",
    2: "AFTER:  Value ID: %s, List[Index} ID: %s, Match: %s",
    3: "LIST ID: %s, LIST ITEMS ID: %s",
}


def get_id(thing_to_check):
    print(
        response[3]
        % (
            id(thing_to_check),
            [(index + 1, id(id_of)) for index, id_of in enumerate(thing_to_check)],
        )
    )
    for index, value in enumerate(thing_to_check):
        print(
            response[1]
            % (
                id(value),
                id(thing_to_check[index]),
                (True if id(thing_to_check[index]) == id(value) else False),
            )
        )
        value += 1
        print(
            response[2]
            % (
                id(value),
                id(thing_to_check[index]),
                (True if id(thing_to_check[index]) == id(value) else False),
            )
        )
