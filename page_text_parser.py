import re
from messages import no_lines_message, not_found_message


# simple switch implementation in version 3.9, in 3.10 is possible to use match - case
def get_print_page_text(pageType, soup, articleName):
    text = ''
    if pageType == 'Search':
        possibleArticles = parseSearchText(soup)
        # Create final CLI message
        text = not_found_message(articleName, possibleArticles)
    elif pageType == 'Article':
        text = parseArticleText(soup)
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
    lineList = []
    for x in text:
        line = x.getText()
        if line != '\n':
            newLine = re.sub('\[(.*?)\]', '', line)
            lineList.append(newLine.strip())

    return lineList


# Parse text from article page
def parseArticleText(soup):
    soup = remove_scripts(soup)

    # Get all paragraph text
    text = soup.findAll('p')

    # Get Lines
    lineList = get_list_of_text_lines(text)

    # If list is empty something went wrong
    if len(lineList) < 1:
        return no_lines_message()

    # Take first 3 lines of text and remove leading and trailing space on each of them
    lines = (line.strip() for line in lineList[:3])
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # Join lines to one text with new line between them
    text = '\n'.join(chunk for chunk in chunks)

    return text


# Parse text from search page
def parseSearchText(soup):
    soup = remove_scripts(soup)

    # Get all links to possible articles
    arts = soup.find_all("div", {"class": "mw-search-result-heading"})

    # Get Lines
    lineList = get_list_of_text_lines(arts)

    # If list is empty something went wrong
    if len(lineList) < 1:
        return no_lines_message()

    # Take first 3 lines of text and remove leading and trailing space on each of them
    lines = (line.strip() for line in lineList)
    # Join lines to one text with new line between them
    possibleArticles = '\n'.join(line for line in lines)

    return possibleArticles
