from django.core.management.base import BaseCommand
import sys

class Command(BaseCommand):
    help = "Run kcli commands from the Django CLI."

    def run_from_argv(self, argv):
        # Remove the management command name ("kcli") from argv
        kcli_args = argv[2:]
        try:
            from kcli.__main__ import app
            # Call the Typer app with the forwarded arguments
            app(prog_name="karrio cli", args=kcli_args)
        except SystemExit as e:
            # Typer uses SystemExit for normal CLI exit, so suppress traceback
            sys.exit(e.code)
        except ImportError:
            self.stderr.write(self.style.ERROR("Could not import kcli CLI app."))
            sys.exit(1)
