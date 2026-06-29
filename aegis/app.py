from rich.console import Console
from rich.panel import Panel

console = Console()


def main():
    console.clear()
    console.print(
        Panel.fit(
            "[bold cyan]AEGIS OS[/bold cyan]\n"
            "Autonomous Emergency & General Information System\n\n"
            "[green]System initialized successfully.[/green]",
            title="Boot",
        )
    )
