import os

import agentlens
from haystack.components.generators.openai import OpenAIGenerator


def main():
    agentlens.init(os.getenv("AGENTLENS_API_KEY"))

    if not os.getenv("OPENAI_API_KEY"):
        print("Skipping OpenAI example: missing OPENAI_API_KEY")
        return

    tracer = agentlens.start_trace(
        trace_name="Haystack OpenAI Example",
        tags=["haystack", "openai", "agentlens-example"],
    )

    prompt = "In one sentence, what is agentlens?"
    generator = OpenAIGenerator(model="gpt-4o-mini")
    result = generator.run(prompt=prompt)
    replies = result.get("replies") or []
    print("Haystack reply:", replies[0] if replies else "<no reply>")

    print("\n" + "=" * 50)
    print("Now let's verify that our LLM calls were tracked properly with agentlens...")
    try:
        validation_result = agentlens.validate_trace_spans(trace_context=tracer)
        agentlens.print_validation_summary(validation_result)
    except agentlens.ValidationError as e:
        print(f"\n❌ Error validating spans: {e}")
        raise

    agentlens.end_trace(tracer, end_state="Success")


if __name__ == "__main__":
    main()
