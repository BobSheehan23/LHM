#!/usr/bin/env python3
"""
Lighthouse Macro — Command Line Interface
"""

import sys
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core import get_config
from src.collectors import FREDCollector
from src.charting import LHMChart, set_lhm_style
from src.ai import BeaconWorkflow, BeamWorkflow, ChartbookWorkflow, HorizonWorkflow

console = Console()


@click.group()
def cli():
    """Lighthouse Macro Intelligence Pipeline"""
    pass


@cli.command()
def status():
    """Check system status and API key configuration"""
    config = get_config()
    api_status = config.validate_api_keys()

    table = Table(title="Lighthouse Macro — System Status")
    table.add_column("Component", style="cyan")
    table.add_column("Status", style="green")

    table.add_row("FRED API", "✓ Configured" if api_status["fred"] else "✗ Missing")
    table.add_row("Google API", "✓ Configured" if api_status["google"] else "✗ Missing")
    table.add_row("Anthropic (Claude)", "✓ Configured" if api_status["anthropic"] else "✗ Missing")
    table.add_row("OpenAI (GPT)", "✓ Configured" if api_status["openai"] else "✗ Missing")
    table.add_row("Grok (xAI)", "✓ Configured" if api_status["grok"] else "✗ Missing")
    table.add_row("Perplexity", "✓ Configured" if api_status["perplexity"] else "✗ Missing")
    table.add_row("Gemini (Google)", "✓ Configured" if api_status["gemini"] else "✗ Missing")
    table.add_row("Substack", "✓ Configured" if api_status["substack"] else "✗ Missing")
    table.add_row("Twitter", "✓ Configured" if api_status["twitter"] else "✗ Missing")

    console.print(table)


@cli.group()
def collect():
    """Data collection commands"""
    pass


@collect.command()
@click.option("--pillar", type=click.Choice(["macro_dynamics", "monetary_mechanics", "market_technicals"]), help="Collect all series for a pillar")
@click.option("--series", help="Collect specific series by ID")
@click.option("--start-date", help="Start date (YYYY-MM-DD)")
def fred(pillar, series, start_date):
    """Collect FRED data"""
    collector = FREDCollector()

    if pillar:
        console.print(f"[cyan]Collecting {pillar} data from FRED...[/cyan]")
        results = collector.fetch_by_pillar(pillar, start_date=start_date)
        success = sum(1 for v in results.values() if v is not None)
        console.print(f"[green]✓ Collected {success}/{len(results)} series[/green]")

    elif series:
        console.print(f"[cyan]Collecting {series} from FRED...[/cyan]")
        df = collector.fetch(series, start_date=start_date)
        console.print(f"[green]✓ Collected {len(df)} observations[/green]")

    else:
        console.print("[red]Specify --pillar or --series[/red]")


@cli.group()
def chart():
    """Charting commands"""
    pass


@chart.command()
@click.argument("series_id")
@click.option("--output", default="chart.png", help="Output filename")
@click.option("--title", help="Chart title")
@click.option("--transform", default=None, help="Transformation: yoy, mom, zscore, etc.")
def create(series_id, output, title, transform):
    """Create LHM standard chart for a series"""
    console.print(f"[cyan]Generating chart for {series_id}...[/cyan]")

    # Load data
    collector = FREDCollector()
    df = collector.load_latest(series_id)

    if df is None:
        console.print(f"[red]✗ No data found for {series_id}. Run collect first.[/red]")
        return

    # Apply smart defaults for common series
    series = df[series_id]

    # Auto-transform based on series type
    if transform:
        # User specified transformation
        from src import transformers
        if hasattr(transformers, transform):
            transform_func = getattr(transformers, transform)
            series = transform_func(series)
            label = f"{series_id} ({transform})"
        else:
            console.print(f"[yellow]Unknown transform '{transform}', using raw data[/yellow]")
            label = series_id
    elif series_id in ["GDP", "GDPC1", "GNP"]:
        # GDP should be YoY % by default (quarterly data)
        from src.transformers import yoy_pct
        series = yoy_pct(series, periods=4)
        label = f"{series_id} YoY%"
        console.print("[cyan]Auto-applying YoY% transformation (quarterly data)[/cyan]")
    elif series_id in ["CPIAUCSL", "PCEPI", "CPILFESL", "PCEPILFE"]:
        # Inflation should be YoY % by default (monthly data)
        from src.transformers import yoy_pct
        series = yoy_pct(series, periods=12)
        label = f"{series_id} YoY%"
        console.print("[cyan]Auto-applying YoY% transformation (monthly data)[/cyan]")
    else:
        # Use levels for other series
        label = series_id

    # Create chart
    set_lhm_style()
    lhm_chart = LHMChart()

    lhm_chart.plot_line(series, label=label, color="ocean_blue")

    if title:
        lhm_chart.set_title(title)
    else:
        # Try to get metadata
        metadata = collector.get_metadata(series_id)
        lhm_chart.set_title(metadata.get("title", series_id))

    lhm_chart.add_watermarks()
    lhm_chart.tight_layout()
    lhm_chart.save(output)

    console.print(f"[green]✓ Chart saved to {output}[/green]")


@cli.group()
def research():
    """Research workflow commands"""
    pass


@research.command()
def beacon():
    """Generate Beacon article (Sunday long-form)"""
    console.print("[cyan]Generating Beacon article...[/cyan]")
    console.print("[yellow]Note: Add data summary and context in interactive mode[/yellow]")

    workflow = BeaconWorkflow()
    # Interactive workflow would go here
    console.print("[green]✓ Beacon workflow initialized[/green]")


@research.command()
@click.argument("series_id")
def beam(series_id):
    """Generate Beam content (Tuesday/Thursday chart + paragraph)"""
    console.print(f"[cyan]Generating Beam for {series_id}...[/cyan]")

    # Load data and create chart
    collector = FREDCollector()
    df = collector.load_latest(series_id)

    if df is None:
        console.print(f"[red]✗ No data found for {series_id}[/red]")
        return

    metadata = collector.get_metadata(series_id)
    chart_desc = f"{metadata.get('title', series_id)} - Latest: {df.iloc[-1].values[0]:.2f}"

    # Generate content
    workflow = BeamWorkflow()
    content = workflow.generate(series_id, chart_desc)

    console.print("\n[bold]Generated Content:[/bold]")
    console.print(content)


@research.command()
def chartbook():
    """Generate Chartbook (Friday 50+ charts)"""
    console.print("[cyan]Generating Chartbook...[/cyan]")
    console.print("[yellow]Batch chart generation workflow[/yellow]")

    workflow = ChartbookWorkflow()
    console.print("[green]✓ Chartbook workflow initialized[/green]")


@research.command()
def horizon():
    """Generate Horizon outlook (First Monday)"""
    console.print("[cyan]Generating Horizon outlook...[/cyan]")

    workflow = HorizonWorkflow()
    console.print("[green]✓ Horizon workflow initialized[/green]")


@cli.command()
def config_info():
    """Show configuration details"""
    config = get_config()

    console.print("\n[bold]Configuration[/bold]")
    console.print(f"Root Directory: {config.root_dir}")
    console.print(f"Data Directory: {config.data_dir}")
    console.print(f"Config Directory: {config.config_dir}")

    console.print("\n[bold]Series Count by Pillar[/bold]")
    for pillar in ["macro_dynamics", "monetary_mechanics", "market_technicals"]:
        series = config.get_series_by_pillar(pillar)
        total = sum(len(v) for v in series.values() if isinstance(v, list))
        console.print(f"{pillar}: {total} series")


if __name__ == "__main__":
    cli()
