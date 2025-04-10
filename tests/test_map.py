import pytest
from unittest.mock import MagicMock, patch
from main import Map, Tile, GhostState


@pytest.fixture
def simple_map_data():
    return """\
#####
#CDP#
# #G#
# g #
#####"""


@pytest.fixture
def game_map(simple_map_data):
    """Фікстура, що створює екземпляр Map для тестів."""
    with patch("main.pygame.sprite.Group", MagicMock()):
        m = Map(tileSize=16, data=simple_map_data)
        return m


def test_map_initialization(game_map, simple_map_data):
    """Тестує базову ініціалізацію карти: розміри, стартові позиції."""
    lines = simple_map_data.split("\n")
    expected_height = len(lines)
    expected_width = len(lines[0])

    assert game_map.height == expected_height
    assert game_map.width == expected_width
    assert isinstance(game_map.data[1][1], Tile)
    assert game_map.playerStartPos == (1, 1)  # 'C'
    assert game_map.ghostReturnGoal == (3, 2)  # 'G'
    assert game_map.ghostAfterReturnGoal == (2, 3)  # 'g'
    assert game_map.tileSize == 16


# Параметризація для тестування isWall
@pytest.mark.parametrize(
    "x, y, state, expected",
    [
        (0, 0, GhostState.NORMAL, True),  # Стіна '#'
        (1, 1, GhostState.NORMAL, False),  # Позиція 'C' (не стіна)
        (3, 2, GhostState.NORMAL, True),  # Позиція 'G' (стіна для NORMAL)
        (
            3,
            2,
            GhostState.EATEN,
            False,
        ),  # Позиція 'G' (стіна для EATEN, бо isRetPass=True)
        (3, 2, GhostState.AFTER_EATEN, False),
        # Позиція 'G' (стіна для AFTER_EATEN)
        (2, 3, GhostState.NORMAL, False),  # Позиція 'g' (не стіна для NORMAL)
        (2, 3, GhostState.EATEN, False),
        # Позиція 'g' (прохідна для EATEN)
        (2, 3, GhostState.AFTER_EATEN, False),
        # Позиція 'g' (прохідна для AFTER_EATEN)
        (-1, 1, GhostState.NORMAL, True),  # За межами зліва
        (1, -1, GhostState.NORMAL, True),  # За межами зверху
        (5, 1, GhostState.NORMAL, True),  # За межами справа  (width=5)
        (1, 5, GhostState.NORMAL, True),  # За межами знизу (height=5)
    ],
)
def test_map_is_wall(game_map, x, y, state, expected):
    """Тестує метод isWall з різними координатами та станами привида."""
    assert game_map.isWall(x, y, state) == expected


# Параметризація для isIntersect
@pytest.mark.parametrize(
    "px, py, expected",
    [
        (5, 5, True),
        # У лівому верхньому куті стіни (0*16, 0*16) -> tile (0,0)
        (24, 24, False),  # У центрі тайла 'C' (1*16+8, 1*16+8) -> tile (1,1)
        (17, 24, False),
        # На межі між (0,1) і (1,1) - ближче до (1,1) -> tile (1,1)
        (
            15,
            24,
            True,
        ),  # На межі між (0,1) і (1,1) - ближче до (0,1) -> tile (0,1) - Стіна
        (80, 20, True),  # За межами карти справа (5*16, ...)
        (20, 80, True),  # За межами карти знизу
    ],
)
def test_map_is_intersect(game_map, px, py, expected):
    """Тестує метод isIntersect
    для перевірки перетину піксельних координат зі стінами."""
    assert game_map.isIntersect(px, py) == expected


@patch("main.pygame.image.load")
@patch("main.pygame.transform.scale")
@patch("main.AlighnedSprite")
@patch.object(Map, "killSprites")
def test_map_update_dots(
    mock_kill, mock_aligned_sprite, mock_scale, mock_load, game_map
):
    """Тестує, що updateDots створює правильні спрайти для точок і пігулок."""
    mock_surface = MagicMock()
    mock_load.return_value = mock_surface
    mock_scale.return_value = mock_surface
    mock_aligned_sprite.return_value = MagicMock()

    game_map.updateDots()

    assert mock_kill.call_count == 2

    calls = mock_aligned_sprite.call_args_list
    dot_called = False
    pill_called = False
    for call in calls:
        args, kwargs = call
        map_arg, img_arg, x_arg, y_arg, *groups_arg = args
        if x_arg == 2 and y_arg == 1:
            dot_called = True
            assert groups_arg[0] is game_map.dots
        if x_arg == 3 and y_arg == 1:
            pill_called = True
            assert groups_arg[0] is game_map.powerPills

    assert dot_called, "AlighnedSprite не викликався для точки ('D')"
    assert pill_called, "AlighnedSprite не викликався для пігулки ('P')"
