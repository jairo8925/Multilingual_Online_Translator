from bs4 import BeautifulSoup
import requests


print('Type "en" if you want to translate from French into English, or "fr" if you want to translate from English into French:')
language = input()
print("Type the word you want to translate:")
word = input()

print('You chose "' + language + '" as the language to translate "' + word + '" to.')


if language == "en":
    url = "https://context.reverso.net/translation/french-english/" + word
    language = "English"
else:
    url = "https://context.reverso.net/translation/english-french/" + word
    language = "French"

r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

if r.status_code == 200:
    print("200 OK")
    print()
    print(language, "Translations:")

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
    print(language, "Examples:")
    print("\n\n".join(("\n".join(j for j in examples[i:i+2]) for i in range(0, 10, 2))))

else:
    print("Try again?")
