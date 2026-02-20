import enum
from dataclasses import dataclass
from pynput.keyboard import Key
from pynput.mouse import Button

@dataclass
class Pair:
    """
    Pair of two values
    """
    x: int
    y: int

class InstructionCode(enum.Enum):
    KEYPRESS = "KEYPRESS"
    KEYPRESSIN = "KEYPRESSIN"
    KEYPRESSOUT = "KEYPRESSOUT"
    MOUSEMOVE = "MOUSEMOVE"
    MOUSECLICK = "MOUSECLICK"
    MOUSECLICKIN = "MOUSECLICKIN"
    MOUSECLICKOUT = "MOUSECLICKOUT"
    MOUSESCROLL = "MOUSESCROLL"
    WAIT = "WAIT"
    CMD = "CMD"

class Instruction:
    def __init__(self, code: InstructionCode, arg: str | Pair | None = None) -> None:
        self.code = code
        self.arg = arg

# Mapping of instruction keys to pynput
KEY_MAPPING = {
    "<alt>": Key.alt,
    "<alt_l>": Key.alt_l,
    "<alt_r>": Key.alt_r,
    "<alt_gr>": Key.alt_gr,
    "<backspace>": Key.backspace,
    "<caps>": Key.caps_lock,
    "<meta>": Key.cmd,
    "<meta_l>": Key.cmd_l,
    "<meta_r>": Key.cmd_r,
    "<ctrl>": Key.ctrl,
    "<ctrl_l>": Key.ctrl_l,
    "<ctrl_r>": Key.ctrl_r,
    "<delete>": Key.delete,
    "<arrow_down>": Key.down,
    "<end>": Key.end,
    "<enter>": Key.enter,
    "<esc>": Key.esc,
    "<f1>": Key.f1,
    "<f2>": Key.f2,
    "<f3>": Key.f3,
    "<f4>": Key.f4,
    "<f5>": Key.f5,
    "<f6>": Key.f6,
    "<f7>": Key.f7,
    "<f8>": Key.f8,
    "<f9>": Key.f9,
    "<f10>": Key.f10,
    "<f11>": Key.f11,
    "<f12>": Key.f12,
    "<f13>": Key.f13,
    "<f14>": Key.f14,
    "<f15>": Key.f15,
    "<f16>": Key.f16,
    "<f17>": Key.f17,
    "<f18>": Key.f18,
    "<f19>": Key.f19,
    "<f20>": Key.f20,
    "<home>": Key.home,
    "<left>": Key.left,
    "<page_down>": Key.page_down,
    "<page_up>": Key.page_up,
    "<arrow_right>": Key.right,
    "<shift>": Key.shift,
    "<shift_l>": Key.shift_l,
    "<shift_r>": Key.shift_r,
    "<space>": Key.space,
    "<tab>": Key.tab,
    "<arrow_up>": Key.up
}
KEY_MAPPING_REVERSE = {v: k for k, v in KEY_MAPPING.items()}

CLICK_MAPPING = {
    "<left>": Button.left,
    "<middle>": Button.middle,
    "<right>": Button.right
}
CLICK_MAPPING_REVERSE = {v: k for k, v in CLICK_MAPPING.items()}

def parse_pair(s: str) -> Pair:
    if not s.startswith('<') or not s.endswith('>'):
        raise ValueError(f'{s} is not a valid pair')
    pairs = s[1:][:-1].split(',')

    return Pair(int(pairs[0]), int(pairs[1]))

def is_special(s: str):
    return s.startswith('<') and s.endswith('>')

def parse_instruction(s: str):
    items = s.split(' ')
    code = InstructionCode(items[0])
    arg = ' '.join(items[1:])
    match code:
        case InstructionCode.MOUSEMOVE | InstructionCode.MOUSESCROLL:
            arg = parse_pair(arg)
    return Instruction(code, arg)

def parse_instructions(s: str):
    results: list[Instruction] = []
    statements = s.split('\n')

    for statement in statements:
        if statement == '' or statement.startswith(';'): # Ignore empty lines or lines starting with ;
            continue
        results.append(parse_instruction(statement))

    return results

def encode_instruction(instruction: Instruction) -> str:
    code = instruction.code.value
    arg = instruction.arg
    if isinstance(arg, Pair):
        arg = f"<{arg.x}, {arg.y}>"
    if arg:
        return f"{code} {arg}"
    else:
        return code

def encode_instructions(instructions: list[Instruction]) -> str:
    result = ""
    for instruction in instructions:
        result += encode_instruction(instruction) + '\n'
    return result
