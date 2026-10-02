from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field


class DataClassification(str, Enum):
    PUBLIC = "Public"
    INTERNAL = "Internal"
    CONFIDENTIAL = "Confidential"
    RESTRICTED = "Restricted"


class DecisionType(str, Enum):
    ALLOW = "ALLOW"
    ALLOW_WITH_MASKING = "ALLOW_WITH_MASKING"
    LIMIT = "LIMIT"
    HUMAN_APPROVAL = "HUMAN_APPROVAL"
    BLOCK = "BLOCK"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SecurityRequest(BaseModel):
    request_id: str = Field(
        default_factory=lambda: f"req_{uuid4().hex}"
    )
    session_id: str = Field(
        default_factory=lambda: f"session_{uuid4().hex}"
    )

    actor_id: str = Field(min_length=1)
    actor_role: str = Field(min_length=1)
    agent_id: str = Field(min_length=1)

    action: str = Field(min_length=1)
    tool_name: str | None = None

    data_classification: DataClassification
    record_count: int = Field(default=0, ge=0)
    destination: str = Field(min_length=1)

    department: str = Field(min_length=1)
    resource_department: str = Field(min_length=1)

    trusted_context: bool = True
    contains_sensitive_data: bool = False
    fields: list[str] = Field(default_factory=list)

    repeated_denials: int = Field(default=0, ge=0)
    transaction_risk_score: int = Field(
        default=0,
        ge=0,
        le=100,
    )
    human_approved: bool = False

    request_text: str = ""
    is_synthetic: bool = True


class LayerResult(BaseModel):
    layer_number: int = Field(ge=1, le=8)
    layer_name: str
    decision: DecisionType
    risk_points: int = Field(ge=0, le=100)
    reason_codes: list[str] = Field(default_factory=list)
    details: str


class SecurityDecision(BaseModel):
    decision_id: str = Field(
        default_factory=lambda: f"decision_{uuid4().hex}"
    )
    event_id: str

    actor_id: str
    agent_id: str
    session_id: str

    decision: DecisionType
    risk_score: int = Field(ge=0, le=100)
    risk_level: RiskLevel

    reason_codes: list[str]
    layers: list[LayerResult]

    policy_version: str
    evaluated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    incident_created: bool = False
    incident_id: str | None = None
    is_synthetic: bool = True


class AgentPublicProfile(BaseModel):
    agent_id: str
    name: str
    agent_type: str
    owner_department: str
    trust_level: int
    permission_profile: str
    maximum_classification: DataClassification
    status: str
    allowed_tools: list[str]
    allowed_destinations: list[str]


class ScenarioResult(BaseModel):
    scenario_id: str
    description: str
    expected_decision: DecisionType
    actual_decision: DecisionType
    passed: bool
    decision: SecurityDecision


class RuntimeMetrics(BaseModel):
    total_decisions: int
    decision_counts: dict[str, int]
    total_incidents: int
    blocked_requests: int
    approval_requests: int
    masked_responses: int
    limited_responses: int