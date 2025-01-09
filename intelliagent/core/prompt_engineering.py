from typing import Dict, List, Optional
from pydantic import BaseModel
import json
import os


class PromptTemplate(BaseModel):
    name: str
    template: str
    variables: List[str]
    description: Optional[str] = None
    domain: Optional[str] = None
    examples: Optional[List[Dict]] = None


class PromptEngine:
    def __init__(self, templates_dir: str = "prompts"):
        self.templates_dir = templates_dir
        self.templates: Dict[str, PromptTemplate] = {}
        self._load_templates()

    def _load_templates(self) -> None:
        """Load prompt templates from files."""
        os.makedirs(self.templates_dir, exist_ok=True)
        for filename in os.listdir(self.templates_dir):
            if filename.endswith('.json'):
                with open(os.path.join(self.templates_dir, filename)) as f:
                    template_data = json.load(f)
                    template = PromptTemplate(**template_data)
                    self.templates[template.name] = template

    def generate_prompt(
        self,
        template_name: str,
        variables: Dict[str, str],
        context: Optional[Dict] = None
    ) -> str:
        """Generate a prompt from a template."""
        if template_name not in self.templates:
            raise ValueError(f"Template {template_name} not found")

        template = self.templates[template_name]
        prompt = template.template

        # Replace variables
        for var in template.variables:
            if var not in variables:
                raise ValueError(f"Missing variable {var}")
            prompt = prompt.replace(f"{{{var}}}", variables[var])

        # Add context if available
        if context:
            prompt += f"\nContext: {json.dumps(context)}"

        return prompt

    def add_template(self, template: PromptTemplate) -> None:
        """Add a new prompt template."""
        self.templates[template.name] = template

        # Save to file
        filename = f"{template.name}.json"
        filepath = os.path.join(self.templates_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(template.dict(), f, indent=2)
