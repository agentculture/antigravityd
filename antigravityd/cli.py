import argparse
import sys

from antigravityd import __version__


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        description="Antigravity daemon for delegated repository tasks and reviewable PRs."
    )
    parser.add_argument("--version", action="version", version=f"antigravityd {__version__}")

    subparsers = parser.add_subparsers(dest="command", help="sub-command help")

    serve_parser = subparsers.add_parser("serve", help="Start the daemon server")
    serve_parser.add_argument(
        "--port", type=int, default=8080, help="Port to run the daemon server on"
    )

    parsed = parser.parse_args(args)

    if parsed.command == "serve":
        print(f"Starting antigravityd daemon on port {parsed.port}...")
        return 0
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
