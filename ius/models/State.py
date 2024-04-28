import enum


class State(enum.Enum):
    START_STATE = 9
    EMPTY_TANK_STATE = 1

    # Состояния для бурного брожения
    # FILL_FF_TANK = 2
    PRE_FERMENTATION = 3
    FAST_FERMENTATION = 4
    # DRAIN_FF_TANK = 5

    # Состояния для тихого брожения
    # FILL_SF_TANK = 6
    SLOW_FERMENTATION = 7
    # DRAIN_SF_TANK = 8

    EMERGENCY_STOP = 10

    FILL_TANK = 11
    DRAIN_TANK = 12
