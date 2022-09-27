from messages import not_wikipedia_page_message
from page_text_parser import get_print_page_text
from wikipedia_parser import WikipediaParser

if __name__ == '__main__':
    parser = WikipediaParser()
    keep_running = True

    print('Zadávej výrazy, které bude program vyhledávat na Wikipedii.\n Pro ukočení napiš \'END\'')

    while keep_running:
        try:
            keyword = str(input('Zadejte výraz, který chcete vyhledat:'))

            if 'END' == keyword.upper():
                # Use variable instead of break
                keep_running = False
                continue

            if keyword in parser.already_looked_up:
                lookup_decide = str(input('Výraz jste již hledali. Přejete si vyhledat znovu? [ano / ne]'))
                if lookup_decide.lower() == 'ne':
                    continue

            parser.search_site(keyword)

            if parser.is_wikipedia_page():
                site = parser.read_page()
                pageType = parser.get_page_type()
                text = get_print_page_text(pageType, site, keyword)
                print(text)
            else:
                print(not_wikipedia_page_message())
        except Exception as ex:
            print(f'V programu nastala vyjimka:\n {str(ex)}')

    parser.end_driver()
    input("Stiskni klavesu pro ukonceni programu....")
