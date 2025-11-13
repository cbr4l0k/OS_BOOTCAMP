"""Development server script for running Chainlit with watch mode."""
import subprocess
import sys


def dev():
    """Run Chainlit in development mode with watch flag."""
    try:
        subprocess.run(
            ["chainlit", "run", "src/app/main.py", "-w"],
            check=True
        )
    except KeyboardInterrupt:
        sys.exit(0)
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)


if __name__ == "__main__":
    dev()
