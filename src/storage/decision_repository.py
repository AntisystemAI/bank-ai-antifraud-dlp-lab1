from __future__ import annotations

from typing import Any

import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

from src.domain.security_models import SecurityDecision


class DecisionRepository:
    def __init__(self, database_url: str) -> None:
        self.database_url = database_url

    def healthcheck(self) -> bool:
        with psycopg.connect(
            self.database_url,
            connect_timeout=5,
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1;")
                result = cursor.fetchone()

                return result is not None and result[0] == 1

    def save(
        self,
        decision: SecurityDecision,
    ) -> None:
        layer_results = [
            layer.model_dump(mode="json")
            for layer in decision.layers
        ]

        with psycopg.connect(
            self.database_url,
            connect_timeout=5,
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO public.security_decisions (
                        decision_id,
                        event_id,
                        actor_id,
                        agent_id,
                        session_id,
                        correlation_id,
                        risk_score,
                        final_decision,
                        reason_codes,
                        layer_results,
                        policy_version,
                        evaluated_at,
                        is_synthetic
                    )
                    VALUES (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    )
                    ON CONFLICT (event_id)
                    DO UPDATE SET
                        actor_id = EXCLUDED.actor_id,
                        agent_id = EXCLUDED.agent_id,
                        session_id = EXCLUDED.session_id,
                        correlation_id = EXCLUDED.correlation_id,
                        risk_score = EXCLUDED.risk_score,
                        final_decision = EXCLUDED.final_decision,
                        reason_codes = EXCLUDED.reason_codes,
                        layer_results = EXCLUDED.layer_results,
                        policy_version = EXCLUDED.policy_version,
                        evaluated_at = EXCLUDED.evaluated_at,
                        is_synthetic = EXCLUDED.is_synthetic
                    """,
                    (
                        decision.decision_id,
                        decision.event_id,
                        decision.actor_id,
                        decision.agent_id,
                        decision.session_id,
                        decision.session_id,
                        decision.risk_score,
                        decision.decision.value,
                        Jsonb(decision.reason_codes),
                        Jsonb(layer_results),
                        decision.policy_version,
                        decision.evaluated_at,
                        decision.is_synthetic,
                    ),
                )

                if (
                    decision.incident_created
                    and decision.incident_id
                ):
                    cursor.execute(
                        """
                        INSERT INTO public.security_incidents (
                            incident_id,
                            decision_id,
                            event_id,
                            agent_id,
                            severity,
                            reason_codes,
                            containment_action,
                            status
                        )
                        VALUES (
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s
                        )
                        ON CONFLICT (incident_id)
                        DO NOTHING
                        """,
                        (
                            decision.incident_id,
                            decision.decision_id,
                            decision.event_id,
                            decision.agent_id,
                            decision.risk_level.value,
                            Jsonb(decision.reason_codes),
                            (
                                "BLOCK_ACTION_AND_"
                                "SUSPEND_DEMO_SESSION"
                            ),
                            "open",
                        ),
                    )

            connection.commit()

    def list_decisions(
        self,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        with psycopg.connect(
            self.database_url,
            connect_timeout=5,
            row_factory=dict_row,
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        decision_id,
                        event_id,
                        actor_id,
                        agent_id,
                        session_id,
                        correlation_id,
                        risk_score,
                        final_decision,
                        reason_codes,
                        layer_results,
                        policy_version,
                        evaluated_at,
                        is_synthetic
                    FROM public.security_decisions
                    ORDER BY evaluated_at DESC
                    LIMIT %s
                    """,
                    (limit,),
                )

                return list(cursor.fetchall())

    def list_incidents(
        self,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        with psycopg.connect(
            self.database_url,
            connect_timeout=5,
            row_factory=dict_row,
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        incident_id,
                        decision_id,
                        event_id,
                        agent_id,
                        severity,
                        reason_codes,
                        containment_action,
                        status,
                        created_at
                    FROM public.security_incidents
                    ORDER BY created_at DESC
                    LIMIT %s
                    """,
                    (limit,),
                )

                return list(cursor.fetchall())