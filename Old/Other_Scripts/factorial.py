import cProfile


def factorial(number):
    """
    This function calculates the factorial of the given number.
    Numbers over 1000 can take over 10secs!
    :param number: Number to calculate
    :return: Returns the value of the number calculated
    """

    def shrink_list(lst):
        """
        This sub-function takes all the numbers in the factorial and multiplies
        every other even one to ever odd one. If the amount of numbers is odd
        it takes the last one off and adds it to the end after the multiplication.
        :param lst: List of numbers to multiply
        :return: Returns a list of numbers after shortening and multiplication.
        """
        if len(lst) % 2 == 0:
            return [(item1 * item2) for item1, item2 in zip(lst[0::2], lst[1::2])]
        else:
            new_lst = lst[:-1]
            new_lst = [
                (item1 * item2) for item1, item2 in zip(new_lst[0::2], new_lst[1::2])
            ]
            new_lst.append(lst[-1])
            return new_lst

    # This creates a list of all the numbers that need to be factored
    numbers_to_multiply = [x for x in range(1, number + 1)]
    valid = False  # For our flow control
    while not valid:
        # This will continually call the sub-function till the list
        # of numbers is less than 14.
        numbers_to_multiply = shrink_list(numbers_to_multiply)
        if len(numbers_to_multiply) < 14:
            valid = True
    return_value = 1
    # This for loop finishes the multiplication on the remaining members.
    for number in numbers_to_multiply:
        return_value *= number
    return return_value


def cf_range(num_range):
    """
    This function saves the factorial to file. It also calls the function
     ranging from 1 to the given number. So all factorials to the number are
     saved to file. The computer has problems displaying any number
     the system can not handle.
    :param num_range: Range of numbers to be factored
    """
    with open("factorial_of_%s.txt" % str(num_range), "w+") as file:
        for number in range(1, num_range + 1):
            file.write(str(factorial(number)) + "\n")


cProfile.run("cf_range(1000)")
