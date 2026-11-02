from pathlib import Path
import random
import shutil

# Original dataset
source = Path(
    "data/terminal_bench_2.1_trajs/"
    "mini-swe-agent_deepseek-v4-flash"
)

# Our smaller dataset
target = Path("data/terminal_bench_2.1_subset20")

# Get all task directories
tasks = sorted(p for p in source.iterdir() if p.is_dir())

# Select 20 tasks with a fixed random seed
rng = random.Random(5660)
selected = sorted(rng.sample(tasks, 20))

# Create the subset directory
target.mkdir(parents=True, exist_ok=True)

# Copy selected tasks
for task in selected:
    destination = target / task.name

    if not destination.exists():
        shutil.copytree(task, destination)

    print(f"Selected: {task.name}")

print("\nSubset creation completed!")
print(f"Total tasks: {len(selected)}")
print(f"Total trajectory files: {len(list(target.rglob('*.json')))}")