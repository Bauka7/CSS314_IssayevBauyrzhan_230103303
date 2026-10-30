import sys
import os
import platform
import json
import argparse
import multiprocessing
from salt import get_student_params

def collect_telemetry():
    cores = os.cpu_count() or multiprocessing.cpu_count()
    profile = {
        "os": platform.system(),
        "kernel": platform.release(),
        "python_version": sys.version,
        "cpu_model": platform.processor() or "Unknown CPU",
        "physical_cores": cores,
        "logical_cores": cores,
        "cache_line_size_bytes": 64
    }
    return profile

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--student-id", required=True, type=str)
    args = parser.parse_args()

    os.makedirs("results", exist_ok=True)

    profile = collect_telemetry()
    with open("results/host_profile.json", "w") as f:
        json.dump(profile, f, indent=4)

    params = get_student_params(args.student_id)
    with open("results/salted_params.json", "w") as f:
        json.dump(params, f, indent=4)

    print("Milestone 0: Profile and Salted parameters emitted successfully.")