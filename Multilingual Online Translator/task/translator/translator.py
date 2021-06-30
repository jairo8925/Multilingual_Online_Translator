from bs4 import BeautifulSoup
import requests


s = requests.Session()

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


def save_to_file(filename, language, translation, sentence_from, sentence_to):
    word_file = open(filename, "a", encoding="utf-8")
    word_file.write(language + " Translations:\n")
    word_file.write(translation + "\n\n")
    word_file.write(language + " Example:\n")
    word_file.write(sentence_from + "\n")
    word_file.write(sentence_to + "\n\n\n")
    word_file.close()


def translate(src, dest, word):
    url = "https://context.reverso.net/translation/" + src + "-" + dest + "/" + word
    language = dest.capitalize()
    r = s.get(url, headers={'User-Agent': 'Mozilla/5.0'})

    if r.status_code == 200:
        print()
        print(language, "Translations:")

        soup = BeautifulSoup(r.content, "html.parser")
        div = soup.find("div", {"id": "translations-content"})
        translation = div.find("a").text.strip()
        print(translation)
        print()

        section = soup.find("section", {"id": "examples-content"})
        examples = [t.text.strip() for t in section.find_all("span", {"class": "text"})]
        print(language, "Example:")
        sentence_from = examples[0]
        sentence_to = examples[1]
        print(sentence_from)
        print(sentence_to)
        print()

        save_to_file(word + ".txt", language, translation, sentence_from, sentence_to)

    else:
        print("Try again?")


def main():
    print("Hello, you're welcome to the translator. Translator supports:")
    for num, lang in languages.items():
        print(num + ". " + lang.capitalize())

    print("Type the number of your language:")
    language_from = input()
    print("Type the number of a language you want to translate to or '0' to translate to all languages:")
    language_to = input()
    print("Type the word you want to translate:")
    word_to_translate = input()

    if language_to == "0":
        for i in range(1, 14):
            if str(i) == language_from:
                continue
            translate(languages.get(language_from), languages.get(str(i)), word_to_translate)
    else:
        translate(languages.get(language_from), languages.get(language_to), word_to_translate)


if __name__ == "__main__":
    main()
