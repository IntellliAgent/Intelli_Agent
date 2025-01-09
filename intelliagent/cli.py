"""Command line interface for IntelliAgent."""

import argparse
import sys
from typing import List, Optional
import json

from .core import DecisionMaker
from .utils import Logger


def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI."""
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        description="IntelliAgent CLI"
    )
    parser.add_argument(
        "--api-key",
        required=True,
        help="OpenAI API key"
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Input text for decision making"
    )
    parser.add_argument(
        "--context",
        type=str,
        default="{}",
        help="JSON context for decision making"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output file for results (optional)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    parsed_args = parser.parse_args(args)

    # Setup logging
    log_level = "DEBUG" if parsed_args.verbose else "INFO"
    logger = Logger("intelliagent", level=log_level)

    try:
        # Parse context
        context = json.loads(parsed_args.context)

        # Initialize agent
        agent = DecisionMaker(api_key=parsed_args.api_key)

        # Make decision
        result = agent.make_decision(
            user_id="cli_user",
            input_data=parsed_args.input,
            context=context
        )

        # Handle output
        if parsed_args.output:
            with open(parsed_args.output, 'w') as f:
                json.dump(result, f, indent=2)
        else:
            print(json.dumps(result, indent=2))

        return 0

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
