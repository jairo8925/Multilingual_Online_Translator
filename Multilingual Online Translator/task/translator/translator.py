import requests
import sys
from bs4 import BeautifulSoup


s = requests.Session()

languages = {
    1: 'arabic',
    2: 'german',
    3: 'english',
    4: 'spanish',
    5: 'french',
    6: 'hebrew',
    7: 'japanese',
    8: 'dutch',
    9: 'polish',
    10: 'portuguese',
    11: 'romanian',
    12: 'russian',
    13: 'turkish'
}


def save_to_file(filename, language, translations, examples):
    word_file = open(filename, "a", encoding="utf-8")
    word_file.write(f"{language} Translations:\n")

    for t in translations[:min(5, len(translations))]:
        word_file.write(t)
    word_file.write("\n")

    if len(examples) == 2:
        word_file.write(f"{language} Example:\n")
    else:
        word_file.write(f"{language} Examples:\n")

    word_file.write("\n\n".join(("\n".join(j for j in examples[i:i+2]) for i in range(0, min(5, len(examples)), 2))))
    word_file.write("\n\n\n")
    word_file.close()


def translate(src, dest, word, multiple):
    url = "https://context.reverso.net/translation/" + src + "-" + dest + "/" + word
    language = dest.capitalize()
    r = s.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, "html.parser")
        div = soup.find("div", {"id": "translations-content"})
        translations = []
        a_tags = div.find_all("a")

        for a in a_tags:
            translations.append(a.text.strip() + "\n")

        section = soup.find("section", {"id": "examples-content"})
        examples = [t.text.strip() for t in section.find_all("span", {"class": "text"})]

        if multiple:
            output(language, translations, examples, True)
            save_to_file(f"{word}.txt", language, translations[:1], examples[:2])
        else:
            output(language, translations, examples, False)
            save_to_file(f"{word}.txt", language, translations, examples)
    elif r.status_code == 404:
        print(f"Sorry, unable to find {word}")
        sys.exit()
    else:
        print("Something wrong with your internet connection")
        sys.exit()


def output(language, translations, examples, multiple_outputs):
    print(f"{language} Translations:")
    if multiple_outputs:
        print(translations[0])
        print(f"{language} Example:")
        print(examples[0])
        print(examples[1])
    else:
        print("".join(translations[:min(5, len(translations))]))
        print(f"{language} Examples:")
        print("\n\n".join(("\n".join(j for j in examples[i:i+2]) for i in range(0, min(5, len(examples)), 2))))
    print("\n")


def main():
    args = sys.argv
    language_from = args[1]
    language_to = args[2]
    word_to_translate = args[3]

    if language_from not in languages.values():
        print(f"Sorry, the program doesn't support {language_from}")
        sys.exit()
    elif language_to != "all" and language_to not in languages.values():
        print(f"Sorry, the program doesn't support {language_to}")
        sys.exit()
    else:
        if language_to == "all":
            for i in range(1, 14):
                if languages.get(i) == language_from:
                    continue
                translate(language_from, languages.get(i), word_to_translate, True)
        else:
            translate(language_from, language_to, word_to_translate, False)


if __name__ == "__main__":
    main()
