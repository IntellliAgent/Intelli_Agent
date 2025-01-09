from typing import Dict, List, Callable
from dataclasses import dataclass
from datetime import datetime
import asyncio


@dataclass
class DecisionStep:
    name: str
    handler: Callable
    required_context: List[str]
    optional_context: List[str] = None
    timeout: float = 30.0


class ComplexDecisionMaker:
    def __init__(self):
        self.steps: Dict[str, DecisionStep] = {}
        self.workflows: Dict[str, List[str]] = {}

    def register_step(self, step: DecisionStep) -> None:
        """Register a decision step."""
        self.steps[step.name] = step

    def create_workflow(self, name: str, step_names: List[str]) -> None:
        """Create a workflow from registered steps."""
        missing_steps = [s for s in step_names if s not in self.steps]
        if missing_steps:
            raise ValueError(f"Steps not registered: {missing_steps}")

        self.workflows[name] = step_names

    async def execute_workflow(
        self,
        workflow_name: str,
        initial_context: Dict
    ) -> Dict:
        """Execute a workflow with given context."""
        if workflow_name not in self.workflows:
            raise ValueError(f"Workflow {workflow_name} not found")

        context = initial_context.copy()
        results = []

        for step_name in self.workflows[workflow_name]:
            step = self.steps[step_name]

            # Validate required context
            missing_context = [
                req for req in step.required_context
                if req not in context
            ]
            if missing_context:
                raise ValueError(
                    f"Missing required context for {
                        step_name}: {missing_context}"
                )

            # Execute step with timeout
            try:
                result = await asyncio.wait_for(
                    step.handler(context),
                    timeout=step.timeout
                )
                results.append({
                    "step": step_name,
                    "result": result,
                    "timestamp": datetime.now().isoformat()
                })

                # Update context with result
                if isinstance(result, dict):
                    context.update(result)

            except asyncio.TimeoutError:
                results.append({
                    "step": step_name,
                    "error": "Timeout",
                    "timestamp": datetime.now().isoformat()
                })
                break

            except Exception as e:
                results.append({
                    "step": step_name,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })
                break

        return {
            "workflow": workflow_name,
            "results": results,
            "final_context": context
        }
