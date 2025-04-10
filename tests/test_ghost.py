import pytest
from unittest.mock import MagicMock, patch
from main import Ghost, GhostState, Map, Game


@pytest.fixture
def mock_map_for_ghost():
    map_mock = MagicMock(spec=Map)
    map_mock.tileSize = 16
    map_mock.isWall.return_value = False
    map_mock.width = 20
    map_mock.height = 20
    return map_mock


@pytest.fixture
def mock_game_for_ghost():
    game_mock = MagicMock(spec=Game)
    game_mock.pacman = MagicMock()
    game_mock.pacman.getTile.return_value = (10, 10)
    return game_mock


@pytest.fixture
def ghost_instance(mock_map_for_ghost, mock_game_for_ghost, mocker):
    mocker.patch("main.pygame.image.load", return_value=MagicMock())
    mocker.patch("main.pygame.transform.scale", return_value=MagicMock())
    mocker.patch(
        "main.pygame.Rect",
        return_value=MagicMock(topleft=(5 * 16, 5 * 16), move=MagicMock()),
    )

    dummy_surface = MagicMock()
    images = [
        [dummy_surface, dummy_surface],  # 0: left
        [dummy_surface, dummy_surface],  # 1: right
        [dummy_surface, dummy_surface],  # 2: down
        [dummy_surface, dummy_surface],  # 3: up
        [dummy_surface, dummy_surface],  # 4: scared
        [dummy_surface],  # 5: eaten
    ]
    target_func = lambda g: (10, 10)

    ghost = Ghost(
        map=mock_map_for_ghost,
        images=images,
        frameDuration=10,
        modes=[20, 10],
        speed=2,
        returnSpeed=4,
        scaredTime=30,
        targetFuction=target_func,
        startX=5,
        startY=5,
        scatterGoalX=1,
        scatterGoalY=1,
        returnGoalX=8,
        returnGoalY=8,
        afterReturnX=9,
        afterReturnY=9,
    )
    ghost.rect = MagicMock(topleft=(5 * 16, 5 * 16), move=MagicMock())
    ghost.rect.move.return_value = ghost.rect
    return ghost


def test_ghost_initialization(ghost_instance):
    assert ghost_instance.curX == 5
    assert ghost_instance.curY == 5
    assert ghost_instance.state == GhostState.NORMAL
    assert ghost_instance.currentMode == 0
    assert ghost_instance.modeDuartion == 20


def test_ghost_reset(ghost_instance):
    ghost_instance.curX = 10
    ghost_instance.curY = 10
    ghost_instance.state = GhostState.SCARED
    ghost_instance.currentMode = 1
    ghost_instance.modeDuartion = 5
    ghost_instance.rect.topleft = (100, 100)

    ghost_instance.reset()

    assert ghost_instance.curX == ghost_instance.startX
    assert ghost_instance.curY == ghost_instance.startY
    assert ghost_instance.state == GhostState.NORMAL
    assert ghost_instance.currentMode == 0
    assert ghost_instance.modeDuartion == ghost_instance.modes[0]
    assert ghost_instance.rect.topleft == (
        ghost_instance.startX * ghost_instance.map.tileSize,
        ghost_instance.startY * ghost_instance.map.tileSize,
    )


def test_ghost_update_mode_change(ghost_instance):
    ghost_instance.modeDuartion = 1
    ghost_instance.updateMode()
    assert ghost_instance.currentMode == 1
    assert ghost_instance.modeDuartion == ghost_instance.modes[1]


def test_ghost_update_mode_cycle(ghost_instance):
    ghost_instance.currentMode = len(ghost_instance.modes) - 1
    ghost_instance.modeDuartion = 1
    ghost_instance.updateMode()
    assert ghost_instance.currentMode == 0
    assert ghost_instance.modeDuartion == ghost_instance.modes[0]


def test_ghost_scare_when_normal(ghost_instance):
    ghost_instance.scare()
    assert ghost_instance.state == GhostState.SCARED
    assert ghost_instance.currentAnimation == 4
    assert ghost_instance.scaredTimer == ghost_instance.scaredTime


def test_ghost_scare_when_already_scared(ghost_instance):
    ghost_instance.state = GhostState.SCARED
    ghost_instance.scaredTimer = 10
    ghost_instance.scare()
    assert ghost_instance.state == GhostState.SCARED
    assert ghost_instance.scaredTimer == 10


def test_ghost_eat_when_scared(ghost_instance):
    ghost_instance.state = GhostState.SCARED
    ghost_instance.eat()
    assert ghost_instance.state == GhostState.EATEN
    assert ghost_instance.currentAnimation == 5
    assert ghost_instance.currentSpeed == ghost_instance.returnSpeed


def test_ghost_eat_when_not_scared(ghost_instance):
    initial_state = ghost_instance.state
    initial_animation = ghost_instance.currentAnimation
    initial_speed = ghost_instance.currentSpeed
    ghost_instance.eat()
    assert ghost_instance.state == initial_state
    assert ghost_instance.currentAnimation == initial_animation
    assert ghost_instance.currentSpeed == initial_speed


@patch("main.calcDistanceSqr")
def test_ghost_update_movement_decision_normal_chase(
    mock_calc_dist, ghost_instance, mock_map_for_ghost, mock_game_for_ghost
):
    """Tests direction selection in NORMAL (chase) mode."""
    ghost_instance.state = GhostState.NORMAL
    ghost_instance.currentMode = 0
    ghost_instance.rect.topleft = (5 * 16, 5 * 16)

    mock_calc_dist.side_effect = [
        100,  # (5, 4) - up
        50,  # (4, 5) - left
        150,  # (5, 6) - down
        25,  # (6, 5) - right -> Best
    ]
    ghost_instance.curX = 4
    ghost_instance.curY = 5
    mock_map_for_ghost.isWall.side_effect = lambda x, y, state: False

    ghost_instance.update(game=mock_game_for_ghost)

    assert ghost_instance.dX == ghost_instance.currentSpeed
    assert ghost_instance.dY == 0
    assert ghost_instance.currentAnimation == 1
    assert ghost_instance.curX == 5
    assert ghost_instance.curY == 5


@patch("main.random.choice")
def test_ghost_update_movement_decision_scared(
    mock_random_choice, ghost_instance, mock_map_for_ghost, mock_game_for_ghost
):
    """Tests direction selection in SCARED (random) mode."""
    ghost_instance.rect.topleft = (5 * 16, 5 * 16)
    ghost_instance.curX = 4
    ghost_instance.curY = 5

    ghost_instance.scare()

    mock_map_for_ghost.isWall.side_effect = lambda x, y, state: False

    down_direction_data = (0, 5, 6, 0, ghost_instance.currentSpeed, 2)
    mock_random_choice.return_value = down_direction_data

    ghost_instance.update(game=mock_game_for_ghost)

    assert ghost_instance.dX == 0
    assert ghost_instance.dY == ghost_instance.currentSpeed
    assert ghost_instance.currentAnimation == 4
    assert ghost_instance.curX == 5
    assert ghost_instance.curY == 5

    valid_directions = mock_random_choice.call_args[0][0]
    assert len(valid_directions) == 3  # up, down, right (left excluded)
    assert all(
        d[1] != 4 or d[2] != 5 for d in valid_directions
    )  # Excluded the reverse direction
