import pytest
from unittest.mock import MagicMock
from main import Settings, Map, Game, Pacman


@pytest.fixture(autouse=True)
def mock_pygame_menu(mocker):
    menu_add_mock = MagicMock()
    menu_mock = MagicMock()
    menu_mock.add = menu_add_mock

    mocker.patch("main.pygame_menu.Menu", return_value=menu_mock)
    mocker.patch("main.pygame_menu.events", MagicMock())
    mocker.patch("main.themes", MagicMock())


@pytest.fixture
def mock_dependencies():
    """Creates mocks for Settings dependencies."""
    mock_map = MagicMock(spec=Map)
    mock_map.generateImage = MagicMock()
    mock_game = MagicMock(spec=Game)
    mock_pacman = MagicMock(spec=Pacman)
    return mock_map, mock_game, mock_pacman


@pytest.fixture
def settings_instance(mock_dependencies):
    """Створює екземпляр Settings з моками."""
    mock_map, mock_game, mock_pacman = mock_dependencies
    s = Settings(
        map=mock_map, game=mock_game,
        player=mock_pacman, menuWidth=100, menuHeight=100
    )
    return s


def test_settings_initialization(settings_instance):
    """Tests that settings are created and menus are configured."""
    assert settings_instance.menu.add.selector.call_count >= 2
    settings_instance.menu.add.button.assert_any_call(
        "Back", settings_instance.menu.add.button.call_args[0][1]
    )


def test_settings_set_lives(settings_instance, mock_dependencies):
    """Testing the change in the number of lives in the game."""
    mock_map, mock_game, mock_pacman = mock_dependencies
    settings_instance.set_lives(None, 1)
    assert mock_game.startLives == 1
    assert mock_game.lives == 1


def test_settings_set_color_background(settings_instance, mock_dependencies):
    """Tests changing the background color
    and updating the background image."""
    mock_map, mock_game, mock_pacman = mock_dependencies
    new_color = (10, 20, 30)
    settings_instance.set_color_background(None, new_color)

    assert mock_map.color_background == new_color
    mock_map.generateImage.assert_called_once()
    assert mock_game.background == mock_map.generateImage.return_value
