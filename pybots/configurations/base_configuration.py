from abc import ABCMeta
from types import MethodType

from pybots.configurations import ConfigurationError
from pybots.configurations.field_placer import FieldPlacerMixin
from pybots.game.fields.empty_field import EmptyField


class BaseConfiguration(FieldPlacerMixin, metaclass=ABCMeta):
    map_width = None
    map_height = None
    bots = None
    treasures = None
    blocks = None

    default_empty_map_field = EmptyField
    rounded_game = False
    maze_game = False
    battery_game = False
    laser_game = False

    _fields = dict(
        map_width=int,
        map_height=int,
        bots=int,
        treasures=int,
        blocks=int,
        default_empty_map_field=object,
        rounded_game=bool,
        maze_game=bool,
        battery_game=bool,
        laser_game=bool,
    )

    def __init__(self):
        missing = []
        for field_name, field_type in self._fields.items():
            value = getattr(self, field_name, None)

            if value is None:
                missing.append(field_name)
                continue

            if field_type:
                if isinstance(value, MethodType):
                    lambda_ = getattr(self.__class__, field_name)
                    setattr(self.__class__, field_name, property(lambda _: lambda_()))

                    if not isinstance(lambda_(), field_type):
                        missing.append(field_name)
                        continue

                elif not isinstance(value, field_type):
                    missing.append(field_name)
                    continue

        if missing:
            raise ConfigurationError("Please provide all configuration fields, '{}' not found or isn't in correct type."
                                     .format(', '.join(missing)), missing)
