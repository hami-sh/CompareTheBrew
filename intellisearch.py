def intellisearch(terms):
    """
    Find related terms based on term inputted into search - by Hamish Bultitude
    :param term: list of strings
    :return: list of terms related to string inputted
    """
    # create mapping of all alcohol types to general "macro" terms
    term_map = dict()
    term_map['vodka'] = ['spirit', 'russia', 'distilled']
    term_map['rice vodka'] = ['spirit', 'japan', 'distilled']
    term_map['scotch'] = ['spirit', 'scotland', 'distilled']
    term_map['rum'] = ['spirit', 'america', 'distilled']
    term_map['american whiskey'] = ['spirit', 'whiskey', 'america', 'distilled']
    term_map['liqueurs'] = ['spirit', 'distilled', 'sugar', 'fruit', 'herbs', 'spices']
    term_map['gin'] = ['spirit', 'distilled', 'juniper', 'berry']
    term_map['tequila'] = ['spirit', 'agave', 'mexico', 'distilled']
    term_map['brandy'] = ['spirit', 'distilled', 'dutch']
    term_map['irish whiskey'] = ['spirit', 'distilled', 'ireland', 'whiskey']
    term_map['bourbon'] = ['spirit', 'distilled', 'america', 'whiskey']
    term_map['premix vodka'] = ['spirit', 'distilled', 'premixed', 'flavour', 'flavor', 'party', 'teenage', 'girl']
    term_map['blended whisky'] = ['spirit', 'distilled', 'blend', 'whiskey']  # spelling mistake on BWS behalf lol
    term_map['blended whiskey'] = ['spirit', 'distilled', 'blend', 'whiskey']
    term_map['corn vodka'] = ['spirit', 'distilled']
    term_map['aperitifs'] = ['spirit', 'wine', 'distilled']
    term_map['premix'] = ['spirit', 'wine', 'distilled']
    term_map['ready to drink'] = ['spirit', 'wine', 'premix']
    term_map['other spirits'] = ['spirit', 'distilled']
    term_map['flavoured vodka'] = ['spirit', 'distilled', 'flavour', 'flavor']
    term_map['ouzo'] = ['spirit', 'distilled', 'anise', 'greece', 'oyzo', 'flavour', 'flavor', 'aperitif']
    term_map['cognac'] = ['spirit', 'distilled', 'brandy', 'france']
    term_map['japanese whisky'] = ['spirit', 'distilled', 'japan', 'whiskey', 'whisky']
    term_map['australian whisky'] = ['spirit', 'distilled', 'australia', 'whiskey', 'whisky']
    term_map['sparkling white'] = ['wine']
    term_map['schnapps'] = ['spirit', 'fruit', 'brandy', 'liqueurs', 'infusion']
    term_map['champagne'] = ['wine', 'french', 'sparkling']
    term_map['medium bodied white'] = ['wine', 'white']
    term_map['dry red'] = ['wine']
    term_map['Sweet White'] = ['wine']
    term_map['Medium Bodied Red'] = ['wine']
    term_map['fortified'] = ['wine', 'spirit', 'brandy', 'mix']
    term_map['dry white'] = ['wine']
    term_map['rosé'] = ['wine', 'rose', 'rosado', 'pink']
    term_map['sweet red'] = ['wine']
    term_map['spritzer'] = ['wine', 'white', 'carbonated', 'mineral', 'sparkling', 'water']
    term_map['sweet sparkling'] = ['wine']
    term_map['Dry Rosé'] = ['rose', 'wine']
    term_map['Sparkling Rosé'] = ['rose', 'wine']
    term_map['cava'] = ['sparkling', 'wine', 'white', 'rose', 'rosé']
    term_map['prosecco'] = ['italy', 'wine', 'italian', 'sparkling', 'white']
    term_map['sparkling red'] = ['wine']
    term_map['sparkling rose'] = ['wine', 'rosé']
    term_map['rice wine'] = ['wine', 'asia', 'distilled', 'fermented']
    term_map['rice wine'] = ['wine', 'asia', 'distilled', 'fermented']
    term_map['rose'] = ['wine', 'rosé']
    term_map['white blend'] = ['wine']
    term_map['Low Alcohol Wine'] = ['wine', 'dumb']  # genuinely hope no one searches for this...
    term_map['Dessert Wine'] = ['wine']
    term_map['Dessert Wine'] = ['wine']
    term_map['craft beer'] = ['small', 'independent', 'traditional', 'beer']
    term_map['lager'] = ['beer']
    term_map['lager'] = ['beer', 'light']
    term_map['canadian whisky'] = ['whiskey', 'spirit', 'distilled']
    term_map['ale'] = ['beer', 'sweet', 'fruit']
    term_map['pale ale'] = ['beer']
    term_map['pilsner'] = ['beer', 'pils', 'pilsener', 'lager', 'pale', 'bavarian']
    term_map['radler'] = ['beer', 'german', 'fruit', 'soda', 'mix']
    term_map['beer'] = ['beer']
    term_map['Ginger Beer'] = ['ginger', 'beer']
    term_map['dark'] = ['beer', 'ale']
    term_map['stout'] = ['beer', 'dark', 'fermented']
    term_map['premium beer'] = ['beer']
    term_map['craft cider'] = ['beer', 'small', 'independent', 'traditional', 'fermented', 'fruit', 'cider']
    term_map['strong pale ale'] = ['beer', 'sweet', 'fruity']
    term_map['cider'] = ['beer', 'fermented', 'fruit', 'cider']
    term_map['mid strength'] = ['beer']
    term_map['golden ale'] = ['beer', 'ale']
    term_map['low carb beer'] = ['beer', 'healthy']
    term_map['flavoured beer'] = ['beer', 'flavour', 'flavor', 'mix']
    term_map['session ale'] = ['beer', 'healthy', 'low']
    term_map['non alcoholic'] = ['beer', 'healthy', 'low']
    term_map['wheat beer'] = ['beer']
    term_map['india pale ale'] = ['beer']
    term_map['amber ale'] = ['beer', 'malt']
    term_map['dark ale'] = ['beer']
    term_map['xpa'] = ['beer', 'pale', 'ale', 'extra']
    term_map['ipa'] = ['beer', 'ale', 'india', 'pale']
    term_map['light beer'] = ['beer', 'healthy']
    term_map['medium dry'] = ['wine']

    # other slang terms
    term_map['cask'] = ['goon', 'sack', 'piss']
    term_map['spirits'] = ['hard liquor']

    # print(term_map)

    # we now need to see if any terms are in the values of each key
    dupOutput = list()
    for term in terms:
        # print("<" + term + ">")
        for key in term_map.keys():
            # print("[" + key + "]")
            for value in term_map.get(key):  # O(n^3) - oh yeah baby kill me
                # print("(" + value + ")")
                if term.find(value) != -1 or value.find(term) != -1:
                    # print("MATCH (k:v)" + key + ":" + value)
                    dupOutput.append(key)
                    dupOutput.append(value)

    for term in terms:
        dupOutput.append(term)

    joined = ""
    for term in terms:
        joined += " " + term

    dupOutput.append(joined)

    cleanOutput = list(dict.fromkeys(dupOutput))

    print(cleanOutput)
    return cleanOutput

def main():
    print("input your search terms")
    input_string = input()
    terms = input_string.split(" ")
    intellisearch(terms)


if __name__ == "__main__":
    main()
