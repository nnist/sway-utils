#!/bin/python3
import time
from dataclasses import dataclass
from typing import List

from rich.align import Align
from rich.console import Console
from rich.live import Live


@dataclass
class Frame:
    text: str
    delay: float


console = Console()
console.clear()

FRAMES: List[Frame] = [
    Frame(
        """[red]
            
            
─────────────
""",
        0.1,
    ),
    Frame(
        """[red]
            
   SUSPEND  
─────────────
""",
        0.1,
    ),
    Frame(
        """[red]
┌───────────┐
   SUSPEND    
└───────────┘
""",
        0.03,
    ),
    Frame(
        """[red]
┌───────────┐
   SUSPEND    
└───────────┘
""",
        0.05,
    ),
    Frame(
        """[red]
▗▄▄▄▄▄▄▄▄▄▄▄▖
▐███████████▌
▝▀▀▀▀▀▀▀▀▀▀▀▘
""",
        0.18,
    ),
    Frame(
        """[red]
┌───────────┐
   [bold]SUSPEND[not bold]
└───────────┘
""",
        0.6,
    ),
]

with Live(Align("", align="center"), refresh_per_second=60, transient=True) as live:
    for frame in FRAMES:
        live.update(Align(frame.text, align="center", vertical="middle"))
        time.sleep(frame.delay)
