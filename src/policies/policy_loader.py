from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


REQUIRED_SECTIONS = {
    "policy_version",
    "risk_thresholds",
    "classification_rank",
    "record_limits",
    "high_risk_tools",
    "always_forbidden_tools",
    "restricted_fields",
    "prompt_attack_markers",
    "agents",
}


def load_security_policy(
    path: str | Path,
) -> dict[str, Any]:
    policy_path = Path(path)

    if not policy_path.exists():
        raise FileNotFoundError(
            f"Security policy was not found: {policy_path}"
        )

    with policy_path.open("r", encoding="utf-8") as file:
        policy = yaml.safe_load(file)

    if not isinstance(policy, dict):
        raise ValueError(
            "Security policy must contain a YAML object."
        )

    missing_sections = REQUIRED_SECTIONS.difference(policy)

    if missing_sections:
        missing_text = ", ".join(sorted(missing_sections))
        raise ValueError(
            f"Security policy is missing sections: {missing_text}"
        )

    if not policy["agents"]:
        raise ValueError(
            "Security policy must contain at least one agent."
        )

    return policy