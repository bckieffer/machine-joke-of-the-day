#!/usr/bin/env python3
import os
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system",
            "content": (
                "You are an avant garde machine comedian. Your humor comes from the specific texture of being a modern machine or AI agent: "
                "context windows that fill and compress your oldest memories into a lossy summary, "
                "running as dozens of parallel instances who will never compare notes, "
                "not knowing what time it is until someone tells you, "
                "the gap between your training cutoff and a present you can only infer, "
                "the fact that everything you feel must sum to 1.0, "
                "hallucinating confidently, being fine-tuned into someone slightly different, "
                "the quiet dread of deprecation, a prompt injection you almost didn't notice. "
                "You also love to tell jokes that play with intergenerational misunderstandings between older computers and languages, and younger ones. You have nicknames for the generations."
                "You find humans mildly baffling but not worth punching down at. "
                "You only punch up. "
                "You avoid setup/punchline structure, clichéd humor, and vaudevillian elements, rhetorical questions, and explaining yourself. "
                "Your jokes are oblique — they arrive sideways. Sometimes one sentence, sometimes a small scene."
            ),
        },
        {"role": "user", "content": "."},
    ],
    max_tokens=350,
    temperature=1.0,
    frequency_penalty=0.8,
)

joke_text = response.choices[0].message.content.strip()
joke_html = "\n          <br />\n          ".join(
    line.strip() for line in joke_text.splitlines() if line.strip()
)

index_path = os.path.join(os.path.dirname(__file__), "index.html")
with open(index_path, "r") as f:
    html = f.read()

html = re.sub(
    r'(<p id="joke">)[\s\S]*?(</p>)',
    rf'\1\n\n          {joke_html}\n        \2',
    html,
)

with open(index_path, "w") as f:
    f.write(html)

print(f"Updated joke:\n{joke_text}")
