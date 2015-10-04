from pybots.game.actions import Action
from pybots.game.fields.empty_field import EmptyField
from pybots.game.fields.player_field import PlayerField
from pybots.game.game import Game, WallError
from pybots.game.map import Map
from pybots.game.map_factory import MapFactory
from pybots.game.orientations import Orientation
from tests.pybots.pybots_test_case import TestCase


class TestGame(TestCase):
    def test_export(self):
        game_map = MapFactory().create()
        game = Game(game_map)

        self.assertCountEqual(
            game.export(),
            dict(map=game_map.export())
        )

    def test_action(self):
        game_map = Map(width=1, height=1)
        fake_map = [
            [PlayerField(Orientation.EAST), EmptyField()],
            [EmptyField(), EmptyField()],
        ]
        setattr(game_map, '_{}__map'.format(game_map.__class__.__name__), fake_map)
        game = Game(game_map)
        game._empty_player_positions = game._map.get_field_positions(PlayerField)

        fake_player_id = 'fake_player_id'

        game.action(fake_player_id, Action.TURN_RIGHT)
        self.assertEqual(
            game._map[game._players_positions[fake_player_id]].orientation,
            Orientation.SOUTH
        )

        game.action(fake_player_id, Action.TURN_LEFT)
        self.assertEqual(
            game._map[game._players_positions[fake_player_id]].orientation,
            Orientation.EAST
        )

        game.action(fake_player_id, Action.STEP)
        self.assertEqual(
            game._players_positions[fake_player_id],
            (1, 0)
        )

        with self.assertRaises(WallError):
            game.action(fake_player_id, Action.STEP)


