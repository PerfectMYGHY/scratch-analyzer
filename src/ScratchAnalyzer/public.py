from pathlib import Path


supported_languages = [
    "python",
    "python-pcode"
]

head_block_opcodes = [
    "event_whenflagclicked",
    "event_whenkeypressed",
    "event_whenthisspriteclicked",
    "event_whenbackdropswitchesto",
    "event_whengreaterthan",
    "event_whenbroadcastreceived",
    "control_start_as_clone",
    "procedures_definition"
]

entries_block_opcodes = [
    "event_whenflagclicked"
]

substack_opcodes = [
    "control_repeat",
    "control_forever",
    "control_if",
    "control_if_else",
    "control_repeat_until",
    "control_while"
]

substack_opcodes_need_flush = {
    "control_repeat": True,
    "control_forever": True,
    "control_if": False,
    "control_if_else": False,
    "control_repeat_until": True,
    "control_while": True
}

assets_root_path = Path(__file__).parent / "assets"
