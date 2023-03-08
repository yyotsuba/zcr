import traceback

from .cli import CLI
from .main import Main

def run():
    cli = CLI()
    (options, args) = cli.parse()
    print(options, args)

    main = Main(cli, options, args)
    if options.upgradedb:
        main.upgradedb()
    elif options.print_version:
        main.print_version()
    else:
        main.start()

