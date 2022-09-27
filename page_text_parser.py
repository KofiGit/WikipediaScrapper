import re
from messages import no_lines_message, not_found_message


# simple switch implementation in version 3.9, in 3.10 is possible to use match - case
def get_print_page_text(page_type, soup, article_name):
    text = ''
    if page_type == 'Search':
        possible_articles = parse_search_page(soup)
        # Create final CLI message
        text = not_found_message(article_name, possible_articles)
    elif page_type == 'Article':
        text = parse_article_page(soup)
    else:
        text = 'Program nenašel správný parser pro stránku.'

    return text


def remove_scripts(soup):
    # Removing all scripts and styles from page
    for script in soup(["script", "style"]):
        script.extract()
    return soup


def get_list_of_text_lines(text):
    # Preparing list of paragraph lines with text
    line_list = []
    for x in text:
        line = x.getText()
        if line != '\n':
            newLine = re.sub('\[(.*?)\]', '', line)
            line_list.append(newLine.strip())

    return line_list


# Parse text from article page
def parse_article_page(soup):
    soup = remove_scripts(soup)

    # Get all paragraph text
    text = soup.findAll('p')

    # Get Lines
    line_list = get_list_of_text_lines(text)

    # If list is empty something went wrong
    if len(line_list) < 1:
        return no_lines_message()

    # Take first 3 lines of text and remove leading and trailing space on each of them
    lines = (line.strip() for line in line_list[:3])
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # Join lines to one text with new line between them
    text = '\n'.join(chunk for chunk in chunks)

    return text


# Parse text from search page
def parse_search_page(soup):
    soup = remove_scripts(soup)

    # Get all links to possible articles
    arts = soup.find_all("div", {"class": "mw-search-result-heading"})

    # Get Lines
    line_list = get_list_of_text_lines(arts)

    # If list is empty something went wrong
    if len(line_list) < 1:
        return no_lines_message()

    # Take lines from search
    lines = (line.strip() for line in line_list)
    # Join lines to one text with new line between them
    possible_articles = '\n'.join(line for line in lines)

    return possible_articles
