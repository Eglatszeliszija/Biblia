import argparse
import os
import requests
from bs4 import BeautifulSoup

# Funkcja do pobierania tekstu z internetu lub z pliku
def retrieve_text(book, chapter_verse, language):
    # Tworzymy nazwę pliku na podstawie danych wejściowych
    filename = f"{book}_{chapter_verse}_{language}.txt"

    # Sprawdzamy, czy plik już istnieje
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            file_content = file.read()
            # Sprawdzenie czy istnieje sekcja z klasami skrótów
            if "\n\nKlasy abbr:\n" in file_content:
                text, abbr_section = file_content.split("\n\nKlasy abbr:\n")
                abbr_classes = abbr_section.strip().split('\n')
            else:
                text = file_content
                abbr_classes = None
            return text, abbr_classes
    else:
        # Tworzymy adres URL strony na podstawie podanych danych
        if language == 'pl':
            url = f'http://bibliepolskie.pl/zzteksty_wer.php?book={book_name_to_number(book)}&chapter={chapter_verse.split("-")[0]}&verse={chapter_verse.split("-")[1]}'
        else:
            url = f'https://biblehub.com/texts/{book}/{chapter_verse}.htm'

        # Pobieramy zawartość strony internetowej
        response = requests.get(url)

        # Sprawdzamy, czy pobranie było udane
        if response.status_code == 200:
            # Parsujemy zawartość strony przy użyciu Beautiful Soup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Jeśli użytkownik wybrał język "pl", użyj funkcji retrieve_pl_text
            if language == 'pl':
                text, abbr_classes = retrieve_pl_text(soup)
            else:
                if language == 'greek':
                    first_element = soup.find(class_='greek')
                elif language == 'hebrew':
                    first_element = soup.find(class_='heb')
                else:
                    return "Nieprawidłowy język. Dostępne opcje to 'greek', 'hebrew' lub 'pl'.", []

                # Jeśli znaleziono element w odpowiednim języku, zwracamy jego tekst
                if first_element:
                    text = first_element.text.replace('\n', '').strip()
                    abbr_classes = []
                else:
                    text = f"Nie znaleziono elementu w języku '{language}' na stronie: {url}"
                    abbr_classes = []

            # Zapisujemy pobrany tekst i klasy abbr do pliku
            with open(filename, 'w', encoding='utf-8') as file:
                if abbr_classes:
                    for abbr, fragment in zip(abbr_classes, text.split('\n')):
                        file.write(f"{abbr} : {fragment}\n")
                else:
                    file.write(text)

            return text, abbr_classes
        else:
            return f"Nie udało się pobrać zawartości strony: {url}", []

# Funkcja do parsowania tekstu w języku polskim
def retrieve_pl_text(soup):
    # Znajdujemy wszystkie elementy o klasie "tdwtext"
    tdwtext_elements = soup.find_all(class_='tdwtext')

    # Łańcuch przechowujący tekst z elementów "tdwtext"
    tdwtext_text = ""

    # Lista przechowująca klasy abbr
    abbr_classes = []

    # Iterujemy przez wszystkie znalezione elementy i dodajemy ich tekst do łańcucha
    for element in tdwtext_elements:
        tdwtext_text += element.text.strip() + "\n"

        # Znajdujemy element o klasie "tdabbr" odpowiadający danemu elementowi "tdwtext"
        abbr_element = element.find_previous_sibling(class_='tdabbr')
        if abbr_element:
            abbr_classes.append(abbr_element.text.strip())

    return tdwtext_text.strip(), abbr_classes

# Funkcja przekształcająca nazwę księgi na numer
def book_name_to_number(name):
    bible_books = {
        "Rdz": 1, "Wj": 2, "Kpł": 3, "Lb": 4, "Pwt": 5,
        "Joz": 6, "Sędz": 7, "Rut": 8, "1Sm": 9, "2Sm": 10,
        "1Krl": 11, "2Krl": 12, "1Krn": 13, "2Krn": 14, "Ezd": 15,
        "Neh": 16, "Est": 17, "Job": 18, "Ps": 19, "Prz": 20,
        "Koh": 21, "Pnp": 22, "Iz": 23, "Jer": 24, "Lm": 25,
        "Ez": 26, "Dn": 27, "Hos": 28, "Jl": 29, "Am": 30,
        "Abd": 31, "Jon": 32, "Mi": 33, "Na": 34, "Ha": 35,
        "So": 36, "Ag": 37, "Za": 38, "Ml": 39,
        "Mt": 40, "Mk": 41, "Łk": 42, "J": 43, "Dz": 44,
        "Rz": 45, "1Kor": 46, "2Kor": 47, "Ga": 48,
        "Ef": 49, "Flp": 50, "Kol": 51, "1Tes": 52, "2Tes": 53,
        "1Tm": 54, "2Tm": 55, "Tt": 56, "Flm": 57, "Hbr": 58,
        "Jk": 59, "1P": 60, "2P": 61, "1J": 62, "2J": 63,
        "3J": 64, "Jd": 65, "Obj": 66
    }
    # Sprawdzamy, czy nazwa księgi jest w słowniku
    if name in bible_books:
        return bible_books[name]
    else:
        return "Nie znaleziono księgi w biblii."

if __name__ == "__main__":
    # Parser argumentów z linii poleceń
    parser = argparse.ArgumentParser(description='Retrieve text from Bible Hub.')
    parser.add_argument('book', help='Nazwa księgi (np. "Rdz") - skróty: Rdz, Wj, Kpł, Lb, Pwt, Joz, Sędz, Rut, 1Sm, 
    2Sm, 1Krl, 2Krl, 1Krn, 2Krn, Ezd, Neh, Est, Job, Ps, Prz, Koh, Pnp, Iz, Jer, Lm, Ez, Dn, Hos, Jl, Am, Abd, Jon, Mi, Na, Ha, So, 
    Ag, Za, Ml, Mt, Mk, Łk, J, Dz, Rz, 1Kor, 2Kor, Ga, Ef, Flp, Kol, 1Tes, 2Tes, 1Tm, 2Tm, Tt, Flm, Hbr, Jk, 1P, 2P, 1J, 2J, 3J, Jd, Obj')
    parser.add_argument('chapter_verse', help='Numer rozdziału i wersetu (np. "1-1")')
    parser.add_argument('language', help='Język tekstu ("greek", "hebrew" lub "pl")')
    args = parser.parse_args()

    text, abbr_classes = retrieve_text(args.book, args.chapter_verse, args.language)

    if abbr_classes:
        print("\nKlasy abbr:")
        # Tworzenie pary (skrócona forma, fragment tekstu) i drukowanie
        for abbr, fragment in zip(abbr_classes, text.split('\n')):
            print(f"{abbr} : {fragment}")
    else:
        print(text)
                       
