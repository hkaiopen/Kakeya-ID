# Kakeya-ID: Numerical Construction of Kakeya Sets via Generalized Ginzburg–Landau Dynamics

This repository contains the code, datasets, and outputs for numerically constructing Kakeya-type sets in three, four, and five dimensions using a generalized Ginzburg–Landau (GL) equation. The work provides **the world's first publicly available four- and five-dimensional Kakeya-type datasets** with full directional coverage and extremely small Lebesgue measure.

---

## 1. What is a Kakeya set?

A **Kakeya set** is a region of space that contains a unit line segment in every direction, yet its total volume can be made arbitrarily small. This counter‑intuitive fact lies at the heart of deep problems in harmonic analysis, geometric measure theory, and the calculus of variations.

In this project, we generate such sets computationally. Instead of manually designing the complicated geometry, we let a partial differential equation do the work: the **generalized Ginzburg–Landau equation** drives an initial random collection of line segments to self‑organize into an extremely sparse structure that still covers all directions.

---

## 2. Key Results

| Dimension | Grid Size | Support Points | Measure Fraction | Coverage |
| :--- | :--- | :--- | :--- | :--- |
| 3D | 32×32×32 | 13 | ~0.04% | 100% |
| 4D | 24×24×24×24 | 9 | ~0.0027% | 100% |
| 5D | 16×16×16×16×16 | **1** | ~0.0001% | 100% |

The five‑dimensional result is the ultimate compressed state: a single grid point that, thanks to periodic boundary conditions and dense irrational orbits, still intersects a unit segment in every tested direction.

---

## 3. Repository Structure

```
Kakeya-ID/
├── README.md                     # This file
├── LICENSE                       # MIT License
│
├── code/                         # Source code
│   ├── kakeya_Nd_generation.py   # Dimension‑adaptive GL construction script
│   └── verify_kakeya.py          # Independent verification script
│
├── datasets/                     # Pre‑computed Kakeya sets
│   ├── README.md                 # Dataset description (plain language)
│   ├── kakeya_3d_N32_puregl.npz
│   ├── kakeya_4d_N24_puregl.npz
│   └── kakeya_5d_N16_puregl.npz
│
└── outputs/                      # Visualizations and logs
    ├── figures/                  # 3D projections and slices
    │   ├── README.md             # Explanation of the figures
    │   ├── 3D.png
    │   ├── 4D.png
    │   └── 5D.png
    └── logs/                     # Console outputs from example runs
        ├── 3d_output.txt
        ├── 4d_output.txt
        └── 5d_output.txt
```

## 4. Requirements

- Python 3.7+
- Required packages: `numpy`, `scipy`, `matplotlib`

Install them with:

```bash
pip install numpy scipy matplotlib
```

---

## 5. Usage

### Generate a Kakeya set

1. Open `code/kakeya_Nd_generation.py`.
2. Set the `DIM` variable to `3`, `4`, or `5` at the top of the file.
3. Run the script:

```bash
cd code
python kakeya_Nd_generation.py
```

The script will:
- Initialize the field with random directional segments.
- Evolve the generalized GL equation for several thousand steps.
- Print progress updates to the console.
- Save the resulting support set as an `.npz` file in the current directory.
- Display a 3D visualization.

### Verify a dataset

To independently check a generated `.npz` file:

```bash
python code/verify_kakeya.py path/to/dataset.npz
```

The verification script computes the discrete Lebesgue measure and tests directional coverage for 500 random directions. It also classifies the state as stable Kakeya phase, metastable, or uniform.

---

## 6. Interpreting the Outputs

- **`kakeya_*_N*_puregl.npz`**  
  Contains the grid shape, physical parameters, a Boolean `support` mask, and the field `intensity`.

- **`outputs/figures/`**  
  Since 4D and 5D data cannot be displayed directly, these images use maximum intensity projections and fixed slices to reduce the dimensionality to 3D. The `README.md` in that folder explains the visualization methods in detail.

- **`outputs/logs/`**  
  Example console outputs showing the evolution of the maximum field amplitude and the measure at each reporting step.

---

## 7. License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## 8. Citation

If you use this code or the datasets in your research, please cite the following:

**The associated research paper (preprint):**  
> Huang, K. & Liu, H. (2026). *Generalized Ginzburg–Landau Construction of Kakeya Sets: From Numerical Realization to Variational Proof*.
> https://doi.org/10.5281/zenodo.19542718

**The Kakeya dataset:**  
> Huang, K. (2026). *Kakeya-type sets in 3D, 4D, and 5D* [Data set]. https://github.com/hkaiopen/Kakeya-ID/datasets

**The software (this repository):**  
> Huang, K. (2026). *Kakeya-ID: Numerical construction of Kakeya sets via generalized Ginzburg–Landau dynamics* (Version v1.0) [Computer software]. GitHub. https://github.com/hkaiopen/Kakeya-ID

---

## 9. Contact

For questions or collaborations, please open an issue on GitHub or contact the authors directly.

*This work bridges information, geometry, and the calculus of variations. We welcome feedback and further exploration.*
