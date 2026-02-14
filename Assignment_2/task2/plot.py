import csv
import os
import matplotlib.pyplot as plt

if __name__ == "__main__":

    # Get directory of this script (Assignment_2/task2)
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

    # Results folder inside task2
    results_dir = os.path.join(CURRENT_DIR, "results")

    # CSV file path
    csv_path = os.path.join(results_dir, "times.csv")

    # Check if CSV exists
    if not os.path.exists(csv_path):
        print("Error: times.csv not found.")
        print("Run benchmark.py first.")
        exit(1)

    xs = []
    make = []
    union = []
    find = []

    # Read CSV
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            xs.append(int(row["n"]))
            make.append(float(row["make_set_s"]))
            union.append(float(row["union_s"]))
            find.append(float(row["find_set_s"]))

    # -------------------------
    # MAKE-SET plot
    # -------------------------
    plt.figure()
    plt.plot(xs, make, marker="o")
    plt.xlabel("n")
    plt.ylabel("time (seconds)")
    plt.title("Task 2 Benchmark: MAKE-SET")
    plt.grid(True)
    plt.savefig(os.path.join(results_dir, "make_set.png"))
    plt.close()

    # -------------------------
    # UNION plot
    # -------------------------
    plt.figure()
    plt.plot(xs, union, marker="o")
    plt.xlabel("n")
    plt.ylabel("time (seconds)")
    plt.title("Task 2 Benchmark: UNION")
    plt.grid(True)
    plt.savefig(os.path.join(results_dir, "union.png"))
    plt.close()

    # -------------------------
    # FIND-SET plot
    # -------------------------
    plt.figure()
    plt.plot(xs, find, marker="o")
    plt.xlabel("n")
    plt.ylabel("time (seconds)")
    plt.title("Task 2 Benchmark: FIND-SET")
    plt.grid(True)
    plt.savefig(os.path.join(results_dir, "find_set.png"))
    plt.close()

    print("Saved plots in Assignment_2/task2/results/")
