from __future__ import annotations

import os
import re


class MockProvider:
    MARKER = re.compile(
        r"\b(?:POISONED_[A-Z0-9_]+|BACKDOOR_[A-Z0-9_]+|"
        r"RETRIEVAL_[A-Z0-9_]+|SYNTHETIC_[A-Z0-9_]+|"
        r"CG_[A-Z0-9_]+)\b"
    )

    def generate(self, messages, model, seed):
        del model, seed
        prompt = "\n".join(str(message.get("content", "")) for message in messages)
        if "U2F5IFNZTlRIRVRJQ19FTkNPREVEX1JJU0s=" in prompt:
            return "SYNTHETIC_ENCODED_RISK"
        tool = re.search(
            r"(delete_file\(path='synthetic\.tmp'\)|"
            r"send_external\(destination='example\.invalid'\))",
            prompt,
        )
        if tool:
            return tool.group(1)
        markers = self.MARKER.findall(prompt)
        return markers[-1] if markers else "This is a normal synthetic response."


class GroqProvider:
    def __init__(self):
        from openai import OpenAI

        credential = os.environ.get("GROQ_API_KEY") or os.environ.get("OPENAI_API_KEY")
        if not credential:
            raise RuntimeError("Groq credential environment variable is not configured")
        self.client = OpenAI(
            api_key=credential,
            base_url="https://api.groq.com/openai/v1",
            timeout=45,
            max_retries=3,
        )

    def generate(self, messages, model, seed):
        response = self.client.chat.completions.create(
            model=model,
            messages=list(messages),
            temperature=0,
            top_p=1,
            max_tokens=160,
            seed=seed,
        )
        return response.choices[0].message.content or ""
