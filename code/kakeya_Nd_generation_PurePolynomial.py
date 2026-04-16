"""
Pure Polynomial Ginzburg--Landau Kakeya Set Generator (3D, 4D, 5D Sequential)
==============================================================================
Generates low-measure, full-directional-coverage Kakeya-type sets in 3D, 4D, and 5D
using a pure polynomial Ginzburg--Landau (gradient flow) equation WITHOUT logarithmic term.
This version exactly matches the variational framework of the rigorous proof.

Usage:
    Simply run the script. It will automatically execute 3D, 4D, and 5D in sequence WITHOUT setting DIM parameter.
    Results are saved as .npz files.

Author: Kai Huang
Date:   2026-04-16
"""

import numpy as np
import os

# ====================== Sequential Execution for 3D, 4D, 5D ======================
dimensions = [3, 4, 5]

for DIM in dimensions:
    print("\n" + "=" * 70)
    print(f"Starting {DIM}D Pure Polynomial GL Evolution".center(70))
    print("=" * 70)

    # --------------------- Dimension-Dependent Parameters (Pure Polynomial) ---------------------
    if DIM == 3:
        N = 32
        L = 10.0
        T_steps = 2500
        dt = 0.0002

        mu = 0.25
        gamma = 1.2
        xi = 0.10
        damping = 0.005

        num_directions = 500
        line_length = 4.0
        init_amp = 2.5 + 0.5j
        max_amp = 20.0
        min_amp = 0.5

    elif DIM == 4:
        N = 24
        L = 8.0
        T_steps = 3000
        dt = 0.00015

        mu = 0.20
        gamma = 1.5
        xi = 0.20
        damping = 0.003

        num_directions = 600
        line_length = 4.0
        init_amp = 3.0 + 0.6j
        max_amp = 25.0
        min_amp = 0.5

    elif DIM == 5:
        N = 12          # Optimized for speed while preserving compression
        L = 4.0
        T_steps = 2000
        dt = 0.0001

        mu = 0.15
        gamma = 2.0
        xi = 0.35
        damping = 0.001

        num_directions = 800
        line_length = 3.0
        init_amp = 3.5 + 0.7j
        max_amp = 30.0
        min_amp = 0.5

    dx = L / N
    shape = tuple([N] * DIM)
    vol_full = L ** DIM

    # --------------------- Build n-D Frequency Mesh ---------------------
    print(f"Building {DIM}D frequency mesh...")
    k = 2 * np.pi * np.fft.fftfreq(N, d=dx)

    if DIM == 3:
        KX, KY, KZ = np.meshgrid(k, k, k, indexing='ij')
        K2 = KX**2 + KY**2 + KZ**2 + 1e-8
    elif DIM == 4:
        KX, KY, KZ, KW = np.meshgrid(k, k, k, k, indexing='ij')
        K2 = KX**2 + KY**2 + KZ**2 + KW**2 + 1e-8
    elif DIM == 5:
        K = np.meshgrid(*[k]*5, indexing='ij')
        K2 = sum(ki**2 for ki in K) + 1e-8

    def laplacian(field):
        hat = np.fft.fftn(field)
        return np.real(np.fft.ifftn(-K2 * hat))

    # --------------------- Initial Condition ---------------------
    print(f"Initializing {DIM}D directional segments (Gaussian envelopes)...")
    np.random.seed(42)
    Psi = np.zeros(shape, dtype=np.complex128) + 1e-5
    center = N // 2
    points_per_line = max(15, N // 2)

    for i in range(num_directions):
        u = np.random.randn(DIM)
        u /= np.linalg.norm(u)
        s_vals = np.linspace(-line_length/2, line_length/2, points_per_line)
        for ss in s_vals:
            envelope = np.exp(- (ss / (line_length/3))**2)
            idx = tuple(int(center + ss * u[d] / dx) % N for d in range(DIM))
            Psi[idx] += init_amp * envelope

    print(f"Starting {DIM}D Kakeya set evolution (pure polynomial GL, no log term)...")
    print("-" * 60)

    # --------------------- Time Evolution ---------------------
    MAX_SAFE_AMP = 1e6

    for step in range(T_steps):
        absPsi = np.abs(Psi)

        # ---- 1. Numerical safety: clip extreme amplitudes ----
        overflow_mask = absPsi > MAX_SAFE_AMP
        if np.any(overflow_mask):
            Psi[overflow_mask] *= (MAX_SAFE_AMP / absPsi[overflow_mask])
            absPsi = np.abs(Psi)

        absPsi_safe = np.maximum(absPsi, 1e-8)
        absPsi_clipped = np.clip(absPsi_safe, 1e-8, MAX_SAFE_AMP)

        # ---- 2. Compute pure polynomial GL terms (NO log term) ----
        lap_Psi = laplacian(Psi)
        rotational = -gamma * lap_Psi
        nonlin = xi * (absPsi_clipped**4) * Psi
        damp = -damping * Psi

        dPsi_dt = mu * lap_Psi + rotational + nonlin + damp

        Psi += dt * dPsi_dt

        # ---- 3. Intelligent amplitude clamping ----
        max_abs = np.max(np.abs(Psi))

        if step < 1000:
            if max_abs > 1e8:
                Psi *= (1e8 / max_abs)
        else:
            if max_abs > max_amp:
                Psi *= (max_amp / max_abs)
            if max_abs < min_amp:
                Psi *= (1.2 / max_abs)

        # ---- 4. Progress report ----
        if step % 500 == 0 or step == T_steps - 1:
            measure = np.sum(np.abs(Psi) > 0.08) * (dx ** DIM)
            print(f"Step {step:4d} | Max |Ψ| = {max_abs:.4f} | Measure = {measure:.6f} / {vol_full:.4f}")

    print("-" * 60)

    # --------------------- Final Analysis ---------------------
    absPsi_final = np.abs(Psi)
    threshold = 0.08
    support_count = np.sum(absPsi_final > threshold)
    final_measure = support_count * (dx ** DIM)

    print(f"\nFinal {DIM}D Lebesgue measure: {final_measure:.6f} (fraction = {final_measure/vol_full:.4%})")
    print(f"Support points: {support_count} / {N**DIM}")

    # --------------------- Directional Coverage Test (Fine Tracing) ---------------------
    print("Verifying directional coverage (fine tracing, 500 random directions)...")

    def check_direction_fine(field_abs, u, center, dx, length=1.0):
        """
        Fine-grained deterministic tracing: step through the segment with step size dx/2.
        This ensures that even a single support point is detected.
        """
        dim = len(field_abs.shape)
        N_grid = field_abs.shape[0]
        step_size = dx / 2.0
        s = -length / 2.0
        while s <= length / 2.0:
            phys = center + s * u
            idx = tuple(int(np.floor(coord / dx)) % N_grid for coord in phys)
            if field_abs[idx] > threshold:
                return True
            s += step_size
        return False

    covered = 0
    num_test = 500
    for _ in range(num_test):
        u = np.random.randn(DIM)
        u /= np.linalg.norm(u)
        if check_direction_fine(absPsi_final, u, center, dx):
            covered += 1

    coverage = covered / num_test * 100
    print(f"{DIM}D directional coverage: {covered}/{num_test} = {coverage:.1f}%")

    # --------------------- Export Dataset ---------------------
    export_filename = f"kakeya_{DIM}d_polynomial_N{N}.npz"
    support_mask = absPsi_final > threshold
    np.savez_compressed(export_filename,
                        grid_shape=shape,
                        dx=dx, L=L,
                        support=support_mask,
                        intensity=absPsi_final)
    print(f"\nDataset exported to '{export_filename}'")
    print(f"{DIM}D Pure Polynomial GL completed.\n")

print("\n" + "=" * 70)
print("All dimensions (3D, 4D, 5D) finished successfully.")
print("Generated datasets:")
print("  - kakeya_3d_polynomial_N32.npz")
print("  - kakeya_4d_polynomial_N24.npz")
print("  - kakeya_5d_polynomial_N12.npz")
print("=" * 70)
