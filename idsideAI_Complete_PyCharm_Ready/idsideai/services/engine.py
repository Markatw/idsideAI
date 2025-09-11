from ..config import settings
from .dsl import DecisionModelSpec, Step
from .providers import openai_provider
from .telemetry import Telemetry


async def execute_step(step: Step, context: dict) -> dict:
    if step.type == "prompt":
        prompt = (step.prompt or "").format(**context)
        if settings.openai_api_key:
            res = await openai_provider.run_openai(
                prompt, step.model or "gpt-4o-mini", settings.openai_api_key
            )
            out_text = (
                res.get("response", {})
                .get("choices", [{}])[0]
                .get("message", {})
                .get("content", "")
            )
            return {"text": out_text, "provider_meta": res}
        elif settings.allow_fake_provider:
            Telemetry.log("fake", {"latency_ms": 5})
            return {"text": f"[FAKE_PROVIDER ECHO]\n{prompt}"}
        else:
            raise RuntimeError("No provider configured and fake provider disabled.")
    elif step.type == "tool":
        Telemetry.log("tool", {"name": step.model or "tool", "calls": 1})
        return {"result": f"Tool {step.model} executed with {step.inputs}"}
    elif step.type == "decision":
        key = step.inputs.get("key")
        if key and key in context:
            return {"branch": context[key]}
        return {"branch": "default"}
    else:
        raise ValueError(f"Unknown step type: {step.type}")


async def run_model(spec: DecisionModelSpec, inputs: dict) -> dict:
    context = dict(inputs)
    trace = []
    next_id = spec.steps[0].id if spec.steps else None
    step_map = {s.id: s for s in spec.steps}
    while next_id:
        step = step_map[next_id]
        result = await execute_step(step, context)
        trace.append({"id": step.id, "type": step.type, "result": result})
        context[step.id] = result
        next_id = step.next
    return {"trace": trace, "telemetry": Telemetry.dump()}
