import csv
import requests
from bs4 import BeautifulSoup
from collections import defaultdict

ANIMAL_SELECTOR = "div.mw-category.mw-category-columns div.mw-category-group a"
NEXT_PAGE_TEXT = "Следующая страница"
WIKI_BASE_URL = "https://ru.wikipedia.org"


def get_animals_list(url: str) -> list:
    """
    Получает список животных с указанной страницы Википедии.

    :param url: URL страницы с категорией животных
    :type url: str
    :return: список названий животных
    :rtype: list
    """
    animals = []
    current_url = url
    processed_urls = set()

    while current_url and current_url not in processed_urls:
        print("Обработка страницы: " + current_url)
        processed_urls.add(current_url)

        try:
            response = requests.get(current_url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            animal_tags = soup.select(ANIMAL_SELECTOR)
            for tag in animal_tags:
                animals.append(tag.text)

            next_url = None
            for link in soup.find_all("a"):
                if link.text.strip() == NEXT_PAGE_TEXT:
                    next_url = WIKI_BASE_URL + link["href"]
                    break

            current_url = next_url

        except Exception as e:
            print("Ошибка при обработке страницы: " + str(e))
            break

    print("Всего найдено животных: " + str(len(animals)))
    return animals


def count_animals_by_letter(animals: list) -> dict:
    """
    Подсчитывает количество животных по первой букве.

    :param animals: список названий животных
    :type animals: list
    :return: словарь с подсчетом по буквам
    :rtype: dict
    """
    letter_counts = defaultdict(int)

    for animal in animals:
        if animal:
            first_letter = animal[0].upper()
            letter_counts[first_letter] += 1

    return dict(letter_counts)


def save_to_csv(letter_counts: dict, filename: str) -> None:
    """
    Сохраняет результаты подсчета в CSV файл.

    :param letter_counts: словарь с подсчетом по буквам
    :type letter_counts: dict
    :param filename: имя файла для сохранения
    :type filename: str
    """
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)

        for letter, count in sorted(letter_counts.items()):
            csv_writer.writerow([letter, count])


def main() -> None:
    """
    Основная функция программы.
    """
    url = WIKI_BASE_URL + "/wiki/Категория:Животные_по_алфавиту"
    filename = "beasts.csv"

    animals = get_animals_list(url)

    letter_counts = count_animals_by_letter(animals)

    save_to_csv(letter_counts, filename)

    print("Данные сохранены в файл: " + filename)


if __name__ == "__main__":
    main()
