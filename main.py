import tkinter as tk
import requests
import googletrans
from bs4 import BeautifulSoup

translator = googletrans.Translator()
language = "en"
word_ru = ""


def get_english_words():
    url = "https://randomword.com/"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        english_words = soup.find("div", id="random_word").text.strip()
        word_definition = soup.find("div", id="random_word_definition").text.strip()
        return {
            "english_words": english_words,
            "word_definition": word_definition
        }
    except Exception as e:
        label_result.config(text="Произошла ошибка: {e}")
        return None


def word_game():
    global word_ru

    word_dict = get_english_words()
    language = "en"
    label_describe_ru.config(text="")
    label_result.config(text="")
    entry_word.delete(0, tk.END)
    label_text_lang.config(text="Введите слово на английском.")
    word_ru = ""

    if word_dict:
        word = word_dict.get("english_words")
        word_definition = word_dict.get("word_definition")
        label_text_en.config(text=f"{word_definition}")
        # Сохраняем слово в переменной, которую можно использовать в других функциях
        entry_word.word = word
        #translate(word, word_definition)



def reset_result():
    entry_word.delete(0, tk.END)
    label_result.config(text="")



def translate():
    if hasattr(entry_word, 'word'):  # Проверка, существует ли атрибут 'word'
        word = entry_word.word
        word_definition = label_text_en.cget("text")  # Получение текста из label_text_en
        word_ru = translator.translate(word, dest="ru").text
        word_definition_ru = translator.translate(word_definition, dest="ru").text
        label_describe_ru.config(text=word_definition_ru)
        return word_ru
    else:
        label_describe_ru.config(text="Сначала начните игру!")


def input_ru():
    if hasattr(entry_word, 'word'):  # Проверка, существует ли атрибут 'word'
        global language, word_ru
        word = entry_word.word
        #word_definition = label_text_en.cget("text")  # Получение текста из label_text_en
        word_ru = translator.translate(word, dest="ru").text
        #word_definition_ru = translator.translate(word_definition, dest="ru").text
        #label_describe_ru.config(text=word_definition_ru)
        label_text_lang.config(text="Введите слово на русском.")
        language = "ru"
        return language

    else:
        label_describe_ru.config(text="Сначала начните игру!")



def input_word():
    global language, word_ru
    if language == "en":
        user = entry_word.get()
        if user == entry_word.word:
            label_result.config(text="Вы угадали!")
        else:
            label_result.config(text=f"Ответ неверный, было загадано это слово - {entry_word.word}")
    elif language == "ru":
        user = entry_word.get()
        if user == word_ru:
            label_result.config(text="Вы угадали!")
        else:
            label_result.config(text=f"Ответ неверный, было загадано это слово - {word_ru}")



root = tk.Tk()
root.title("Угадай слово")

# кнопка "Начать игру"---------------------------------------------------
button_start_game = tk.Button(root, text="Начать игру", bg="grey", command=word_game)
button_start_game.grid(row=1, column=1, sticky="ew")

# ввод описания (en)---------------------------------------------------
label_text_en = tk.Label(text="Слово не загадано.")
label_text_en.grid(row=2, column=0, columnspan=3, sticky="ew")

# ввод описания (ru)---------------------------------------------------
label_describe_ru = tk.Label(text="Слово не загадано.")
label_describe_ru.grid(row=3, column=0, columnspan=3, sticky="ew")

# подсказка 1 (перевод описания)---------------------------------------------------
button_describe_ru = tk.Button(root, text="Подсказка 1", bg="grey", command=translate)
button_describe_ru.grid(row=2, column=3, sticky="ew")

# подсказка 2 (перевод слова)---------------------------------------------------
button_text_ru = tk.Button(root, text="Подсказка 2", bg="grey", command=input_ru)
button_text_ru.grid(row=3, column=3, sticky="ew")

# пояснение на каком языке выполнить ввод слова--------------------------------
label_text_lang = tk.Label(text="Введите слово на английском.")
label_text_lang.grid(row=5, column=0, columnspan=3, sticky="ew")

# ввод слова---------------------------------------------------
entry_word = tk.Entry(root, bg="yellow")
entry_word.grid(row=6, column=0, columnspan=3, sticky="ew")

button_input_word = tk.Button(root, text="ОК", bg="grey", command=input_word)
button_input_word.grid(row=6, column=3, sticky="ew")

# результирующее сообщение-------------------------------------------------
label_result = tk.Label(text="Результат: 0")
label_result.grid(row=7, column=0, columnspan=3, sticky="ew")

button_reset = tk.Button(root, text="Сброс", bg="grey", command=reset_result)
button_reset.grid(row=7, column=3, sticky="ew")

# запуск окна программы---------------------------------------------------
root.mainloop()