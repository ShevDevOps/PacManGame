import pytest
from main import Tile


# Параметризація для тестування різних типів тайлів
@pytest.mark.parametrize(
    "char, is_wall, has_dot, has_pill, is_ret_pass",
    [
        ("#", True, False, False, False),  # Стіна
        ("D", False, True, False, True),  # Точка
        ("P", False, False, True, True),  # Пігулка
        ("R", True, False, False, True),  # Стіна для повернення (Ghost Return)
        ("G", True, False, False, True),  # Стіна біля воріт (Ghost Gate)
        (" ", False, False, False, True),  # Порожній простір
        ("C", False, False, False, True),  # Стартова позиція гравця
        ("g", False, False, False, True),  # Позиція після повернення привида
    ],
)
def test_tile_initialization(char, is_wall, has_dot, has_pill, is_ret_pass):
    """Тестує правильність ініціалізації властивостей Tile."""
    tile = Tile(char)
    assert tile.isWall == is_wall
    assert tile.hasDot == has_dot
    assert tile.hasPill == has_pill
    assert tile.isRetPass == is_ret_pass
    # Перевірка, що 'R' та 'G' також є isWall
    if char in ("R", "G"):
        assert tile.isWall is True
