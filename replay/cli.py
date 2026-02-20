import click
from replay.recorder import Recorder
from replay.runner import Runner
from replay.instructions import parse_instructions
import atexit
import time

@click.command()
@click.option('--record', '-r', help='Record mouse and keyboard actions into a file')
@click.option('--wait', '-w', help='Wait x seconds before recording or replaying', type=int)
@click.option('--precise', '-p', help='Enable extra time precision when recording', default=False, is_flag=True)
@click.option('--loop', '-l', help="Whether to loop a replay", default=False, is_flag=True)
@click.argument('file', required=False)
def replay(
    record: str,
    wait: int,
    precise: bool,
    loop: bool,
    file: str
):
    if wait:
        while wait:
            click.echo(wait)
            time.sleep(1)
            wait -= 1

    if record:
        recorder = Recorder(precise)

        atexit.register(lambda: recorder.save(record))

        click.echo("Started" if not precise else "Started (in precision mode)")
        recorder.start()
    elif file:
        while True:
            instructions = []

            click.echo(f"Replaying {file}")

            with open(file, 'r') as f:
                data = f.read()
                instructions = parse_instructions(data)

            runner = Runner(instructions)
            runner.start()

            if not loop:
                break
