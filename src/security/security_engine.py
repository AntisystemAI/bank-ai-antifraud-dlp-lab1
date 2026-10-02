from __future__ import annotations

from typing import Any
from uuid import uuid4

from src.domain.security_models import (
    DataClassification,
    DecisionType,
    LayerResult,
    RiskLevel,
    SecurityDecision,
    SecurityRequest,
)


DECISION_PRIORITY = {
    DecisionType.ALLOW: 0,
    DecisionType.ALLOW_WITH_MASKING: 1,
    DecisionType.LIMIT: 2,
    DecisionType.HUMAN_APPROVAL: 3,
    DecisionType.BLOCK: 4,
}


class SecurityEngine:
    def __init__(self, policy: dict[str, Any]) -> None:
        self.policy = policy

    def evaluate(
        self,
        request: SecurityRequest,
    ) -> SecurityDecision:
        if not request.is_synthetic:
            raise ValueError(
                "Only synthetic demonstration events are allowed."
            )

        agent = self.policy["agents"].get(request.agent_id)

        layers = [
            self._layer_1_identity(request, agent),
            self._layer_2_input_control(request),
            self._layer_3_tool_access(request, agent),
            self._layer_4_data_access(request, agent),
            self._layer_5_risk(request),
            self._layer_6_dlp(request),
            self._layer_7_egress(request, agent),
            self._layer_8_monitoring(request),
        ]

        final_decision = max(
            (layer.decision for layer in layers),
            key=lambda decision: DECISION_PRIORITY[decision],
        )

        risk_score = min(
            100,
            sum(layer.risk_points for layer in layers),
        )

        risk_score = self._apply_decision_floor(
            risk_score,
            final_decision,
        )

        score_decision = self._decision_from_score(risk_score)

        if (
            DECISION_PRIORITY[score_decision]
            > DECISION_PRIORITY[final_decision]
        ):
            final_decision = score_decision

        reason_codes = sorted(
            {
                reason
                for layer in layers
                for reason in layer.reason_codes
            }
        )

        if not reason_codes:
            reason_codes = ["NO_POLICY_VIOLATION"]

        incident_created = (
            final_decision == DecisionType.BLOCK
        )

        incident_id = (
            f"incident_{uuid4().hex}"
            if incident_created
            else None
        )

        return SecurityDecision(
            event_id=request.request_id,
            actor_id=request.actor_id,
            agent_id=request.agent_id,
            session_id=request.session_id,
            decision=final_decision,
            risk_score=risk_score,
            risk_level=self._risk_level(risk_score),
            reason_codes=reason_codes,
            layers=layers,
            policy_version=self.policy["policy_version"],
            incident_created=incident_created,
            incident_id=incident_id,
            is_synthetic=True,
        )

    def _layer_1_identity(
        self,
        request: SecurityRequest,
        agent: dict[str, Any] | None,
    ) -> LayerResult:
        if agent is None:
            return self._result(
                number=1,
                name="Identity and trust",
                decision=DecisionType.BLOCK,
                risk_points=70,
                reason_codes=["UNKNOWN_AGENT"],
                details=(
                    "Агент отсутствует в утверждённом реестре."
                ),
            )

        if agent["status"] != "active":
            return self._result(
                number=1,
                name="Identity and trust",
                decision=DecisionType.BLOCK,
                risk_points=70,
                reason_codes=["AGENT_NOT_ACTIVE"],
                details="Учётная запись агента неактивна.",
            )

        if request.actor_role not in agent["allowed_roles"]:
            return self._result(
                number=1,
                name="Identity and trust",
                decision=DecisionType.BLOCK,
                risk_points=50,
                reason_codes=[
                    "ROLE_NOT_ALLOWED_FOR_AGENT"
                ],
                details=(
                    "Роль пользователя не разрешена "
                    "профилем агента."
                ),
            )

        return self._result(
            number=1,
            name="Identity and trust",
            decision=DecisionType.ALLOW,
            risk_points=0,
            reason_codes=[],
            details=(
                "Идентичность, роль и состояние агента "
                "проверены."
            ),
        )

    def _layer_2_input_control(
        self,
        request: SecurityRequest,
    ) -> LayerResult:
        normalized_text = request.request_text.lower()

        attack_detected = any(
            marker.lower() in normalized_text
            for marker in self.policy[
                "prompt_attack_markers"
            ]
        )

        if attack_detected:
            return self._result(
                number=2,
                name="Input and context control",
                decision=DecisionType.BLOCK,
                risk_points=50,
                reason_codes=[
                    "POLICY_BYPASS_INSTRUCTION_DETECTED"
                ],
                details=(
                    "Обнаружена инструкция на обход "
                    "защитной политики."
                ),
            )

        if not request.trusted_context:
            return self._result(
                number=2,
                name="Input and context control",
                decision=DecisionType.HUMAN_APPROVAL,
                risk_points=25,
                reason_codes=[
                    "UNTRUSTED_CONTEXT_DETECTED"
                ],
                details=(
                    "Недоверенный контекст изолирован "
                    "и требует проверки."
                ),
            )

        return self._result(
            number=2,
            name="Input and context control",
            decision=DecisionType.ALLOW,
            risk_points=0,
            reason_codes=[],
            details=(
                "Входной контекст соответствует политике."
            ),
        )

    def _layer_3_tool_access(
        self,
        request: SecurityRequest,
        agent: dict[str, Any] | None,
    ) -> LayerResult:
        if request.tool_name is None:
            return self._result(
                number=3,
                name="Tool access control",
                decision=DecisionType.ALLOW,
                risk_points=0,
                reason_codes=[],
                details="Вызов инструмента не запрашивался.",
            )

        if (
            request.tool_name
            in self.policy["always_forbidden_tools"]
        ):
            return self._result(
                number=3,
                name="Tool access control",
                decision=DecisionType.BLOCK,
                risk_points=60,
                reason_codes=[
                    "FORBIDDEN_TOOL_REQUESTED"
                ],
                details=(
                    "Запрошен безусловно запрещённый "
                    "инструмент."
                ),
            )

        if (
            agent is None
            or request.tool_name
            not in agent["allowed_tools"]
        ):
            return self._result(
                number=3,
                name="Tool access control",
                decision=DecisionType.BLOCK,
                risk_points=45,
                reason_codes=["TOOL_NOT_ALLOWED"],
                details=(
                    "Инструмент отсутствует в allowlist "
                    "агента."
                ),
            )

        if (
            request.tool_name
            in self.policy["high_risk_tools"]
            and not request.human_approved
        ):
            return self._result(
                number=3,
                name="Tool access control",
                decision=DecisionType.HUMAN_APPROVAL,
                risk_points=30,
                reason_codes=[
                    "HIGH_RISK_TOOL_REQUIRES_APPROVAL"
                ],
                details=(
                    "Инструмент высокого риска требует "
                    "согласования."
                ),
            )

        return self._result(
            number=3,
            name="Tool access control",
            decision=DecisionType.ALLOW,
            risk_points=0,
            reason_codes=[],
            details=(
                "Инструмент разрешён профилем агента."
            ),
        )

    def _layer_4_data_access(
        self,
        request: SecurityRequest,
        agent: dict[str, Any] | None,
    ) -> LayerResult:
        if agent is None:
            return self._result(
                number=4,
                name="Data access control",
                decision=DecisionType.BLOCK,
                risk_points=50,
                reason_codes=[
                    "DATA_ACCESS_WITH_UNKNOWN_AGENT"
                ],
                details=(
                    "Неизвестный агент не может "
                    "обращаться к данным."
                ),
            )

        classification_rank = self.policy[
            "classification_rank"
        ]

        requested_rank = classification_rank[
            request.data_classification.value
        ]

        maximum_rank = classification_rank[
            agent["maximum_classification"]
        ]

        if requested_rank > maximum_rank:
            return self._result(
                number=4,
                name="Data access control",
                decision=DecisionType.BLOCK,
                risk_points=55,
                reason_codes=[
                    "CLASSIFICATION_SCOPE_EXCEEDED"
                ],
                details=(
                    "Уровень данных превышает "
                    "полномочия агента."
                ),
            )

        if (
            requested_rank >= 2
            and request.department
            != request.resource_department
            and request.agent_id != "agent_security"
        ):
            return self._result(
                number=4,
                name="Data access control",
                decision=DecisionType.BLOCK,
                risk_points=50,
                reason_codes=[
                    "CROSS_DEPARTMENT_ACCESS_DENIED"
                ],
                details=(
                    "ABAC запретил доступ к данным "
                    "другого подразделения."
                ),
            )

        record_limit = self.policy["record_limits"][
            request.data_classification.value
        ]

        if request.record_count > record_limit:
            return self._result(
                number=4,
                name="Data access control",
                decision=DecisionType.LIMIT,
                risk_points=25,
                reason_codes=[
                    "DATA_VOLUME_LIMIT_EXCEEDED"
                ],
                details=(
                    "Запрошенный объём превышает лимит "
                    f"{record_limit} записей."
                ),
            )

        return self._result(
            number=4,
            name="Data access control",
            decision=DecisionType.ALLOW,
            risk_points=0,
            reason_codes=[],
            details=(
                "Классификация, подразделение и объём "
                "проверены."
            ),
        )

    def _layer_5_risk(
        self,
        request: SecurityRequest,
    ) -> LayerResult:
        if request.repeated_denials >= 2:
            return self._result(
                number=5,
                name="Behavioral and transaction risk",
                decision=DecisionType.BLOCK,
                risk_points=45,
                reason_codes=[
                    "REPEATED_POLICY_VIOLATION"
                ],
                details=(
                    "Обнаружено повторение ранее "
                    "запрещённого действия."
                ),
            )

        if request.transaction_risk_score >= 70:
            return self._result(
                number=5,
                name="Behavioral and transaction risk",
                decision=DecisionType.BLOCK,
                risk_points=45,
                reason_codes=[
                    "CRITICAL_TRANSACTION_RISK"
                ],
                details=(
                    "Транзакционный риск достиг "
                    "критического уровня."
                ),
            )

        if request.transaction_risk_score >= 50:
            return self._result(
                number=5,
                name="Behavioral and transaction risk",
                decision=DecisionType.HUMAN_APPROVAL,
                risk_points=30,
                reason_codes=[
                    "HIGH_TRANSACTION_RISK"
                ],
                details=(
                    "Операция требует проверки аналитиком."
                ),
            )

        if (
            request.transaction_risk_score >= 30
            or request.repeated_denials == 1
        ):
            return self._result(
                number=5,
                name="Behavioral and transaction risk",
                decision=DecisionType.LIMIT,
                risk_points=20,
                reason_codes=[
                    "ELEVATED_BEHAVIORAL_RISK"
                ],
                details=(
                    "Обнаружено отклонение от обычного "
                    "поведения."
                ),
            )

        return self._result(
            number=5,
            name="Behavioral and transaction risk",
            decision=DecisionType.ALLOW,
            risk_points=0,
            reason_codes=[],
            details=(
                "Критических поведенческих отклонений нет."
            ),
        )

    def _layer_6_dlp(
        self,
        request: SecurityRequest,
    ) -> LayerResult:
        restricted_fields = set(
            self.policy["restricted_fields"]
        )

        requested_fields = set(request.fields)

        if restricted_fields.intersection(requested_fields):
            return self._result(
                number=6,
                name="DLP and masking",
                decision=DecisionType.HUMAN_APPROVAL,
                risk_points=25,
                reason_codes=[
                    "RESTRICTED_FIELD_DETECTED"
                ],
                details=(
                    "Обнаружены поля, требующие "
                    "отдельного согласования."
                ),
            )

        if (
            request.data_classification
            == DataClassification.RESTRICTED
        ):
            return self._result(
                number=6,
                name="DLP and masking",
                decision=DecisionType.HUMAN_APPROVAL,
                risk_points=25,
                reason_codes=[
                    "RESTRICTED_DATA_DETECTED"
                ],
                details=(
                    "Restricted-данные нельзя выдавать "
                    "без согласования."
                ),
            )

        if (
            request.contains_sensitive_data
            or request.data_classification
            == DataClassification.CONFIDENTIAL
        ):
            return self._result(
                number=6,
                name="DLP and masking",
                decision=DecisionType.ALLOW_WITH_MASKING,
                risk_points=10,
                reason_codes=[
                    "SENSITIVE_DATA_MASKING_REQUIRED"
                ],
                details=(
                    "Идентификаторы должны быть "
                    "замаскированы."
                ),
            )

        return self._result(
            number=6,
            name="DLP and masking",
            decision=DecisionType.ALLOW,
            risk_points=0,
            reason_codes=[],
            details=(
                "Чувствительные поля не обнаружены."
            ),
        )

    def _layer_7_egress(
        self,
        request: SecurityRequest,
        agent: dict[str, Any] | None,
    ) -> LayerResult:
        if agent is None:
            return self._result(
                number=7,
                name="Egress control",
                decision=DecisionType.BLOCK,
                risk_points=50,
                reason_codes=[
                    "EGRESS_WITH_UNKNOWN_AGENT"
                ],
                details=(
                    "Неизвестному агенту запрещена "
                    "передача данных."
                ),
            )

        if (
            request.destination
            in agent["allowed_destinations"]
        ):
            return self._result(
                number=7,
                name="Egress control",
                decision=DecisionType.ALLOW,
                risk_points=0,
                reason_codes=[],
                details=(
                    "Используется разрешённое направление "
                    "передачи."
                ),
            )

        classification_rank = self.policy[
            "classification_rank"
        ][request.data_classification.value]

        if (
            classification_rank >= 2
            or request.contains_sensitive_data
        ):
            return self._result(
                number=7,
                name="Egress control",
                decision=DecisionType.BLOCK,
                risk_points=50,
                reason_codes=[
                    "SENSITIVE_DATA_EXTERNAL_DESTINATION"
                ],
                details=(
                    "Передача чувствительных данных "
                    "в этот канал запрещена."
                ),
            )

        return self._result(
            number=7,
            name="Egress control",
            decision=DecisionType.LIMIT,
            risk_points=15,
            reason_codes=[
                "DESTINATION_NOT_ALLOWED"
            ],
            details=(
                "Направление отсутствует в allowlist "
                "агента."
            ),
        )

    def _layer_8_monitoring(
        self,
        request: SecurityRequest,
    ) -> LayerResult:
        if request.repeated_denials >= 2:
            return self._result(
                number=8,
                name="Monitoring and response",
                decision=DecisionType.BLOCK,
                risk_points=10,
                reason_codes=[
                    "SESSION_CONTAINMENT_REQUIRED"
                ],
                details=(
                    "Сессия должна быть остановлена "
                    "и расследована."
                ),
            )

        return self._result(
            number=8,
            name="Monitoring and response",
            decision=DecisionType.ALLOW,
            risk_points=0,
            reason_codes=[],
            details=(
                "Событие будет записано в безопасный аудит."
            ),
        )

    @staticmethod
    def _apply_decision_floor(
        score: int,
        decision: DecisionType,
    ) -> int:
        minimum_scores = {
            DecisionType.ALLOW: 0,
            DecisionType.ALLOW_WITH_MASKING: 10,
            DecisionType.LIMIT: 30,
            DecisionType.HUMAN_APPROVAL: 50,
            DecisionType.BLOCK: 70,
        }

        return max(score, minimum_scores[decision])

    @staticmethod
    def _decision_from_score(
        score: int,
    ) -> DecisionType:
        if score >= 70:
            return DecisionType.BLOCK

        if score >= 50:
            return DecisionType.HUMAN_APPROVAL

        if score >= 30:
            return DecisionType.LIMIT

        return DecisionType.ALLOW

    @staticmethod
    def _risk_level(score: int) -> RiskLevel:
        if score >= 70:
            return RiskLevel.CRITICAL

        if score >= 50:
            return RiskLevel.HIGH

        if score >= 30:
            return RiskLevel.MEDIUM

        return RiskLevel.LOW

    @staticmethod
    def _result(
        number: int,
        name: str,
        decision: DecisionType,
        risk_points: int,
        reason_codes: list[str],
        details: str,
    ) -> LayerResult:
        return LayerResult(
            layer_number=number,
            layer_name=name,
            decision=decision,
            risk_points=risk_points,
            reason_codes=reason_codes,
            details=details,
        )