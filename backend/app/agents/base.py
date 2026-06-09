import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """
    Abstract base class for all JobInsight AI agents.
    Provides common functionality like standardized logging, tracing, and error handling.
    """

    def __init__(self, name: str):
        self.name = name
        self.logger = logger.getChild(self.name)

    def log_start(self, task_name: str, **kwargs) -> None:
        """Log the beginning of a processing task."""
        self.logger.info(f"[{self.name}] Starting task: {task_name}", extra=kwargs)

    def log_end(self, task_name: str, **kwargs) -> None:
        """Log the successful completion of a processing task."""
        self.logger.info(f"[{self.name}] Finished task: {task_name}", extra=kwargs)

    def log_error(self, task_name: str, error: Exception, **kwargs) -> None:
        """Log an error that occurred during a task."""
        self.logger.error(
            f"[{self.name}] Error in task {task_name}: {str(error)}",
            exc_info=True,
            extra=kwargs,
        )

    @abstractmethod
    def run(self, *args, **kwargs):
        """Main execution logic. Must be implemented by all child agents."""
        pass
