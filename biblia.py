import argparse
import os
import requests
from bs4 import BeautifulSoup

def main():
    parser = argparse.ArgumentParser(description='Retrieve text from Bible Hub.')
    parser.add_argument('book', help='Book name (e.g., "Rdz")')
    parser.add_argument('chapter_verse', help='Chapter and verse (e.g., "1-1")')
    parser.add_argument('language', help='Language ("greek", "hebrew" or "pl")')
    args = parser.parse_args()

    text, abbr_classes = retrieve_text(args.book, args.chapter_verse, args.language)

    if abbr_classes:
        print("\nAbbr Classes:")
        for abbr, fragment in zip(abbr_classes, text.split('\n')):
            print(f"{abbr} : {fragment}")
    else:
        print(text)

def retrieve_text(book, chapter_verse, language):
    filename = generate_filename(book, chapter_verse, language)

    if os.path.exists(filename):
        return read_file(filename)

    url = generate_url(book, chapter_verse, language)
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        if language == 'pl':
            text, abbr_classes = retrieve_pl_text(soup)
        else:
            text, abbr_classes = retrieve_other_language_text(soup, language)

        save_file(filename, text, abbr_classes)
        return text, abbr_classes
    else:
        return f"Failed to retrieve content from: {url}", []

def generate_filename(book, chapter_verse, language):
    return f"{book}_{chapter_verse}_{language}.txt"

def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        file_content = file.read()
        if "\n\nAbbr Classes:\n" in file_content:
            text, abbr_section = file_content.split("\n\nAbbr Classes:\n")
            abbr_classes = abbr_section.strip().split('\n')
        else:
            text = file_content
            abbr_classes = None
        return text, abbr_classes

def generate_url(book, chapter_verse, language):
    book_number = book_name_to_number(book)
    if isinstance(book_number, str):
        return book_number  # error message
    
    if language == 'pl':
        return f'http://bibliepolskie.pl/zzteksty_wer.php?book={book_number}&chapter={chapter_verse.split("-")[0]}&verse={chapter_verse.split("-")[1]}'
    else:
        return f'https://biblehub.com/texts/{book}/{chapter_verse}.htm'

def retrieve_pl_text(soup):
    tdwtext_elements = soup.find_all(class_='tdwtext')
    tdwtext_text = ""
    abbr_classes = []

    for element in tdwtext_elements:
        tdwtext_text += element.text.strip() + "\n"
        abbr_element = element.find_previous_sibling(class_='tdabbr')
        if abbr_element:
            abbr_classes.append(abbr_element.text.strip())

    return tdwtext_text.strip(), abbr_classes

def retrieve_other_language_text(soup, language):
    if language == 'greek':
        first_element = soup.find(class_='greek')
    elif language == 'hebrew':
        first_element = soup.find(class_='heb')
    else:
        return "Invalid language. Available options are 'greek', 'hebrew' or 'pl'.", []

    if first_element:
        text = first_element.text.replace('\n', '').strip()
        abbr_classes = []
    else:
        text = f"No element found for language '{language}' on the page."
        abbr_classes = []

    return text, abbr_classes

def save_file(filename, text, abbr_classes):
    with open(filename, 'w', encoding='utf-8') as file:
        if abbr_classes:
            file.write(text + "\n\nAbbr Classes:\n")
            file.write('\n'.join(abbr_classes))
        else:
            file.write(text)

def book_name_to_number(name):
    bible_books = {
        "rdz": 1, "wj": 2, "kpł": 3, "lb": 4, "pwt": 5, "joz": 6, "sędz": 7, "rut": 8, "1sm": 9, "2sm": 10,
        "1krl": 11, "2krl": 12, "1krn": 13, "2krn": 14, "ezd": 15, "neh": 16, "est": 17, "job": 18, "ps": 19,
        "prz": 20, "koh": 21, "pnp": 22, "iz": 23, "jer": 24, "lm": 25, "ez": 26, "dn": 27, "hos": 28, "jl": 29,
        "am": 30, "abd": 31, "jon": 32, "mi": 33, "na": 34, "ha": 35, "so": 36, "ag": 37, "za": 38, "ml": 39,
        "mt": 40, "mk": 41, "łk": 42, "j": 43, "dz": 44, "rz": 45, "1kor": 46, "2kor": 47, "ga": 48, "ef": 49,
        "flp": 50, "kol": 51, "1tes": 52, "2tes": 53, "1tm": 54, "2tm": 55, "tt": 56, "flm": 57, "hbr": 58,
        "jk": 59, "1p": 60, "2p": 61, "1j": 62, "2j": 63, "3j": 64, "jd": 65, "obj": 66
    }
    lower_name = name.lower()
    return bible_books.get(lower_name, "Book not found in the Bible.")

if __name__ == "__main__":
    main()
