
import click
from loguru import logger
from data import extract_commits_data


@click.command()
@click.option('--email', help='Git user email to search for')
@click.option('--base_path', help='Base path from which recursive search for git repos starts')
@click.option('--start_date', help='Start date')
@click.option('--end_date', help='End date')
@click.option('--export_path', default="./data/ipbox.csv", help='Export path to which CSV is saved')
def parse(email:str, base_path: str, start_date: str, end_date: str, export_path: str) -> None:
    """Prepare basic info about work done in given timeframe"""
    logger.info(f"Parsing started with: {email=}, {base_path=}, {start_date=}, {end_date=}, {export_path=}")
    data = main(email, base_path, start_date, end_date, export_path)
    if not data.empty:
        logger.info(f"Saving data to {export_path}")
        data.to_csv(export_path, index=False)
    else:
        logger.info("No commit data found")


def main(email:str, base_path: str, start_date: str, end_date: str, export_path: str):
    return extract_commits_data(email, start_date, end_date, base_path)
 


if __name__ == '__main__':
    parse()

