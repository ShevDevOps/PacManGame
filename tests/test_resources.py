import pytest
from pathlib import Path

BASE_DIR = Path(".")

# --- Статичні файли ---
STATIC_FILES = [
    "map/mapData.txt",
    "tiles/cornerTile.png",
    "tiles/straightTile.png",
    "tiles/passageTile.png",
    "dots/dot.png",
    "dots/pill.png",
    "eaten/eaten.png",
    "cherry.png",
]

# Кадри Pac-Man
PACMAN_NORMAL_FRAMES = [f"pacman/frame_{i}.png" for i in range(8)]
PACMAN_GAMEOVER_FRAMES = [f"pacman/gameOver/frame_{i}.png" for i in range(42)]

# Кадри Привидів (звичайні)
GHOST_NAMES = ["blinky", "pinky", "inky", "clyde"]
GHOST_NORMAL_FRAMES = []
for name in GHOST_NAMES:
    for i in range(4):  # Напрямки (0-3)
        for j in range(2):  # Кадри анімації на напрямок (0-1)
            GHOST_NORMAL_FRAMES.append(f"{name}/frame_{i}_{j}.png")

# Кадри Привидів (налякані)
SCARED_FRAMES = [f"scared/scared_{i}.png" for i in range(2)]

# Збираємо ВСІ очікувані файли в один список
ALL_EXPECTED_FILES = (
    STATIC_FILES
    + PACMAN_NORMAL_FRAMES
    + PACMAN_GAMEOVER_FRAMES
    + GHOST_NORMAL_FRAMES
    + SCARED_FRAMES
)

# --- Тест за допомогою параметризації ---


@pytest.mark.parametrize("filepath_str", ALL_EXPECTED_FILES)
def test_resource_file_exists(filepath_str):
    """
    Перевіряє, чи існує вказаний файл ресурсу.
    """
    # Створюємо повний шлях до файлу
    resource_path = BASE_DIR / filepath_str

    # Використовуємо os.path.isfile або Path.is_file()
    assert (
        resource_path.is_file()
    ), f"Файл ресурсу НЕ знайдено: {resource_path.resolve()}"
    # assert os.path.isfile(resource_path),
    # f"Файл ресурсу НЕ знайдено: {os.path.abspath(resource_path)}"


# Додатковий тест для перевірки
# існування директорій (необов'язково, але корисно)
EXPECTED_DIRS = [
    "map",
    "tiles",
    "dots",
    "pacman",
    "pacman/gameOver",
    "blinky",
    "pinky",
    "inky",
    "clyde",
    "scared",
    "eaten",
]


@pytest.mark.parametrize("dirpath_str", EXPECTED_DIRS)
def test_resource_directory_exists(dirpath_str):
    """
    Перевіряє, чи існує вказана директорія ресурсів.
    """
    resource_path = BASE_DIR / dirpath_str
    assert (
        resource_path.is_dir()
    ), f"Директорія ресурсів НЕ знайдена: {resource_path.resolve()}"
