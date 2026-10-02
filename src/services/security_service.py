from __future__ import annotations

from collections import deque
from typing import Any

from src.domain.security_models import (
    SecurityDecision,
    SecurityRequest,
)
from src.security.security_engine import SecurityEngine
from src.storage.decision_repository import DecisionRepository


class SecurityService:
    def __init__(
        self,
        engine: SecurityEngine,
        repository: DecisionRepository,
        persist_decisions: bool,
    ) -> None:
        self.engine = engine
        self.repository = repository
        self.persist_decisions = persist_decisions

        self.runtime_decisions: deque[dict[str, Any]] = (
            deque(maxlen=1000)
        )
        self.runtime_incidents: deque[dict[str, Any]] = (
            deque(maxlen=1000)
        )

    def evaluate(
        self,
        request: SecurityRequest,
    ) -> SecurityDecision:
        decision = self.engine.evaluate(request)

        if self.persist_decisions:
            self.repository.save(decision)

        serialized = decision.model_dump(mode="json")
        self.runtime_decisions.appendleft(serialized)

        if decision.incident_created:
            self.runtime_incidents.appendleft(
                {
                    "incident_id": decision.incident_id,
                    "decision_id": decision.decision_id,
                    "event_id": decision.event_id,
                    "agent_id": decision.agent_id,
                    "severity": decision.risk_level.value,
                    "reason_codes": decision.reason_codes,
                    "containment_action": (
                        "BLOCK_ACTION_AND_"
                        "SUSPEND_DEMO_SESSION"
                    ),
                    "status": "open",
                    "created_at": (
                        decision.evaluated_at.isoformat()
                    ),
                }
            )

        return decision

    def list_decisions(
        self,
        limit: int,
    ) -> list[dict[str, Any]]:
        if self.persist_decisions:
            return self.repository.list_decisions(limit)

        return list(self.runtime_decisions)[:limit]

    def list_incidents(
        self,
        limit: int,
    ) -> list[dict[str, Any]]:
        if self.persist_decisions:
            return self.repository.list_incidents(limit)

        return list(self.runtime_incidents)[:limit]