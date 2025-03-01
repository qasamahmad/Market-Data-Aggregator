from abc import ABC, abstractmethod
from typing import Any, Optional
import pandas as pd

class BaseDataSource(ABC):
    """Abstract base for market data sources."""

    @abstractmethod
    def fetch_data(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **kwargs: Any
    ) -> pd.DataFrame:
        """Fetch market data for a symbol and return it as a DataFrame."""
        pass