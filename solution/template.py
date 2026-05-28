# """
# Day 1 — LLM API Foundation
# AICB-P1: AI Practical Competency Program, Phase 1
# """

# import os
# import time
# from typing import Any, Callable

# PRICING_1M_TOKENS = {
#     "gpt-4o": {"input": 5.00, "output": 20.00},
#     "gpt-4o-mini": {"input": 0.150, "output": 0.600},
#     "gemini-2.5-flash": {"input": 0.075, "output": 0.300},
#     "gemini-2.5-pro": {"input": 1.25, "output": 5.00},
#     "claude-3-5-sonnet": {"input": 3.00, "output": 15.00},
#     "claude-3-5-haiku": {"input": 0.80, "output": 4.00},
# }

# OPENAI_MODEL = "gpt-4o"
# OPENAI_MINI_MODEL = "gpt-4o-mini"
# GEMINI_MODEL = "gemini-2.5-flash"
# ANTHROPIC_MODEL = "claude-3-5-haiku"


# # ---------------------------------------------------------------------------
# # Task 1 — Call OpenAI
# # ---------------------------------------------------------------------------
# def call_openai(
#     prompt: str,
#     model: str = OPENAI_MODEL,
#     temperature: float = 0.7,
#     top_p: float = 0.9,
#     max_tokens: int = 256,
# ) -> tuple[str, float, dict]:

#     from openai import OpenAI

#     client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#     start = time.time()

#     response = client.chat.completions.create(
#         model=model,
#         messages=[
#             {"role": "user", "content": prompt}
#         ],
#         temperature=temperature,
#         top_p=top_p,
#         max_tokens=max_tokens,
#     )

#     latency = time.time() - start

#     text = response.choices[0].message.content

#     usage = {
#         "input_tokens": response.usage.prompt_tokens,
#         "output_tokens": response.usage.completion_tokens,
#     }

#     return text, latency, usage


# # ---------------------------------------------------------------------------
# # Task 2 — Call Gemini
# # ---------------------------------------------------------------------------
# def call_gemini(
#     prompt: str,
#     model: str = GEMINI_MODEL,
#     temperature: float = 0.7,
#     top_p: float = 0.9,
#     max_tokens: int = 256,
# ) -> tuple[str, float, dict]:

#     from google import genai
#     from google.genai import types

#     client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

#     config = types.GenerateContentConfig(
#         temperature=temperature,
#         top_p=top_p,
#         max_output_tokens=max_tokens,
#     )

#     start = time.time()

#     response = client.models.generate_content(
#         model=model,
#         contents=prompt,
#         config=config,
#     )

#     latency = time.time() - start

#     usage_meta = response.usage_metadata

#     usage = {
#         "input_tokens": usage_meta.prompt_token_count,
#         "output_tokens": usage_meta.candidates_token_count,
#     }

#     return response.text, latency, usage


# # ---------------------------------------------------------------------------
# # Task 3 — Call Anthropic
# # ---------------------------------------------------------------------------
# def call_anthropic(
#     prompt: str,
#     model: str = ANTHROPIC_MODEL,
#     temperature: float = 0.7,
#     top_p: float = 0.9,
#     max_tokens: int = 256,
# ) -> tuple[str, float, dict]:

#     import anthropic

#     client = anthropic.Anthropic(
#         api_key=os.getenv("ANTHROPIC_API_KEY")
#     )

#     start = time.time()

#     response = client.messages.create(
#         model=model,
#         max_tokens=max_tokens,
#         temperature=temperature,
#         top_p=top_p,
#         messages=[
#             {
#                 "role": "user",
#                 "content": prompt
#             }
#         ],
#     )

#     latency = time.time() - start

#     text = response.content[0].text

#     usage = {
#         "input_tokens": response.usage.input_tokens,
#         "output_tokens": response.usage.output_tokens,
#     }

#     return text, latency, usage


# # ---------------------------------------------------------------------------
# # Task 4 — Compare Models
# # ---------------------------------------------------------------------------
# def compare_models(prompt: str) -> dict:

#     def calculate_cost(model_name, usage):
#         pricing = PRICING_1M_TOKENS[model_name]

#         input_cost = (
#             usage["input_tokens"] * pricing["input"]
#         ) / 1_000_000

#         output_cost = (
#             usage["output_tokens"] * pricing["output"]
#         ) / 1_000_000

#         return input_cost + output_cost

#     # GPT-4o
#     response_4o, latency_4o, usage_4o = call_openai(
#         prompt,
#         model=OPENAI_MODEL,
#     )

#     # GPT-4o Mini
#     response_mini, latency_mini, usage_mini = call_openai(
#         prompt,
#         model=OPENAI_MINI_MODEL,
#     )

#     # Gemini Flash
#     response_gemini, latency_gemini, usage_gemini = call_gemini(
#         prompt,
#         model=GEMINI_MODEL,
#     )

