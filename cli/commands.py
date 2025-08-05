"""CLI commands for Math Operations service."""
import asyncio
import json
from typing import Optional

import click
import httpx
from tabulate import tabulate

from app.core.config import settings


BASE_URL = f"http://localhost:{settings.PORT}{settings.API_V1_STR}"


@click.group()
def cli():
    """Math Operations CLI - Command line interface for the microservice."""
    pass


@cli.command()
@click.option('--base', '-b', type=int, required=True, help='Base number')
@click.option('--exponent', '-e', type=int, required=True, help='Exponent')
def power(base: int, exponent: int):
    """Calculate base raised to the power of exponent."""
    asyncio.run(_calculate('power', base, exponent))


@cli.command()
@click.option('--number', '-n', type=int, required=True, help='Position in Fibonacci sequence')
def fibonacci(number: int):
    """Calculate the n-th Fibonacci number."""
    asyncio.run(_calculate('fibonacci', number))


@cli.command()
@click.option('--number', '-n', type=int, required=True, help='Number to calculate factorial')
def factorial(number: int):
    """Calculate the factorial of a number."""
    asyncio.run(_calculate('factorial', number))


@cli.command()
@click.option('--limit', '-l', type=int, default=10, help='Number of records to show')
@click.option('--operation', '-o', type=click.Choice(['power', 'fibonacci', 'factorial']), 
              help='Filter by operation type')
def history(limit: int, operation: Optional[str]):
    """View operation history."""
    asyncio.run(_get_history(limit, operation))


@cli.command()
def cache_stats():
    """View cache statistics."""
    asyncio.run(_get_cache_stats())


@cli.command()
@click.confirmation_option(prompt='Are you sure you want to clear the cache?')
def clear_cache():
    """Clear the cache."""
    asyncio.run(_clear_cache())


async def _calculate(operation: str, value: int, exponent: Optional[int] = None):
    """Perform calculation via API."""
    async with httpx.AsyncClient() as client:
        try:
            data = {
                "operation": operation,
                "value": value
            }
            if exponent is not None:
                data["exponent"] = exponent
            
            response = await client.post(f"{BASE_URL}/calculate", json=data)
            
            if response.status_code == 200:
                result = response.json()
                click.echo(f"\n✓ Calculation completed successfully!")
                click.echo(f"Operation: {result['operation']}")
                click.echo(f"Input: {result['input_value']}")
                if result.get('exponent'):
                    click.echo(f"Exponent: {result['exponent']}")
                click.echo(f"Result: {result['result']}")
                click.echo(f"Cached: {'Yes' if result['cached'] else 'No'}")
                click.echo(f"Computation time: {result['computation_time_ms']:.3f} ms")
            else:
                error = response.json()
                click.echo(f"\n✗ Error: {error.get('detail', 'Unknown error')}", err=True)
                
        except httpx.ConnectError:
            click.echo("\n✗ Error: Cannot connect to the API. Is the service running?", err=True)
        except Exception as e:
            click.echo(f"\n✗ Error: {str(e)}", err=True)


async def _get_history(limit: int, operation: Optional[str]):
    """Get operation history."""
    async with httpx.AsyncClient() as client:
        try:
            params = {"limit": limit}
            if operation:
                params["operation"] = operation
            
            response = await client.get(f"{BASE_URL}/history", params=params)
            
            if response.status_code == 200:
                history = response.json()
                
                if not history:
                    click.echo("\nNo operations found in history.")
                    return
                
                # Prepare table data
                table_data = []
                for item in history:
                    table_data.append([
                        item['id'],
                        item['operation'],
                        item['input_value'],
                        item.get('exponent', '-'),
                        str(item['result'])[:20] + '...' if len(str(item['result'])) > 20 else item['result'],
                        f"{item['computation_time_ms']:.3f} ms",
                        item['created_at'][:19]  # Remove microseconds
                    ])
                
                headers = ['ID', 'Operation', 'Input', 'Exponent', 'Result', 'Time', 'Created At']
                click.echo(f"\n{tabulate(table_data, headers=headers, tablefmt='grid')}")
                
        except httpx.ConnectError:
            click.echo("\n✗ Error: Cannot connect to the API. Is the service running?", err=True)
        except Exception as e:
            click.echo(f"\n✗ Error: {str(e)}", err=True)


async def _get_cache_stats():
    """Get cache statistics."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/cache/stats")
            
            if response.status_code == 200:
                stats = response.json()
                click.echo("\nCache Statistics:")
                click.echo(f"  Current size: {stats['size']}")
                click.echo(f"  Maximum size: {stats['max_size']}")
                click.echo(f"  TTL: {stats['ttl_seconds']} seconds")
                
        except httpx.ConnectError:
            click.echo("\n✗ Error: Cannot connect to the API. Is the service running?", err=True)
        except Exception as e:
            click.echo(f"\n✗ Error: {str(e)}", err=True)


async def _clear_cache():
    """Clear the cache."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.delete(f"{BASE_URL}/cache")
            
            if response.status_code == 200:
                click.echo("\n✓ Cache cleared successfully!")
            else:
                click.echo("\n✗ Error clearing cache", err=True)
                
        except httpx.ConnectError:
            click.echo("\n✗ Error: Cannot connect to the API. Is the service running?", err=True)
        except Exception as e:
            click.echo(f"\n✗ Error: {str(e)}", err=True)


if __name__ == "__main__":
    cli()