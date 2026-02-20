from replay.instructions import Instruction, InstructionCode, is_special, KEY_MAPPING, CLICK_MAPPING
from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
import time
import os
import subprocess

class Runner:
    def __init__(self, instructions: list[Instruction]):
        self.instructions = instructions
        self.keyboard = KeyboardController()
        self.mouse = MouseController()

    def start(self):
        for instruction in self.instructions:
            code = instruction.code
            arg = instruction.arg

            match code:
                case InstructionCode.KEYPRESS:
                    self._press(arg)
                    self._release(arg)
                case InstructionCode.KEYPRESSIN:
                    self._press(arg)
                case InstructionCode.KEYPRESSOUT:
                    self._release(arg)
                case InstructionCode.MOUSEMOVE:
                    self.mouse.position = (arg.x, arg.y)
                case InstructionCode.MOUSECLICK:
                    self._click(arg)
                    self._clickout(arg)
                case InstructionCode.MOUSECLICKIN:
                    self._click(arg)
                case InstructionCode.MOUSECLICKOUT:
                    self._clickout(arg)
                case InstructionCode.MOUSESCROLL:
                    self.mouse.scroll(arg.x, arg.y)
                case InstructionCode.WAIT:
                    time.sleep(float(arg) / 1000)
                case InstructionCode.CMD:
                    proc = subprocess.Popen(arg)

    def _press(self, arg):
        if is_special(arg):
            self.keyboard.press(KEY_MAPPING[arg])
        else:
            self.keyboard.press(arg)

    def _release(self, arg):
        if is_special(arg):
            self.keyboard.release(KEY_MAPPING[arg])
        else:
            self.keyboard.release(arg)

    def _click(self, arg):
        self.mouse.press(CLICK_MAPPING[arg] if arg else Button.left)

    def _clickout(self, arg):
        self.mouse.release(CLICK_MAPPING[arg] if arg else Button.left)


