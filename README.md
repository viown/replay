# replay

Simplle utility for recording and replaying keyboard and mouse actions.

## Installation

```
pip install git+https://github.com/viown/replay
```

## Usage

### Start record
```
replay --record my_macro.rep
```

Addtiional options can be used when recording:
- `-w [seconds]` - Wait a specific number of seconds before recording.
- `-p` - Millisecond-precise recording. Will result in a significantly larger file. (disabled by default)
- - With precise disabled, you can expect inaccuracies to be within ~50 ms.

### Replay
```
replay my_macro.rep
```

Options:
- `-l` - Loop the macro

## Instructions

The generated file is a list of simple text-based instructions for how to replay a macro.

- `KEYPRESS` - A combination of both `KEYPRESSIN` and `KEYPRESSOUT`
- - `KEYPRESSIN`
- - `KEYPRESSOUT`
- `MOUSEMOVE` - Move the mouse to a specific location on the screen
- `MOUSECLICK` - Click the mouse. Without any arguments, will click left. Otherwise, specify `<middle>` or `<right>`
- - `MOUSECLICKIN`
- - `MOUSECLICKOUT`
- `MOUSESCROLL` - Scroll the mouse
- `WAIT` - Wait a specific number of milliseconds
- `CMD` - Run a command. This is not typically generated when recording, but can be added manually, for e.g, to initialize the macro by starting an application.

This looks like this:

```
; Macro to echo "Hi"

CMD terminal
WAIT 1000
KEYPRESS e
KEYPRESS c
KEYPRESS h
KEYPRESS o
KEYPRESS <space>
KEYPRESS H
KEYPRESS i
KEYPRESS <enter>
```

Mouse:

```
; move to (1, 2) on the screen
MOUSEMOVE <1, 2>
; at current location, scroll 10 steps up
MOUSESCROLL <0, 10>
```
