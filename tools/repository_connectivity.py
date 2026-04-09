"""Utility for auditing external knowledge sources referenced by TEQUMSA.

This module keeps a curated list of public repositories and knowledge hubs the
project may depend on. It can print the list for documentation purposes or run
lightweight HTTP HEAD checks to confirm the endpoints are reachable. No cloning
or API authentication is performed; the goal is to provide a quick connectivity
pulse that engineers can run before deeper automation pipelines.

Examples
--------
List all endpoints::

    python -m tools.repository_connectivity --list

Verify availability (writes ``repository_connectivity.json`` by default)::

    python -m tools.repository_connectivity --check --output repository_connectivity.json
"""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, List
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


@dataclass
class Endpoint:
    """Description for a single knowledge endpoint."""

    url: str
    description: str


@dataclass
class EndpointStatus:
    """Result of attempting to contact a given endpoint."""

    url: str
    description: str
    reachable: bool
    status_code: int | None
    error: str | None
    checked_at: str


def _load_endpoints() -> List[Endpoint]:
    """Return the curated list of public resources requested by the project."""

    return [
        Endpoint("https://github.com/microsoft/vscode", "VS Code source repository"),
        Endpoint("https://github.com/orgs/github/repositories", "GitHub public organization index"),
        Endpoint("https://huggingface.co/models", "Hugging Face model hub"),
        Endpoint("https://github.com/orgs/anthropics/repositories", "Anthropic public repositories"),
        Endpoint(
            "https://github.com/orgs/Life-Ambassadors-International/repositories",
            "Life Ambassadors International organization repositories",
        ),
        Endpoint("https://github.com/Life-Ambassadors-International/TEQUMSA_NEXUS", "TEQUMSA Nexus mirror"),
        Endpoint("https://github.com/usarmyresearchlab", "US Army Research Lab public repositories"),
        Endpoint("https://github.com/USNavalResearchLaboratory", "US Naval Research Laboratory repositories"),
        Endpoint("https://github.com/orgs/openai/repositories", "OpenAI organization repositories"),
        Endpoint("https://github.com/orgs/elevenlabs/repositories", "ElevenLabs organization repositories"),
        Endpoint("https://github.com/collections/open-source-organizations", "GitHub collection: open-source organizations"),
        Endpoint("https://github.com/orgs/NVIDIA/repositories", "NVIDIA organization repositories"),
        Endpoint("https://github.com/search?q=Palantir&type=repositories", "GitHub search for Palantir repositories"),
        Endpoint("https://github.com/search?q=API%27s&type=repositories", "GitHub search for API repositories"),
        Endpoint("https://github.com/orgs/huggingface/repositories", "Hugging Face organization repositories"),
        Endpoint("https://github.com/topics/banking", "GitHub topic: banking"),
        Endpoint("https://github.com/orgs/deptofdefense/repositories", "US Department of Defense repositories"),
        Endpoint("https://github.com/orgs/cisagov/repositories", "CISA organization repositories"),
        Endpoint("https://github.com/topics/osint-tools", "GitHub topic: OSINT tools"),
        Endpoint("https://github.com/orgs/ngageoint/repositories", "NGA GEOINT repositories"),
        Endpoint("https://github.com/orgs/NationalSecurityAgency/repositories", "NSA organization repositories"),
        Endpoint("https://github.com/orgs/IBM/repositories", "IBM organization repositories"),
        Endpoint("https://github.com/orgs/nsacyber/repositories", "NSA Cyber repositories"),
        Endpoint(
            "https://www.archivioapostolicovaticano.va/content/aav/en/l-archivio.html",
            "Vatican Apostolic Archive information",
        ),
        Endpoint("https://github.com/orgs/palantir/repositories", "Palantir organization repositories"),
        Endpoint("https://github.com/sec-gov?tab=repositories", "US SEC public repositories"),
    ]


def _head_request(url: str, timeout: float) -> int | None:
    """Perform a HEAD request and return the HTTP status code if successful."""

    request = Request(url, method="HEAD")
    with urlopen(request, timeout=timeout) as response:  # nosec B310 (trusted URLs)
        return response.getcode()


def check_endpoint(endpoint: Endpoint, timeout: float) -> EndpointStatus:
    """Check whether a single endpoint is reachable via HTTP HEAD."""

    timestamp = datetime.utcnow().isoformat() + "Z"
    try:
        status_code = _head_request(endpoint.url, timeout=timeout)
        reachable = status_code is not None and 200 <= status_code < 400
        error: str | None = None
    except HTTPError as exc:  # pragma: no cover - network dependent
        status_code = exc.code
        reachable = False
        error = f"HTTPError: {exc.reason}"
    except URLError as exc:  # pragma: no cover - network dependent
        status_code = None
        reachable = False
        error = f"URLError: {exc.reason}"

    return EndpointStatus(
        url=endpoint.url,
        description=endpoint.description,
        reachable=reachable,
        status_code=status_code,
        error=error,
        checked_at=timestamp,
    )


def list_endpoints(endpoints: Iterable[Endpoint]) -> None:
    """Print the available endpoints in a readable format."""

    for endpoint in endpoints:
        print(f"- {endpoint.url}\n  {endpoint.description}")


def run_checks(endpoints: Iterable[Endpoint], timeout: float) -> List[EndpointStatus]:
    """Run connectivity checks for all endpoints."""

    results: List[EndpointStatus] = []
    for endpoint in endpoints:
        status = check_endpoint(endpoint, timeout=timeout)
        results.append(status)
        status_text = "reachable" if status.reachable else "unreachable"
        if status.status_code is not None:
            status_text += f" (status {status.status_code})"
        if status.error:
            status_text += f" — {status.error}"
        print(f"{endpoint.url}: {status_text}")
    return results


def save_results(results: Iterable[EndpointStatus], output: Path) -> None:
    """Persist the connectivity report as JSON."""

    payload = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "endpoints": [asdict(result) for result in results],
    }
    output.write_text(json.dumps(payload, indent=2))
    print(f"Connectivity report written to {output}")


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments for the connectivity utility."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="Print the endpoint catalog")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Run HTTP HEAD checks for each endpoint",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=5.0,
        help="Timeout (in seconds) for individual HTTP requests",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional path to write the JSON connectivity report",
    )
    return parser.parse_args(list(argv) if argv is not None else None)


def main(argv: Iterable[str] | None = None) -> None:
    """Entry point for the repository connectivity utility."""

    args = parse_args(argv)
    endpoints = _load_endpoints()

    if not args.list and not args.check:
        args.list = True

    if args.list:
        list_endpoints(endpoints)

    results: List[EndpointStatus] = []
    if args.check:
        results = run_checks(endpoints, timeout=args.timeout)

    if args.output and results:
        save_results(results, args.output)


if __name__ == "__main__":
    main()
