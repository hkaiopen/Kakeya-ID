"""
Dimension-Adaptive Stable Kakeya Set Generation via Pure GL Dynamics
=====================================================================
Generates low-measure, full-directional-coverage Kakeya-type sets in 3D, 4D, or 5D
using a pure Ginzburg--Landau (gradient flow) equation.

Usage:
    Set DIM = 3, 4, or 5.
    Run the script. Results are saved as .npz files and visualized.

Author: Kai Huang
Date:   2026-04-12
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fftn, ifftn
from mpl_toolkits.mplot3d import Axes3D

# ====================== USER CONFIGURATION ======================
DIM = 3          # Choose 3, 4, or 5(takes more time)
# =================================================================

# --------------------- Dimension-Dependent Stable Presets (Pure GL) ---------------------
if DIM == 3:
    N = 32
    L = 10.0
    T_steps = 2500
    dt = 0.0002

    kappa = 0.15
    mu = 0.35
    gamma = 0.8
    Psi0 = 0.2
    damping = 0.005
    xi = 0.06

    num_directions = 400
    line_length = 3.5
    init_amp = 1.8 + 0.4j
    max_amp = 8.0
    min_amp = 0.5

elif DIM == 4:
    N = 24
    L = 8.0
    T_steps = 3000
    dt = 0.00015

    kappa = 0.18
    mu = 0.25
    gamma = 1.2
    Psi0 = 0.2
    damping = 0.003
    xi = 0.12

    num_directions = 500
    line_length = 3.5
    init_amp = 2.0 + 0.5j
    max_amp = 10.0
    min_amp = 0.5

elif DIM == 5:
    N = 16
    L = 4.0
    T_steps = 4000
    dt = 0.00005

    kappa = 0.3
    mu = 0.15
    gamma = 2.0
    Psi0 = 0.2
    damping = 0.001
    xi = 0.25

    num_directions = 600
    line_length = 2.5
    init_amp = 2.5 + 0.6j
    max_amp = 15.0
    min_amp = 0.5

else:
    raise ValueError("DIM must be 3, 4, or 5")

dx = L / N
shape = tuple([N] * DIM)

# --------------------- Build n-D Frequency Mesh ---------------------
print(f"Building {DIM}D frequency mesh...")
x = np.linspace(0, L, N, endpoint=False)
k = 2 * np.pi * np.fft.fftfreq(N, d=dx)

if DIM == 3:
    KX, KY, KZ = np.meshgrid(k, k, k, indexing='ij')
    K2 = KX**2 + KY**2 + KZ**2 + 1e-8
elif DIM == 4:
    KX, KY, KZ, KW = np.meshgrid(k, k, k, k, indexing='ij')
    K2 = KX**2 + KY**2 + KZ**2 + KW**2 + 1e-8
elif DIM == 5:
    K1, K2_, K3, K4, K5 = np.meshgrid(k, k, k, k, k, indexing='ij')
    K2 = K1**2 + K2_**2 + K3**2 + K4**2 + K5**2 + 1e-8

def laplacian(field):
    hat = fftn(field)
    return ifftn(-K2 * hat)

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

print(f"Starting {DIM}D Kakeya set evolution (pure GL)...")
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

    # ---- 2. Compute GL terms ----
    log_term = kappa * np.log(absPsi_clipped / Psi0 + 1e-8)
    lap_Psi = laplacian(Psi)
    rotational = -gamma * lap_Psi
    nonlin = xi * (absPsi_clipped**4) * Psi
    damp = -damping * Psi

    dPsi_dt = log_term + mu * lap_Psi + rotational + nonlin + damp

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
        vol_full = L ** DIM
        print(f"Step {step:4d} | Max |Ψ| = {max_abs:.4f} | Measure = {measure:.4f} / {vol_full:.4f}")

print("-" * 60)

# --------------------- Final Analysis ---------------------
absPsi_final = np.abs(Psi)
threshold = 0.08
support_count = np.sum(absPsi_final > threshold)
final_measure = support_count * (dx ** DIM)
vol_full = L ** DIM

print(f"\nFinal {DIM}D Lebesgue measure: {final_measure:.4f} (fraction = {final_measure/vol_full:.4%})")
print(f"Support points: {support_count} / {N**DIM}")
print(f"Expected Hausdorff dimension = {DIM}")

# Directional coverage test
covered = 0
num_test = 50
for _ in range(num_test):
    u = np.random.randn(DIM)
    u /= np.linalg.norm(u)
    line_sum = 0.0
    for ss in np.linspace(-1.2, 1.2, 15):
        idx = tuple(int(center + ss * u[d] / dx) % N for d in range(DIM))
        line_sum += absPsi_final[idx]
    if line_sum > 0.25:
        covered += 1
coverage = covered / num_test * 100
print(f"{DIM}D directional coverage: {covered}/{num_test} = {coverage:.1f}%")

# --------------------- Export Dataset ---------------------
export_filename = f"kakeya_{DIM}d_N{N}_puregl.npz"
support_mask = absPsi_final > threshold
np.savez_compressed(export_filename,
                    grid_shape=shape,
                    dx=dx, L=L,
                    support=support_mask,
                    intensity=absPsi_final)
print(f"\nDataset exported to '{export_filename}'")

# --------------------- Visualization (3D Projection) ---------------------
fig = plt.figure(figsize=(14, 6))

if DIM == 3:
    proj = absPsi_final
elif DIM == 4:
    proj = np.max(absPsi_final, axis=3)
elif DIM == 5:
    proj = np.max(np.max(absPsi_final, axis=4), axis=3)

ax1 = fig.add_subplot(121, projection='3d')
mask = proj > threshold
if np.any(mask):
    xs, ys, zs = np.where(mask)
    sc = ax1.scatter(xs*dx, ys*dx, zs*dx, c=proj[mask], cmap='plasma', s=3, alpha=0.7)
    plt.colorbar(sc, ax=ax1, label='|Ψ| projection')
ax1.set_title(f'{DIM}D Kakeya Set — 3D Projection\nMeasure fraction: {final_measure/vol_full:.3%}')
ax1.set_xlabel('x'); ax1.set_ylabel('y'); ax1.set_zlabel('z')

if DIM == 3:
    slice_data = absPsi_final[N//2, :, :]
    ax2 = fig.add_subplot(122)
    im = ax2.imshow(slice_data, cmap='viridis', origin='lower', extent=[0, L, 0, L])
    ax2.set_title(f'Slice z = {L/2:.2f}')
    plt.colorbar(im, ax=ax2)
else:
    ax2 = fig.add_subplot(122, projection='3d')
    if DIM == 4:
        slice_data = absPsi_final[:, :, :, N//2]
        title = f'Slice w = {L/2:.2f}'
    else:  # DIM == 5
        slice_data = absPsi_final[:, :, :, N//2, N//2]
        title = f'Slice w = {L/2:.2f}, v = {L/2:.2f}'
    mask2 = slice_data > threshold
    if np.any(mask2):
        xs2, ys2, zs2 = np.where(mask2)
        sc2 = ax2.scatter(xs2*dx, ys2*dx, zs2*dx, c=slice_data[mask2], cmap='viridis', s=3, alpha=0.7)
        plt.colorbar(sc2, ax=ax2)
    ax2.set_title(title)
    ax2.set_xlabel('x'); ax2.set_ylabel('y'); ax2.set_zlabel('z')

plt.tight_layout()
plt.show()
