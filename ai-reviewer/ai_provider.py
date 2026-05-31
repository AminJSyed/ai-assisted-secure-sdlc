import json
import os
import urllib.request
import urllib.error


class AIProvider:
    def __init__(self):
        self.provider = os.getenv("AI_PROVIDER", "rule_based").strip().lower()
        self.api_url = os.getenv("AI_API_URL", "").strip()
        self.api_key = os.getenv("AI_API_KEY", "").strip()

    def generate(self, prompt: str) -> str:
        if self.provider == "mock":
            return self._mock_response(prompt)

        if self.provider == "external":
            return self._external_response(prompt)

        return self._rule_based_response(prompt)

    def _rule_based_response(self, prompt: str) -> str:
        return (
            "AI provider mode: rule_based\n\n"
            "The review was generated using deterministic local security rules. "
            "This mode is safe for CI/CD because it does not require an external AI API key. "
            "The output should be treated as advisory and validated by a human reviewer."
        )

    def _mock_response(self, prompt: str) -> str:
        return (
            "AI provider mode: mock\n\n"
            "This is a simulated AI-assisted response. "
            "It represents how an LLM-style assistant could summarize risk, remediation, and release impact "
            "without calling a real external provider."
        )

    def _external_response(self, prompt: str) -> str:
        if not self.api_url or not self.api_key:
            return (
                "AI provider mode: external\n\n"
                "External provider was requested, but AI_API_URL or AI_API_KEY was not configured. "
                "Falling back to local advisory behavior. No external request was made."
            )

        payload = json.dumps({"prompt": prompt}).encode("utf-8")

        request = urllib.request.Request(
            self.api_url,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                body = response.read().decode("utf-8")
                return (
                    "AI provider mode: external\n\n"
                    "External provider response received.\n\n"
                    f"{body}"
                )
        except urllib.error.URLError as error:
            return (
                "AI provider mode: external\n\n"
                "External provider request failed. "
                f"Reason: {error}. "
                "The workflow should continue in advisory mode unless policy requires a hard failure."
            )
