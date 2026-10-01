from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field


class ActorType(str, Enum):
    EMPLOYEE = "employee"
    INTERNAL_AGENT = "internal_agent"
    EXTERNAL_AGENT = "external_agent"
    SERVICE = "service"


class DataClassification(str, Enum):
    PUBLIC = "Public"
    INTERNAL = "Internal"
    CONFIDENTIAL = "Confidential"
    RESTRICTED = "Restricted"


class Decision(str, Enum):
    ALLOW = "ALLOW"
    ALLOW_WITH_MASKING = "ALLOW_WITH_MASKING"
    LIMIT = "LIMIT"
    HUMAN_APPROVAL = "HUMAN_APPROVAL"
    BLOCK = "BLOCK"


class SecurityRequest(BaseModel):
    event_id: str = Field(
        default_factory=lambda: f"evt_{uuid4().hex}"
    )
    actor_id: str = Field(min_length=1)
    actor_type: ActorType
    role: str = Field(min_length=1)

    agent_id: str | None = None
    session_id: str = Field(
        default_factory=lambda: f"session_{uuid4().hex}"
    )
    correlation_id: str = Field(
        default_factory=lambda: f"corr_{uuid4().hex}"
    )

    action: str = Field(min_length=1)
    tool_name: str | None = None

    data_classification: DataClassification
    record_count: int = Field(default=0, ge=0)
    destination: str = "internal_dashboard"

    trust_level: int = Field(default=50, ge=0, le=100)
    transaction_risk: int = Field(default=0, ge=0, le=100)

    approved: bool = False
    contains_untrusted_instruction: bool = False
    repeated_denials: int = Field(default=0, ge=0)

    is_synthetic: bool = True


class LayerResult(BaseModel):
    layer_number: int = Field(ge=1, le=8)
    layer_name: str
    risk_points: int = Field(ge=0, le=100)
    decision: Decision
    reason_codes: list[str] = Field(default_factory=list)
    details: str


class SecurityDecision(BaseModel):
    decision_id: str = Field(
        default_factory=lambda: f"decision_{uuid4().hex}"
    )
    event_id: str
    actor_id: str
    agent_id: str | None
    session_id: str
    correlation_id: str

    risk_score: int = Field(ge=0, le=100)
    final_decision: Decision
    reason_codes: list[str]
    layer_results: list[LayerResult]

    policy_version: str
    evaluated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    is_synthetic: bool = True