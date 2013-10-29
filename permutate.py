#!/usr/bin/python

# Settings

MIN_WORD_LENGTH = 4
MAX_PARTS = 3
JOIN_CHARS = ['', ' ', '.', '-', '+', '_']

# Import dependancies
import itertools
import sys

def is_good_pass(permutation):

    max_word_length = 0

    for word in permutation:
        temp = list(permutation[:])
        temp.remove(word)
        word_length = len(word)

        if ((word_length >= MIN_WORD_LENGTH)
            and (word in temp)):
            return False

        if word_length > max_word_length:
            max_word_length = word_length

    if max_word_length < MIN_WORD_LENGTH:
        return False

    return True

def main():

    # Create array with known parts of the password
    f = open(sys.argv[1])
    parts = f.read().split()
    f.close()

    # Number of parts per password
    for number in range(1, MAX_PARTS + 1):

        # Build a list of combinations of knows parts with number of parts
        permutations = list(itertools.permutations(parts, number))

        # Print list
        for (i, permutation) in enumerate(permutations):
            if (not is_good_pass(permutation)):
                continue
            if len(permutation) > 1:
                for char in JOIN_CHARS:
                    print char.join(permutation)
            else:
                print ''.join(permutation)

if __name__ == '__main__':
    main()
