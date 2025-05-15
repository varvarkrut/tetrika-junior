import pytest
import os
import csv
from solution import (
    count_animals_by_letter,
    save_to_csv,
    get_animals_list,
)


@pytest.fixture
def sample_animals():
    return [
        "Аист",
        "Акула",
        "Антилопа",
        "Белка",
        "Бобр",
        "Волк",
        "Ворона",
        "Гадюка",
        "Газель",
        "Дельфин",
        "Динозавр",
    ]


def test_count_animals_by_letter():
    animals = ["Аист", "Акула", "Антилопа", "Белка", "Бобр", "Волк", "Ворона"]

    result = count_animals_by_letter(animals)

    assert result == {"А": 3, "Б": 2, "В": 2}
    assert result["А"] == 3
    assert result["Б"] == 2
    assert result["В"] == 2


def test_save_to_csv():
    letter_counts = {"А": 3, "Б": 2, "В": 2}
    test_filename = "test_beasts.csv"

    save_to_csv(letter_counts, test_filename)

    assert os.path.exists(test_filename)

    with open(test_filename, "r") as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)

        assert len(rows) == 3
        assert rows[0] == ["А", "3"]
        assert rows[1] == ["Б", "2"]
        assert rows[2] == ["В", "2"]

    os.remove(test_filename)


class MockResponse:
    def __init__(self, text):
        self.text = text


def test_get_animals_list(monkeypatch):
    """
    """
    html_page = """
    <div class="mw-category mw-category-columns">
        <div class="mw-category-group">
            <h3>А</h3>
            <ul>
                <li><a href="/wiki/Аист">Аист</a></li>
                <li><a href="/wiki/Акула">Акула</a></li>
            </ul>
        </div>
        <div class="mw-category-group">
            <h3>Б</h3>
            <ul>
                <li><a href="/wiki/Белка">Белка</a></li>
                <li><a href="/wiki/Бобр">Бобр</a></li>
            </ul>
        </div>
        <div class="mw-category-group">
            <h3>В</h3>
            <ul>
                <li><a href="/wiki/Волк">Волк</a></li>
                <li><a href="/wiki/Ворона">Ворона</a></li>
            </ul>
        </div>
    </div>
    """

    mock_response = MockResponse(html_page)

    def mock_get(*args, **kwargs):
        return mock_response

    monkeypatch.setattr("requests.get", mock_get)

    url = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"
    animals = get_animals_list(url)

    assert len(animals) == 6
    assert "Аист" in animals
    assert "Акула" in animals
    assert "Белка" in animals
    assert "Бобр" in animals
    assert "Волк" in animals
    assert "Ворона" in animals


def test_empty_animals_list():
    result = count_animals_by_letter([])
    assert result == {}


def test_special_characters():
    animals = ["Ёж", "1Аист", "2Слон", "_Муравей"]
    result = count_animals_by_letter(animals)
    assert result == {"Ё": 1, "1": 1, "2": 1, "_": 1}
