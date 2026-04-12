"""
Kakeya Set Verification Script with Robust Coverage Detection
==============================================================
Verifies Lebesgue measure and directional coverage of a candidate Kakeya set.
Handles extremely sparse sets (e.g., single-point support) by using a
deterministic line traversal instead of random sampling.

Usage:
    python verify_kakeya.py path/to/kakeya_5d_N16.npz
"""

import numpy as np
import sys
import os

def load_dataset(filepath):
    data = np.load(filepath)
    required = ['grid_shape', 'dx', 'support']
    for key in required:
        if key not in data:
            raise ValueError(f"Missing required field: {key}")
    shape = tuple(data['grid_shape'])
    support = data['support']
    if support.shape != shape:
        raise ValueError(f"Shape mismatch: support shape {support.shape} != {shape}")
    dx = float(data['dx'])
    L = float(data['L']) if 'L' in data else shape[0] * dx
    return shape, dx, L, support

def compute_measure(support, dx):
    vol_element = dx ** len(support.shape)
    return np.sum(support) * vol_element

def random_unit_vector(dim):
    v = np.random.randn(dim)
    return v / np.linalg.norm(v)

def check_direction_deterministic(support, dx, L, direction, center, segment_length=1.0):
    """
    Check coverage by tracing the entire line segment and checking ALL grid cells
    it passes through. This guarantees detection even for single-point supports.
    """
    dim = len(support.shape)
    N = support.shape[0]
    # Step size small enough to hit every grid cell along the line
    # Use half the grid spacing to ensure no cell is skipped
    step_size = dx / 2.0
    s = -segment_length / 2.0
    while s <= segment_length / 2.0:
        phys = center + s * direction
        idx = tuple(int(np.floor(coord / dx)) % N for coord in phys)
        if support[idx]:
            return True
        s += step_size
    return False

def check_direction_sampling(support, dx, L, direction, center, segment_length=1.0, num_samples=30):
    """
    Fast sampling-based check (suitable for dense supports).
    """
    dim = len(support.shape)
    N = support.shape[0]
    s_vals = np.linspace(-segment_length/2, segment_length/2, num_samples)
    for s in s_vals:
        phys = center + s * direction
        idx = tuple(int(np.floor(coord / dx)) % N for coord in phys)
        if support[idx]:
            return True
    return False

def verify_coverage(support, dx, L, num_directions=500, segment_length=1.0):
    dim = len(support.shape)
    center = np.full(dim, L/2.0)
    support_count = np.sum(support)
    
    # Choose method based on sparsity
    if support_count < 100:
        print(f"Using deterministic tracing (support points = {support_count} < 100)")
        check_func = lambda d: check_direction_deterministic(support, dx, L, d, center, segment_length)
    else:
        print(f"Using fast sampling (support points = {support_count} >= 100)")
        check_func = lambda d: check_direction_sampling(support, dx, L, d, center, segment_length)
    
    covered = 0
    for _ in range(num_directions):
        direction = random_unit_vector(dim)
        if check_func(direction):
            covered += 1
    return covered / num_directions

def classify_state(measure_fraction, support_fraction, coverage_passed):
    if not coverage_passed:
        return "COVERAGE FAILED (not a Kakeya set)"
    if measure_fraction < 0.01 and support_fraction < 0.05:
        return "STABLE KAKEYA PHASE"
    elif measure_fraction < 0.10 and support_fraction < 0.20:
        return "METASTABLE / PARTIALLY COMPRESSED"
    else:
        return "UNIFORM / TRIVIAL STATE"

def main():
    if len(sys.argv) < 2:
        print("Usage: python verify_kakeya.py <dataset.npz>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        sys.exit(1)
    
    print(f"Loading dataset: {filepath}")
    shape, dx, L, support = load_dataset(filepath)
    dim = len(shape)
    total_points = np.prod(shape)
    support_points = np.sum(support)
    
    print(f"Dimension: {dim}D")
    print(f"Grid size: {shape}")
    print(f"dx = {dx:.4f}, L = {L:.4f}")
    print(f"Support points: {support_points} / {total_points}")
    
    measure = compute_measure(support, dx)
    volume_full = L ** dim
    measure_fraction = measure / volume_full
    support_fraction = support_points / total_points
    
    print(f"\n--- Measure ---")
    print(f"Discrete Lebesgue measure: {measure:.6f}")
    print(f"Relative measure: {measure_fraction:.6%}")
    
    print(f"\n--- Directional Coverage Test (random 500 directions) ---")
    coverage = verify_coverage(support, dx, L, num_directions=500, segment_length=1.0)
    print(f"Coverage rate: {coverage*100:.1f}%")
    
    coverage_passed = coverage > 0.95
    if coverage_passed:
        print("✓ Coverage test PASSED")
    else:
        print("✗ Coverage test FAILED")
    
    print(f"\n--- State Classification ---")
    state = classify_state(measure_fraction, support_fraction, coverage_passed)
    print(f"Conclusion: {state}")

if __name__ == "__main__":
    main()