#     return {
#         "gpt4o": {
#             "response": response_4o,
#             "latency": latency_4o,
#             "cost": calculate_cost(OPENAI_MODEL, usage_4o),
#             "input_tokens": usage_4o["input_tokens"],
#             "output_tokens": usage_4o["output_tokens"],
#         },
#         "gpt4o_mini": {
#             "response": response_mini,
#             "latency": latency_mini,
#             "cost": calculate_cost(OPENAI_MINI_MODEL, usage_mini),
#             "input_tokens": usage_mini["input_tokens"],
#             "output_tokens": usage_mini["output_tokens"],
#         },
#         "gemini_flash": {
#             "response": response_gemini,
#             "latency": latency_gemini,
#             "cost": calculate_cost(GEMINI_MODEL, usage_gemini),
#             "input_tokens": usage_gemini["input_tokens"],
#             "output_tokens": usage_gemini["output_tokens"],
#         },
#     }


# # ---------------------------------------------------------------------------
# # Task 5 — Streaming Chatbot
# # ---------------------------------------------------------------------------
# def streaming_chatbot() -> None:

#     from google import genai

#     client = genai.Client(
#         api_key=os.getenv("GEMINI_API_KEY")
#     )

#     history = []

#     print("Gemini Chatbot Started!")

#     while True:

#         user_input = input("\nYou: ")

#         if user_input.lower() in ["quit", "exit"]:
#             print("Goodbye!")
#             break

#         history.append({
#             "role": "user",
#             "content": user_input,
#         })

#         history = history[-6:]

#         prompt = ""

#         for msg in history:
#             prompt += f"{msg['role']}: {msg['content']}\n"

#         print("\nGemini: ", end="", flush=True)

#         stream = client.models.generate_content_stream(
#             model=GEMINI_MODEL,
#             contents=prompt,
#         )

#         assistant_response = ""

#         for chunk in stream:
#             if chunk.text:
#                 print(chunk.text, end="", flush=True)
#                 assistant_response += chunk.text

#         print()

#         history.append({
#             "role": "assistant",
#             "content": assistant_response,
#         })


# # ---------------------------------------------------------------------------
# # Bonus Task A — Retry with backoff
# # ---------------------------------------------------------------------------
# def retry_with_backoff(
#     fn: Callable[[], Any],
#     max_retries: int = 3,
#     base_delay: float = 0.1,
# ) -> Any:

#     for attempt in range(max_retries + 1):

#         try:
#             return fn()

#         except Exception:

#             if attempt == max_retries:
#                 raise

#             delay = base_delay * (2 ** attempt)
#             time.sleep(delay)


# # ---------------------------------------------------------------------------
# # Bonus Task B — Batch compare
# # ---------------------------------------------------------------------------
# def batch_compare(prompts: list[str]) -> list[dict]:

#     results = []

#     for prompt in prompts:

#         comparison = compare_models(prompt)

#         comparison["prompt"] = prompt

#         results.append(comparison)

#     return results


# # ---------------------------------------------------------------------------
# # Bonus Task C — Format comparison table
# # ---------------------------------------------------------------------------
# def format_comparison_table(results: list[dict]) -> str:

#     table = (
#         "| Prompt | Model | Response | Latency | Tokens (In/Out) | Cost |\n"
#         "|---|---|---|---|---|---|\n"
#     )

#     for result in results:

#         prompt = result["prompt"]

#         for model_name in ["gpt4o", "gpt4o_mini", "gemini_flash"]:

#             stats = result[model_name]

#             response = stats["response"][:50].replace("\n", " ")

#             latency = f"{stats['latency']:.2f}s"

#             tokens = (
#                 f"{stats['input_tokens']}/{stats['output_tokens']}"
#             )

#             cost = f"${stats['cost']:.6f}"

#             table += (
#                 f"| {prompt} | "
#                 f"{model_name} | "
#                 f"{response} | "
#                 f"{latency} | "
#                 f"{tokens} | "
#                 f"{cost} |\n"
#             )

#     return table

"""
Day 1 — LLM API Foundation
"""

import os
import time
from typing import Any, Callable

from openai import OpenAI
from google import genai
from google.genai import types
import anthropic


PRICING_1M_TOKENS = {
    "gpt-4o": {"input": 5.00, "output": 20.00},
    "gpt-4o-mini": {"input": 0.150, "output": 0.600},
    "gemini-2.5-flash": {"input": 0.075, "output": 0.300},
}

OPENAI_MODEL = "gpt-4o"
OPENAI_MINI_MODEL = "gpt-4o-mini"
GEMINI_MODEL = "gemini-2.5-flash"
ANTHROPIC_MODEL = "claude-3-5-haiku"


# ---------------------------------------------------------------------------
# Task 1 — Call OpenAI
# ---------------------------------------------------------------------------
def call_openai(
    prompt: str,
    model: str = OPENAI_MODEL,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float, dict]:

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    start = time.time()

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )

    latency = time.time() - start

    text = response.choices[0].message.content

    usage = {
        "input_tokens": response.usage.prompt_tokens,
        "output_tokens": response.usage.completion_tokens,
    }

    return text, latency, usage


