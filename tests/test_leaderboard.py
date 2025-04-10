import pytest
from unittest.mock import MagicMock
from main import LeaderBoard  # Замініть 'main'


# Мокаємо pygame_menu, щоб уникнути реальної ініціалізації UI
@pytest.fixture(autouse=True)
# Застосовуємо автоматично до всіх тестів у файлі
def mock_pygame_menu(mocker):
    mocker.patch("main.pygame_menu.Menu", return_value=MagicMock())
    mocker.patch("main.pygame_menu.events", MagicMock())
    mocker.patch("main.themes", MagicMock())


@pytest.fixture
def leaderboard():
    """Створює екземпляр LeaderBoard для тестів."""
    # Menu вже замокано за допомогою autouse=True
    lb = LeaderBoard(menuWidth=100, menuHeight=100)
    # Можна додатково мокати методи menu, якщо вони використовуються в __init__
    lb.menu.add = MagicMock()  # Мокаємо метод add у моканому меню
    return lb


def test_leaderboard_check_new_name(leaderboard):
    """Тестує перевірку імені, якого ще немає."""
    assert leaderboard.check("NewPlayer") is True
    assert leaderboard.message == ""


def test_leaderboard_check_existing_name(leaderboard):
    """Тестує перевірку імені, яке вже існує."""
    leaderboard.board = [("ExistingPlayer", 100)]  # Додаємо запис вручну
    assert leaderboard.check("ExistingPlayer") is False
    assert leaderboard.message == '"ExistingPlayer" is already taken'


def test_leaderboard_add_new_record(leaderboard):
    """Тестує додавання нового унікального запису."""
    result = leaderboard.add("Player1", 150)
    assert result is True
    assert ("Player1", 150) in leaderboard.board
    # Перевіряємо, чи викликався метод додавання мітки в меню
    leaderboard.menu.add.label.assert_called_with("Player1 - 150")


def test_leaderboard_add_duplicate_record(leaderboard):
    """Тестує спробу додавання запису з існуючим іменем."""
    leaderboard.add("Player1", 150)  # Додаємо перший раз
    leaderboard.menu.add.label.reset_mock()  # Скидаємо лічильник викликів

    result = leaderboard.add("Player1", 200)  # Спробуємо додати знову
    assert result is False
    # Перевіряємо, що другий запис не додався
    assert len(leaderboard.board) == 1
    assert leaderboard.board[0] == ("Player1", 150)  # Старий запис залишився
    # Перевіряємо, що мітка в меню не додавалася вдруге
    leaderboard.menu.add.label.assert_not_called()
