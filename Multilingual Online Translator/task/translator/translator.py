from bs4 import BeautifulSoup
import requests

languages = {
    '1': 'arabic',
    '2': 'german',
    '3': 'english',
    '4': 'spanish',
    '5': 'french',
    '6': 'hebrew',
    '7': 'japanese',
    '8': 'dutch',
    '9': 'polish',
    '10': 'portuguese',
    '11': 'romanian',
    '12': 'russian',
    '13': 'turkish'
}

print("Hello, you're welcome to the translator. Translator supports:")
for k, v in languages.items():
    print(k + ". " + v.capitalize())

print("Type the number of your language:")
language_from = input()
print("Type the number of language you want to translate to:")
language_to = input()
print("Type the word you want to translate:")
word = input()

url = "https://context.reverso.net/translation/" + languages.get(language_from) + "-" + languages.get(language_to) + "/" + word
language_to = languages.get(language_to).capitalize()

r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

if r.status_code == 200:
    print()
    print(language_to, "Translations:")

    soup = BeautifulSoup(r.content, "html.parser")
    translations = []
    div = soup.find("div", {"id": "translations-content"})
    for a in div.find_all("a"):
        translations.append(a.text.strip())
    print("\n".join(translations[:5]))
    print()

    examples = []
    section = soup.find("section", {"id": "examples-content"})
    for span in section.find_all("span", {"class": "text"}):
        examples.append(span.text.strip())
    print(language_to, "Examples:")
    print("\n\n".join(("\n".join(j for j in examples[i:i+2]) for i in range(0, 10, 2))))

else:
    print("Try again?")
