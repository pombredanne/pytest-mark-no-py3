from bowler import Query
import click

from ._bowler import filter_already_marked
from ._bowler import filter_failing_tests
from ._bowler import MARKER
from ._bowler import remove_marker


@click.command(help="Remove %s from failing tests" % MARKER)
@click.option(
    "--result-log",
    type=click.File("r"),
    help="Path to pytest --result-log file",
    required=False,
)
@click.option("--interactive/--no-interactive", is_flag=True, default=True)
@click.argument("paths", type=click.Path(exists=True, dir_okay=True), nargs=-1)
def main(result_log, interactive, paths):
    query = Query(paths).select("funcdef").filter(filter_already_marked)
    if result_log:
        query = query.filter(filter_failing_tests(result_log))

    query.modify(remove_marker).write(interactive=interactive)


if __name__ == "__main__":
    main()
