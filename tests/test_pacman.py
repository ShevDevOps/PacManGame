import pytest
from unittest.mock import MagicMock
from main import Pacman, Map


@pytest.fixture
def mock_map():
    map_mock = MagicMock(spec=Map)
    map_mock.tileSize = 16
    map_mock.playerStartPos = (5, 5)
    map_mock.isIntersect.return_value = False
    map_mock.width = 10
    map_mock.height = 10
    return map_mock


@pytest.fixture
def pacman_player(mock_map, mocker):
    """Creates an instance of Pacman with the dependencies loaded."""
    mocker.patch("main.pygame.image.load", return_value=MagicMock())
    mocker.patch("main.pygame.transform.scale", return_value=MagicMock())
    mocker.patch("main.pygame.transform.rotate", return_value=MagicMock())
    mocker.patch(
        "main.pygame.Rect",
        return_value=MagicMock(
            topleft=(
                mock_map.playerStartPos[0] * mock_map.tileSize,
                mock_map.playerStartPos[1] * mock_map.tileSize,
            )
        ),
    )  # Мокаємо Rect

    dummy_surface = MagicMock()
    frames = [[[dummy_surface]]]
    p = Pacman(map=mock_map, frames=frames, frameDuration=3)
    p.rect = MagicMock(
        topleft=(
            mock_map.playerStartPos[0] * mock_map.tileSize,
            mock_map.playerStartPos[1] * mock_map.tileSize,
        ),
        move=MagicMock(),
    )
    p.rect.move.return_value = p.rect

    p.rect.topleft = (
        mock_map.playerStartPos[0] * mock_map.tileSize,
        mock_map.playerStartPos[1] * mock_map.tileSize,
    )
    p.rect.topright = (
        mock_map.playerStartPos[0] * mock_map.tileSize + mock_map.tileSize - 1,
        mock_map.playerStartPos[1] * mock_map.tileSize,
    )
    p.rect.bottomleft = (
        mock_map.playerStartPos[0] * mock_map.tileSize,
        mock_map.playerStartPos[1] * mock_map.tileSize + mock_map.tileSize - 1,
    )
    p.rect.bottomright = (
        mock_map.playerStartPos[0] * mock_map.tileSize + mock_map.tileSize - 1,
        mock_map.playerStartPos[1] * mock_map.tileSize + mock_map.tileSize - 1,
    )

    return p


def test_pacman_initialization(pacman_player, mock_map):
    """Tests the initial state of Pacman."""
    start_px = mock_map.playerStartPos[0] * mock_map.tileSize
    start_py = mock_map.playerStartPos[1] * mock_map.tileSize
    assert pacman_player.rect.topleft == (start_px, start_py)
    assert pacman_player.speed == 2
    assert pacman_player.direction is None
    assert pacman_player.nextDirection is None
    assert pacman_player.map is mock_map


def test_pacman_reset(pacman_player, mock_map):
    """Tests Pacman state reset."""
    pacman_player.rect.topleft = (100, 100)
    pacman_player.direction = "up"
    pacman_player.nextDirection = "down"
    pacman_player.currentAnimation = 1
    pacman_player.currentFrame = 2
    pacman_player.angle = 90

    pacman_player.reset()

    start_px = mock_map.playerStartPos[0] * mock_map.tileSize
    start_py = mock_map.playerStartPos[1] * mock_map.tileSize
    assert pacman_player.rect.topleft == (start_px, start_py)
    assert pacman_player.direction is None
    assert pacman_player.nextDirection is None
    assert pacman_player.currentAnimation == 0
    assert pacman_player.currentFrame == 0
    assert pacman_player.angle == 0


def test_pacman_set_direction(pacman_player):
    """Tests the next direction setting."""
    pacman_player.setDirection("up")
    assert pacman_player.nextDirection == "up"
    assert pacman_player.directionCounter == pacman_player.directionDelay

    pacman_player.setDirection("up")
    assert pacman_player.nextDirection == "up"
    assert pacman_player.directionCounter == pacman_player.directionDelay

    pacman_player.directionCounter = 0
    pacman_player.setDirection("down")
    assert pacman_player.nextDirection == "down"
    assert pacman_player.directionCounter == pacman_player.directionDelay


@pytest.mark.parametrize(
    "direction, mock_isIntersect_side_effects, expected_can_move",
    [
        ("up", [False, False], True),  # Up freely (2 calls)
        ("up", [True, False], False),  # Up left wall (1 call)
        ("up", [False, True], False),  # Up right wall (2 calls)
        ("down", [False, False], True),  # Down freely (2 calls)
        ("down", [True, False], False),  # Down left wall (1 call)
        ("down", [False, True], False),  # Down right wall (2 calls)
        ("left", [False, False], True),  # Left freely (2 calls)
        ("left", [True, False], False),  # Top left wall (1 call)
        ("left", [False, True], False),  # Bottom left wall (2 calls)
        ("right", [False, False], True),  # Right freely (2 calls)
        ("right", [True, False], False),  # Top right wall (1 call)
        ("right", [False, True], False),  # Bottom right wall (2 calls)
    ],
)
def test_pacman_can_move(
    pacman_player, mock_map, direction,
    mock_isIntersect_side_effects, expected_can_move
):
    """Tests canMove logic with isIntersect soaking,
    taking into account short-circuiting."""
    mock_map.isIntersect.side_effect = mock_isIntersect_side_effects

    mock_map.isIntersect.reset_mock()

    result = pacman_player.canMove(direction)
    assert result == expected_can_move

    if mock_isIntersect_side_effects[0] is True:
        assert (
            mock_map.isIntersect.call_count == 1
        ), f"Очікувався 1 виклик isIntersect (short-circuit),\
        але було {mock_map.isIntersect.call_count}"
    else:
        assert (
            mock_map.isIntersect.call_count == 2
        ), f"Очікувалося 2 виклики isIntersect,\
        але було {mock_map.isIntersect.call_count}"


def test_pacman_get_tile(pacman_player, mock_map):
    """Tests the calculation of the tile on which Pacman is located."""
    px, py = 70, 85  # : tileSize=16 -> tile (4, 5)
    pacman_player.rect.topleft = (px, py)

    tile_x, tile_y = pacman_player.getTile()

    assert tile_x == px // mock_map.tileSize
    assert tile_y == py // mock_map.tileSize
