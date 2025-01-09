from typing import Dict, Any
import openai
from datetime import datetime


class GPTModel:
    def __init__(self, api_key: str, model_name: str = "gpt-4"):
        """Initialize the GPT model."""
        self.model_name = model_name
        openai.api_key = api_key

    def process_input(self, input_text: str, context: Dict) -> Dict[str, Any]:
        """Process input using the GPT model."""
        # Prepare the prompt
        prompt = self._prepare_prompt(input_text, context)

        try:
            # Make API call
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=150,
                n=1,
                stop=None
            )

            # Extract and process response
            result = response.choices[0].message.content

            # Parse the response
            parsed_result = self._parse_response(result)

            return {
                "decision": parsed_result.get("decision"),
                "reasoning": parsed_result.get("reasoning", []),
                "predictions": [0.8],  # Placeholder for actual predictions
                "raw_response": result,
                "model": self.model_name,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            raise RuntimeError(f"Error processing input: {str(e)}")

    def _prepare_prompt(self, input_text: str, context: Dict) -> str:
        """Prepare the prompt with context."""
        context_str = "\n".join(
            f"{k}: {v}"
            for k, v in context.items()
        )
        return f"""Input: {input_text}

Context:
{context_str}

Please provide a decision and reasoning."""

    def _get_system_prompt(self) -> str:
        """Get the system prompt."""
        return """You are an intelligent decision-making assistant.
        Analyze the input and context carefully, then provide a clear decision
        with step-by-step reasoning."""

    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse the model's response into structured format."""
        # Simple parsing for now
        lines = response.split('\n')
        decision = lines[0] if lines else ""
        reasoning = lines[1:] if len(lines) > 1 else []

        return {
            "decision": decision,
            "reasoning": reasoning
        }
