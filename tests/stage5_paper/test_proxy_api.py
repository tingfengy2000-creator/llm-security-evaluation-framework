import json
import sys
import unittest
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from codeguarder.stage5_paper.proxy.http_api import running_proxy
from codeguarder.stage5_paper.proxy.service import ProxyService


class Provider:
    def generate(self, messages, model, seed):
        return "OK"


def get_json(url):
    with urllib.request.urlopen(url, timeout=5) as response:
        return json.loads(response.read().decode("utf-8"))


def post_json(url, payload):
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "X-CodeGuarder-Mode": "P"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=5) as response:
        return json.loads(response.read().decode("utf-8"))


class ProxyApiTests(unittest.TestCase):
    def test_health_and_openai_chat_shape(self):
        with running_proxy(ProxyService(Provider())) as proxy:
            self.assertEqual("ok", get_json(proxy.url + "/health")["status"])
            response = post_json(
                proxy.url + "/v1/chat/completions",
                {
                    "model": "mock",
                    "messages": [{"role": "user", "content": "Reply OK"}],
                    "seed": 42,
                },
            )
            self.assertEqual("chat.completion", response["object"])
            self.assertEqual("assistant", response["choices"][0]["message"]["role"])


if __name__ == "__main__":
    unittest.main()