# ---------------------------------------------------------------------------
# Task 2 — Call Gemini
# ---------------------------------------------------------------------------
def call_gemini(
    prompt: str,
    model: str = GEMINI_MODEL,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float, dict]:

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    config = types.GenerateContentConfig(
        temperature=temperature,
        top_p=top_p,
        max_output_tokens=max_tokens,
    )

    start = time.time()

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=config,
    )

    latency = time.time() - start

    usage = {
        "input_tokens": response.usage_metadata.prompt_token_count,
        "output_tokens": response.usage_metadata.candidates_token_count,
    }

    return response.text, latency, usage


# ---------------------------------------------------------------------------
# Task 3 — Call Anthropic
# ---------------------------------------------------------------------------
def call_anthropic(
    prompt: str,
    model: str = ANTHROPIC_MODEL,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float, dict]:

    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    start = time.time()

    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        messages=[{"role": "user", "content": prompt}],
    )

    latency = time.time() - start

    text = response.content[0].text

    usage = {
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
    }

    return text, latency, usage


# ---------------------------------------------------------------------------
# Task 4 — Compare Models
# ---------------------------------------------------------------------------
def compare_models(prompt: str) -> dict:

    def calc_cost(model_name, usage):
        pricing = PRICING_1M_TOKENS[model_name]
        return (
            usage["input_tokens"] * pricing["input"]
            + usage["output_tokens"] * pricing["output"]
        ) / 1_000_000

    r4o, l4o, u4o = call_openai(prompt, model=OPENAI_MODEL)
    rmini, lmini, umini = call_openai(prompt, model=OPENAI_MINI_MODEL)
    rgem, lgem, ugem = call_gemini(prompt, model=GEMINI_MODEL)

    return {
        "gpt4o": {
            "response": r4o,
            "latency": l4o,
            "cost": calc_cost("gpt-4o", u4o),
            "input_tokens": u4o["input_tokens"],
            "output_tokens": u4o["output_tokens"],
        },
        "gpt4o_mini": {
            "response": rmini,
            "latency": lmini,
            "cost": calc_cost("gpt-4o-mini", umini),
            "input_tokens": umini["input_tokens"],
            "output_tokens": umini["output_tokens"],
        },
        "gemini_flash": {
            "response": rgem,
            "latency": lgem,
            "cost": calc_cost("gemini-2.5-flash", ugem),
            "input_tokens": ugem["input_tokens"],
            "output_tokens": ugem["output_tokens"],
        },
    }


# ---------------------------------------------------------------------------
# Task 5 — Streaming chatbot
# ---------------------------------------------------------------------------
def streaming_chatbot() -> None:

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    history = []

    print("Gemini Chatbot Started!")

    while True:
        user_input = input("\nYou: ")

        if user_input.lower() in ["quit", "exit"]:
            print("Goodbye!")
            break

        history.append({"role": "user", "content": user_input})
        history = history[-6:]

        prompt = ""
        for msg in history:
            prompt += f"{msg['role']}: {msg['content']}\n"

        print("\nGemini: ", end="", flush=True)

        stream = client.models.generate_content_stream(
            model=GEMINI_MODEL,
            contents=prompt,
        )

        response_text = ""

        for chunk in stream:
            if chunk.text:
                print(chunk.text, end="", flush=True)
                response_text += chunk.text

        print()

        history.append({"role": "assistant", "content": response_text})


# ---------------------------------------------------------------------------
# Bonus A — Retry with backoff (FIXED ✅)
# ---------------------------------------------------------------------------
def retry_with_backoff(
    fn: Callable[[], Any],
    max_retries: int = 3,
    base_delay: float = 0.1,
) -> Any:

    for attempt in range(max_retries + 1):

        try:
            return fn()

        except Exception:

            if attempt == max_retries:
                raise

            delay = base_delay * (2 ** attempt)
            time.sleep(delay)


# ---------------------------------------------------------------------------
# Bonus B — Batch compare
# ---------------------------------------------------------------------------
def batch_compare(prompts: list[str]) -> list[dict]:

    results = []

    for prompt in prompts:
        res = compare_models(prompt)
        res["prompt"] = prompt
        results.append(res)

    return results


# ---------------------------------------------------------------------------
# Bonus C — Format table
# ---------------------------------------------------------------------------
def format_comparison_table(results: list[dict]) -> str:

    table = (
        "| Prompt | Model | Response | Latency | Tokens (In/Out) | Cost |\n"
        "|---|---|---|---|---|---|\n"
    )

    for item in results:

        prompt = item["prompt"]

        for model_key in ["gpt4o", "gpt4o_mini", "gemini_flash"]:

            data = item[model_key]

            response = data["response"][:50].replace("\n", " ")
            latency = f"{data['latency']:.2f}s"
            tokens = f"{data['input_tokens']}/{data['output_tokens']}"
            cost = f"${data['cost']:.6f}"

            table += (
                f"| {prompt} "
                f"| {model_key} "
                f"| {response} "
                f"| {latency} "
                f"| {tokens} "
                f"| {cost} |\n"
            )

    return table


