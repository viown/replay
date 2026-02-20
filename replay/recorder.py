from pynput import mouse, keyboard
from replay.instructions import InstructionCode, Instruction, Pair, encode_instructions, KEY_MAPPING_REVERSE, CLICK_MAPPING_REVERSE
import time

class Recorder:
    """
    Record keyboard and mouse actions into instructions
    """
    def __init__(self, precise: bool = False):
        self.instructions: list[Instruction] = []
        self.precise = precise

        self.counter = time.perf_counter()

        self._mouse_listener = mouse.Listener(
            on_move=self._on_move,
            on_click=self._on_click,
            on_scroll=self._on_scroll
        )

        self._keyboard_listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )

    def start(self):
        self._mouse_listener.start()
        
        with self._keyboard_listener as listener:
            listener.join()

    def save(self, filename):
        with open(filename, 'w', encoding='UTF-8') as f:
            f.write(encode_instructions(self.instructions))

    def _add_wait(self):
        diff = time.perf_counter() - self.counter
        if self.precise or diff > 0.05:
            diff_ms = round(diff * 1000, 3)
            self.instructions.append(Instruction(InstructionCode.WAIT, str(diff_ms)))
        self.counter = time.perf_counter()

    ### Mouse events

    def _on_move(self, x: int, y: int):
        self._add_wait()
        self.instructions.append(Instruction(InstructionCode.MOUSEMOVE, Pair(x, y)))

    def _on_click(self, x: int, y: int, button, pressed: bool):
        self._add_wait()
        if pressed:
            self.instructions.append(Instruction(InstructionCode.MOUSECLICKIN, CLICK_MAPPING_REVERSE[button]))
        else:
            self.instructions.append(Instruction(InstructionCode.MOUSECLICKOUT, CLICK_MAPPING_REVERSE[button]))

    def _on_scroll(self, x: int, y: int, dx: int, dy: int):
        self._add_wait()
        self.instructions.append(Instruction(InstructionCode.MOUSESCROLL, Pair(dx, dy)))

    ### Keyboard events

    def _on_press(self, key):
        self._add_wait()
        if isinstance(key, keyboard.KeyCode):
            self.instructions.append(Instruction(InstructionCode.KEYPRESSIN, key.char))
        elif isinstance(key, keyboard.Key):
            self.instructions.append(Instruction(InstructionCode.KEYPRESSIN, KEY_MAPPING_REVERSE[key]))

    def _on_release(self, key):
        self._add_wait()
        if isinstance(key, keyboard.KeyCode):
            self.instructions.append(Instruction(InstructionCode.KEYPRESSOUT, key.char))
        elif isinstance(key, keyboard.Key):
            self.instructions.append(Instruction(InstructionCode.KEYPRESSOUT, KEY_MAPPING_REVERSE[key]))
