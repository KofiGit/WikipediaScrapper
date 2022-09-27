def not_found_message(articleName, possibleArticles):
    text = f'Článek s názvem \'{articleName}\' nebyl nalezen. Zadaný text se vyskytuje v článcích s tímto názvem:\n {possibleArticles} '
    return text


def no_lines_message():
    return 'Omlouváme se, ale žádné řádky s textem nebyli nalezeny.'


def not_wikipedia_page_message():
    return "Omlouvame se, ale nebyla nalezena korektni struktura wikipedie."