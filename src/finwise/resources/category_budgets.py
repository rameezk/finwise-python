"""Category budgets resource."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from finwise.models.category_budget import AggregatedCategoryBudget
from finwise.resources._base import BaseResource


class CategoryBudgetsResource(BaseResource):
    """
    Category Budgets API resource.

    Provides methods for retrieving aggregated category budget information.

    Example:
        >>> client = FinWise(api_key="your-key")
        >>>
        >>> # Get aggregated budgets
        >>> budgets = client.category_budgets.aggregated(currency_code="ZAR")
        >>> for budget in budgets:
        ...     print(f"Category {budget.category_id}: {budget.amount}")
    """

    _path = "/category-budgets"

    def aggregated(
        self,
        *,
        currency_code: str,
        aggregate_by: Optional[list[str]] = None,
        from_budget_period_to: Optional[datetime] = None,
    ) -> list[AggregatedCategoryBudget]:
        """
        Get aggregated category budget totals.

        Args:
            currency_code: Currency code for aggregation (e.g., "ZAR", "USD").
            aggregate_by: Fields to aggregate by (default: ["transactionCategoryId", "transactionType"]).
            from_budget_period_to: End date for the budget period filter.

        Returns:
            List of aggregated category budget totals.

        Example:
            >>> # Get budget totals by category
            >>> budgets = client.category_budgets.aggregated(
            ...     currency_code="ZAR",
            ... )
            >>> for budget in budgets:
            ...     print(f"Category {budget.category_id}: {budget.amount} ({budget.transaction_type})")
            >>>
            >>> # Filter by budget period
            >>> from datetime import datetime
            >>> budgets = client.category_budgets.aggregated(
            ...     currency_code="ZAR",
            ...     from_budget_period_to=datetime(2024, 3, 1),
            ... )
        """
        if aggregate_by is None:
            aggregate_by = ["transactionCategoryId", "transactionType"]

        filters: dict[str, object] = {
            "fromBudgetPeriodFromForCategoryIds": {},
        }
        if from_budget_period_to:
            filters["fromBudgetPeriodTo"] = from_budget_period_to.isoformat() + "+00:00"

        body = {
            "filters": filters,
            "currencyCode": currency_code,
            "aggregateBy": aggregate_by,
        }

        response = self._transport.post(f"{self._path}/aggregated", json=body)

        items = response if isinstance(response, list) else []
        return [AggregatedCategoryBudget.model_validate(item) for item in items]
