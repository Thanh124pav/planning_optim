from eval import EXPERIMENTS, ROOT, run_experiment_on_test


def main():
    tests = sorted(
        path
        for path in (ROOT / "tests").glob("test[0-9]*.txt")
        if not path.stem.endswith("_ans")
    )
    print("| ordering rule | repair/fill rounds | score | time_s | correct |")
    print("| --- | ---: | ---: | ---: | ---: |")
    for exp in [item for item in EXPERIMENTS if item["algorithm"] == "greedy"]:
        rows = [run_experiment_on_test(exp, test, 70.0) for test in tests]
        score = sum(row["score"] for row in rows)
        runtime = sum(row["runtime_seconds"] for row in rows)
        correct = sum(1 for row in rows if row["score"] == 100)
        params = exp["hyperparameters"]
        print(
            f"| {params['GREEDY_ORDER_MODE']} | "
            f"{params['GREEDY_REPAIR_FILL_ROUNDS']} | "
            f"{score} | {runtime:.6f} | {correct}/{len(rows)} |"
        )


if __name__ == "__main__":
    main()
