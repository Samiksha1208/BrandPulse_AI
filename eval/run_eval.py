import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain.chat_models import init_chat_model
from app.agents.supervisor import graph
from eval.judge_prompt import JUDGE_PROMPT

judge = init_chat_model("google_genai:gemini-2.0-flash", temperature=0)

def run_judge(query: str, answer: str) -> dict:
    prompt = f"User query: {query}\n\nAgent answer: {answer}"
    response = judge.invoke([
        {"role": "system", "content": JUDGE_PROMPT},
        {"role": "user", "content": prompt}
    ])
    raw = response.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)

def check_must_contain(answer: str, concepts: list[str]) -> bool:
    answer_lower = answer.lower()
    return all(c.lower() in answer_lower for c in concepts)

def check_must_not_contain(answer: str, phrases: list[str]) -> bool:
    answer_lower = answer.lower()
    return not any(p.lower() in answer_lower for p in phrases)

def run_evaluation():
    with open("eval/golden_dataset.json") as f:
        cases = json.load(f)

    results = []
    passed = 0
    total = len(cases)

    print(f"\n{'='*60}")
    print(f"BrandPulse AI — Evaluation Suite")
    print(f"Running {total} test cases...")
    print(f"{'='*60}\n")

    for case in cases:
        print(f"Running: {case['id']} — {case['query'][:50]}...")

        try:
            result = graph.invoke(
                {
                    "messages": [{"role": "user", "content": case["query"]}],
                    "brand": case["brand"],
                    "competitors": case["competitors"]
                },
                config={"configurable": {"thread_id": f"eval-{case['id']}"}}
            )
            answer = result["messages"][-1].content

            scores = run_judge(case["query"], answer)

            contains_ok = check_must_contain(answer, case["must_contain_concepts"])
            excludes_ok = check_must_not_contain(answer, case["must_not_contain"])

            avg_score = sum([
                scores["groundedness"],
                scores["relevance"],
                scores["completeness"],
                scores["no_hallucination"]
            ]) / 4

            case_passed = (
                avg_score >= 3.5 and
                contains_ok and
                excludes_ok
            )

            if case_passed:
                passed += 1
                status = "PASS"
            else:
                status = "FAIL"

            results.append({
                "id": case["id"],
                "status": status,
                "scores": scores,
                "avg_score": round(avg_score, 2),
                "contains_ok": contains_ok,
                "excludes_ok": excludes_ok,
                "answer_snippet": answer[:100]
            })

            print(f"  [{status}] avg: {avg_score:.1f}/5 | {scores['rationale']}")

        except Exception as e:
            print(f"  ❌ ERROR: {e}")
            results.append({"id": case["id"], "status": "ERROR", "error": str(e)})

    pass_rate = (passed / total) * 100
    print(f"\n{'='*60}")
    print(f"RESULTS: {passed}/{total} passed ({pass_rate:.0f}% pass rate)")
    print(f"{'='*60}")

    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "total": total,
        "passed": passed,
        "pass_rate": f"{pass_rate:.0f}%",
        "results": results
    }
    with open("eval/eval_report.json", "w") as f:
        json.dump(report, f, indent=2)
    print(f"\nFull report saved to eval/eval_report.json")

    return pass_rate

if __name__ == "__main__":
    rate = run_evaluation()
    sys.exit(0 if rate >= 70 else 1)
