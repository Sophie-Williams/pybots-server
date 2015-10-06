from flask import jsonify
from flask.views import MethodView

from pybots.game.actions import Action
from pybots.game.game_controller import game_controller
from pybots.views.utils import form_to_kwargs, args_to_kwargs


class ActionView(MethodView):
    decorators = [form_to_kwargs, args_to_kwargs]

    def post(self, player_id=None, action=None, *args, **kwargs):
        if not all((player_id, action)):
            return 'Invalid request', 404

        game_controller.action(
            player_id,
            Action(int(action))
        )

        return jsonify(**game_controller.get(player_id).export()), 200
