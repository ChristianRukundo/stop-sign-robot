import time
from enum import Enum, auto


class RobotState(Enum):
    MOVING = auto()
    STOPPING = auto()


class StateMachine:
    """Manages the robot's state and the logic for transitions."""

    def __init__(self, stop_duration_s: int):
        self.current_state = RobotState.MOVING
        self._stop_duration = stop_duration_s
        self._stop_timer_start = 0
        self._last_signal = None

        self.MOVE_SIGNAL = b"0"
        self.STOP_SIGNAL = b"1"

    def update(self, stop_sign_detected: bool):
        """
        Updates the state based on detection and returns the signal to be sent.
        """
        if stop_sign_detected:
            self.current_state = RobotState.STOPPING
            self._stop_timer_start = time.time()

        if self.current_state == RobotState.STOPPING:
            if time.time() - self._stop_timer_start > self._stop_duration:
                self.current_state = RobotState.MOVING

    def get_signal(self) -> bytes:
        """Returns the appropriate signal based on the current state."""
        if self.current_state == RobotState.STOPPING:
            signal = self.STOP_SIGNAL
        else:
            signal = self.MOVE_SIGNAL

        if signal != self._last_signal:
            state_name = "STOP" if signal == self.STOP_SIGNAL else "MOVE"
            print(f"STATE CHANGE: Entering {state_name} state.")
        self._last_signal = signal

        return signal
