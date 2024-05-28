import os
import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import commands

# Funkcja do pobierania tekstu z internetu lub z pliku
def retrieve_text(book, chapter_verse, language):
    filename = f"{book}_{chapter_verse}_{language}.txt"

    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            file_content = file.read()
            if "\n\nKlasy abbr:\n" in file_content:
                text, abbr_section = file_content.split("\n\nKlasy abbr:\n")
                abbr_classes = abbr_section.strip().split('\n')
            else:
                text = file_content
                abbr_classes = None
            return text, abbr_classes
    else:
        if language == 'pl':
            url = f'http://bibliepolskie.pl/zzteksty_wer.php?book={book_name_to_number(book)}&chapter={chapter_verse.split("-")[0]}&verse={chapter_verse.split("-")[1]}'
        else:
            url = f'https://biblehub.com/texts/{book}/{chapter_verse}.htm'

        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            if language == 'pl':
                text, abbr_classes = retrieve_pl_text(soup)
            else:
                if language == 'greek':
                    first_element = soup.find(class_='greek')
                elif language == 'hebrew':
                    first_element = soup.find(class_='heb')
                else:
                    return "Nieprawidłowy język. Dostępne opcje to 'greek', 'hebrew' lub 'pl'.", []

                if first_element:
                    text = first_element.text.replace('\n', '').strip()
                    abbr_classes = []
                else:
                    text = f"Nie znaleziono elementu w języku '{language}' na stronie: {url}"
                    abbr_classes = []

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
    tdwtext_elements = soup.find_all(class_='tdwtext')
    tdwtext_text = ""
    abbr_classes = []

    for element in tdwtext_elements:
        tdwtext_text += element.text.strip() + "\n"
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
    return bible_books.get(name, "Nie znaleziono księgi w biblii.")

# Inicjalizacja bota
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Komenda bota
@bot.command()
async def biblia(ctx, book: str, chapter_verse: str, language: str):
    text, abbr_classes = retrieve_text(book, chapter_verse, language)

    if abbr_classes:
        result = "\n:\n"
        for abbr, fragment in zip(abbr_classes, text.split('\n')):
            result += f"{abbr} : {fragment}\n"
        await ctx.send(result)
    else:
        await ctx.send(text)

# Uruchomienie bota
bot.run('Token')
