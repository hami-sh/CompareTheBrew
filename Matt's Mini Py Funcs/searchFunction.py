# REQUIRES pyspellchecker - pip install pyspellchecker
from spellchecker import SpellChecker

# vodka is misspelt, but filterSearch will return type: vodka, category: spirits
STRING = "1 bitch ass vooodka please goon"

TYPES = ["beer", "wine", "cider", "spirits", "sake", "gin", "whiskey", "rum", "tequila", "vodka", "bourbon", "brandy"]
SPIRITS = ["gin", "whiskey", "rum", "tequila", "vodka", "bourbon", "brandy"]


def filter_search(string):
    output = []
    category = "other"
    terms = string.split()
    for term in terms:
        lower_term = term.lower()
        if lower_term in TYPES:
            if lower_term == "beer" or lower_term == "wine" or lower_term == "spirits" or lower_term == "cider":
                output.append(("Type: " + lower_term, "Category: " + category))
            elif lower_term in SPIRITS:
                category = "spirits"
                output.append(("Type: " + lower_term, "Category: " + category))
            else:
                output.append(("Type: " + lower_term, "Category: " + category))
            return output
    #   at this point none of the search terms are spirits, beer/wine/cider. Autocorrect words to check.
    for term in terms:
        corrected_term = SpellChecker().correction(term)
        lower_term = corrected_term.lower()
        if lower_term in TYPES:
            if lower_term == "beer" or lower_term == "wine" or lower_term == "spirits" or lower_term == "cider":
                output.append(("Type: " + lower_term, "Category: " + category))
            elif lower_term in SPIRITS:
                category = "spirits"
                output.append(("Type: " + lower_term, "Category: " + category))
            else:
                output.append(("Type: " + lower_term, "Category: " + category))
            return output
    # at this point no type or category has been found. Check for other terms like mL sizes???-> how would we handle?
    return "No alcohol specifications found."

def main():
    print(filter_search(STRING))

if __name__ == '__main__':
    main()