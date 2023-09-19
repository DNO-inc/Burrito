
alphabet = {
    "а": ["a"],
    "б": ["b"],
    "в": ["v"],
    "г": ["h"],
    "ґ": ["g"],
    "д": ["d"],
    "е": ["e"],
    "є": ["ye", "ie"],
    "ж": ["zh"],
    "з": ["z"],
    "и": ["y"],
    "і": ["i"],
    "ї": ["yi", "i"],
    "й": ["y", "i"],
    "к": ["k"],
    "л": ["l"],
    "м": ["m"],
    "н": ["n"],
    "о": ["o"],
    "п": ["p"],
    "р": ["r"],
    "с": ["s"],
    "т": ["t"],
    "у": ["u"],
    "ф": ["f"],
    "х": ["kh"],
    "ц": ["ts"],
    "ч": ["ch"],
    "ш": ["sh"],
    "щ": ["shch"],
    "ю": ["yu", "iu"],
    "я": ["ya", "ia"]
}

different_values = "єїйюя"


def transliterate(initial_sentence: str):
    result = []

    for word in initial_sentence.split(" "):
        new_word = ""
        word = word.lower()
        for i, letter in enumerate(word):
            if not alphabet.get(letter):
                continue
            new_word += alphabet[letter][(0 if i == 0 else 1) if letter in different_values else 0]

        result.append(new_word)

    return "_".join(result)
