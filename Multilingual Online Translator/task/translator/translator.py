from bs4 import BeautifulSoup
import requests


print('Type "en" if you want to translate from French into English, or "fr" if you want to translate from English into French:')
language = input()
print("Type the word you want to translate:")
word = input()

print('You chose "' + language + '" as the language to translate "' + word + '" to.')

if language == "en":
    url = "https://context.reverso.net/translation/french-english/" + word
else:
    url = "https://context.reverso.net/translation/english-french/" + word

r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

if r.status_code == 200:
    print("200 OK")
    print("Translations")
    soup = BeautifulSoup(r.content, "html.parser")
    translations = []
    div = soup.find("div", {"id": "translations-content"})
    for a in div.find_all("a"):
        translations.append(a.text.strip())
    print(translations)

    examples = []
    section = soup.find("section", {"id": "examples-content"})
    for span in section.find_all("span", {"class": "text"}):
        examples.append(span.text.strip())
    print(examples)

else:
    print("Try again?")
