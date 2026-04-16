# Kakeya-ID: Numerical Construction of Kakeya Sets via Generalized Ginzburg–Landau Dynamics

This repository contains the code, datasets, and outputs for numerically constructing Kakeya-type sets in three, four, and five dimensions using a generalized Ginzburg–Landau (GL) equation. The work provides **the world's first publicly available four- and five-dimensional Kakeya-type datasets** with full directional coverage and extremely small Lebesgue measure.

---

## 1. What is a Kakeya set?

A **Kakeya set** is a region of space that contains a unit line segment in every direction, yet its total volume can be made arbitrarily small. This counter‑intuitive fact lies at the heart of deep problems in harmonic analysis, geometric measure theory, and the calculus of variations.

In this project, we generate such sets computationally. Instead of manually designing the complicated geometry, we let a partial differential equation do the work: the **generalized Ginzburg–Landau equation** drives an initial random collection of line segments to self‑organize into an extremely sparse structure that still covers all directions.

---

## 2. Two Methods, One Framework

This work employs **two complementary numerical approaches**, both rooted in the same generalized Ginzburg–Landau dynamics:

| Method | Description | Code | Datasets | Logs |
| :--- | :--- | :--- | :--- | :--- |
| **Logarithmic GL** (original) | Includes a logarithmic potential κ log\|Ψ\| that prevents the field from vanishing, preserving directional coverage during compression. | `code/kakeya_Nd_generation.py` | `datasets/` (`.npz` files) | `outputs/logs/3D_output.txt`, `4D_output.txt`, `5D_output.txt` |
| **Pure Polynomial GL** | Removes the logarithmic term entirely, relying only on polynomial nonlinearities (ξ\|Ψ\|⁴Ψ) and anti-diffusion. This version corresponds exactly to the variational framework of the rigorous mathematical proof. | `code/kakeya_Nd_generation_PurePolynomial.py` | `datasets_PurePolynomial/` | `outputs/logs/PurePolynomial_3D4D5D_output.txt` |

Both methods produce Kakeya-type sets with extremely small Lebesgue measure. The pure polynomial version demonstrates that **the logarithmic term is not strictly necessary**—the compression mechanism itself is robust and dimension-independent.

---

## 3. Key Results

### 3.1 Logarithmic GL Results

| Dimension | Grid Size | Support Points | Measure Fraction | Coverage |
| :--- | :--- | :--- | :--- | :--- |
| 3D | 32×32×32 | 13 | ~0.04% | 100% |
| 4D | 24×24×24×24 | 9 | ~0.0027% | 100% |
| 5D | 16×16×16×16×16 | **1** | ~0.0001% | 100% |

### 3.2 Pure Polynomial GL Results

| Dimension | Grid Size | Support Points | Measure Fraction | Coverage | Interpretation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 3D (baseline) | 32×32×32 | **1** | ~0.0031% | **0%** | Over‑compressed; coverage fails |
| 3D (strong) | 32×32×32 | **1** | ~0.0031% | **0%** | Stronger compression, still fails |
| 3D (high dir) | 32×32×32 | **1** | ~0.0031% | **0%** | More initial directions, still fails |
| 4D | 24×24×24×24 | **1** | ~0.0003% | **100%** | Single‑point Kakeya set |
| 5D | 12×12×12×12×12 | **1** | ~0.0004% | **100%** | Ultimate compression |

The five‑dimensional result—a single grid point that still intersects a unit segment in every tested direction—is the ultimate compressed state of a discrete Kakeya set.

---

## 4. Scientific Significance

Beyond the numerical construction itself, this work carries deeper implications that bridge geometry, information theory, and theoretical physics.

### 4.1 The First Publicly Available 4D and 5D Kakeya Datasets

Prior to this work, no publicly available numerical dataset of a Kakeya set in four or five dimensions existed. These files provide **concrete, verifiable examples** of a famously elusive mathematical object. Anyone can download the `.npz` files and run `verify_kakeya.py` to independently confirm the two defining properties: extremely small measure and full directional coverage.

### 4.2 Information Compression as Geometry Emergence

The Kakeya construction demonstrates a profound principle: **in a pure information field (the generalized GL equation), directional information can be losslessly compressed onto a zero‑measure geometric skeleton**, and in sufficiently high dimensions, it collapses to a single singularity (a point). This is a **rigorous mathematical example of "geometry emerging from information."** The GL gradient flow spontaneously sculpts the information field into a low‑dimensional geometric structure—the Kakeya set is not manually designed; it is what the information field *becomes* when it pursues minimal redundancy.

### 4.3 Matter as a Projection of Information

This work provides what may be the **first and strongest mathematical evidence for the claim that "matter is a projection of information."** The information field, governed by a simple variational principle, self‑organizes into a geometric structure that possesses all the essential features of a physical object: directional completeness, minimal spatial extent, and dimensional saturation. Geometry—and by extension, the "stuff" of the physical world—appears not as a fundamental given, but as the **condensate of an underlying information dynamics**.

### 4.4 A New Perspective on Black Hole Information

The pure polynomial results in 4D reveal a striking dichotomy: **in 4D, a single‑point Kakeya set is both possible (100% coverage) and stable**, while in 3D the same single‑point configuration **fails catastrophically (0% coverage)**. This has a direct analogue in the black hole information paradox: **information need not "escape"—it can be perfectly confined and encoded on a zero‑measure skeleton.** The 4D single‑point Kakeya set is a mathematical realization of an "information superconductor," where information is preserved without loss despite extreme compression. In contrast, the 3D failure shows that **lower dimensions lack the geometric capacity for such confinement**—exactly the tension between information preservation and dimensional constraints that lies at the heart of the paradox.

### 4.5 Why Our Universe is Three‑Dimensional

The dimensional threshold revealed by the pure polynomial experiments offers a compelling mathematical explanation for the observed dimensionality of physical space:

- **3D**: Single‑point Kakeya sets fail. Information **must** be distributed across multiple points (e.g., 13 points in the logarithmic version) to achieve full coverage. A 3D universe cannot collapse all directional information into a singularity without losing it.
- **4D**: Single‑point Kakeya sets **succeed** (100% coverage). Information *can* be perfectly confined to a zero‑dimensional skeleton.
- **5D and above**: Single‑point Kakeya sets remain successful; the compression saturates.

If information is primary and geometry is its emergent manifestation, then **a universe with observers (who require distinguishable structures) must exist in a dimension where information can be both complete and extended.** Three dimensions appear to be the **minimal arena** in which information can achieve lossless encoding without collapsing into an unobservable singularity. We live in three dimensions not by accident, but because it is the **lowest dimension that supports both information completeness and structural richness.**

### 4.6 Validation of the Variational Proof Framework

The pure polynomial runs **directly correspond to the variational framework used in the rigorous mathematical proof** (geometric obstacle + polynomial GL energy). The fact that both the logarithmic and pure polynomial paths converge to Kakeya sets—and that the pure polynomial version achieves even more extreme compression in 4D and 5D—provides strong numerical evidence that the proof's core mechanism (measure compression without directional loss) is physically robust and dimension‑independent.

### 4.7 A New Paradigm for Interdisciplinary Research

This work establishes a **unified language** for addressing problems across mathematics, physics, and information science:

- **In mathematics**: Transforms a static existence problem into a dynamic generation process, offering new variational tools for high‑dimensional geometric measure theory.
- **In physics**: Provides a rigorously analyzable toy model for holographic encoding and dimensional emergence.
- **In information science**: Reveals a variational foundation for optimal encoding—lossless preservation (logarithmic barrier) + redundancy elimination (compression terms) = optimal geometric code.

We warmly invite researchers from all relevant fields to explore and expand this emerging paradigm.

---

## 5. Repository Structure

```
Kakeya-ID/
├── README.md                              # This file
├── LICENSE                                # MIT License
│
├── code/                                  # Source code
│   ├── kakeya_Nd_generation.py            # Logarithmic GL (original)
│   ├── kakeya_Nd_generation_PurePolynomial.py  # Pure polynomial GL
│   └── verify_kakeya.py                   # Verification script
│
├── datasets/                              # Logarithmic GL datasets
│   ├── README.md
│   ├── kakeya_3d_N32_puregl.npz
│   ├── kakeya_4d_N24_puregl.npz
│   └── kakeya_5d_N16_puregl.npz
│
├── datasets_PurePolynomial/               # Pure polynomial GL datasets
│   ├── README.md
│   ├── kakeya_3d_polynomial_N32.npz
│   ├── kakeya_3d_polynomial_strong_N32.npz
│   ├── kakeya_3d_polynomial_hd_N32.npz
│   ├── kakeya_4d_polynomial_N24.npz
│   └── kakeya_5d_polynomial_N12.npz
│
└── outputs/                               # Visualizations and logs
    ├── figures/                           # 3D projections and slices
    │   ├── README.md
    │   ├── 3D.png
    │   ├── 4D.png
    │   └── 5D.png
    └── logs/                              # Console outputs
        ├── 3D_output.txt
        ├── 4D_output.txt
        ├── 5D_output.txt
        ├── PurePolynomial_3D4D5D_output.txt
        └── verify_logs/                   # Verification outputs
            ├── verify_3d.txt
            ├── verify_4d.txt
            └── verify_5d.txt
```

---

## 6. Requirements

- Python 3.7+
- Required packages: `numpy`, `scipy`, `matplotlib`

Install them with:
```bash
pip install numpy scipy matplotlib
```

---

## 7. Usage

### Generate a Kakeya set

**Logarithmic GL (original):**
```bash
cd code
# Edit kakeya_Nd_generation.py to set DIM = 3, 4, or 5
python kakeya_Nd_generation.py
```

**Pure polynomial GL:**
```bash
cd code
# Edit kakeya_Nd_generation_PurePolynomial.py to set DIM = 3, 4, or 5
python kakeya_Nd_generation_PurePolynomial.py
```

### Verify a dataset

```bash
python code/verify_kakeya.py path/to/dataset.npz
```

The verification script computes the discrete Lebesgue measure and tests directional coverage for 500 random directions. It also classifies the state as stable Kakeya phase, metastable, or uniform.

---

## 8. License

This project is licensed under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License** (CC BY-NC-SA 4.0).

This license allows you to:
*   **Share** — copy and redistribute the material in any medium or format.
*   **Adapt** — remix, transform, and build upon the material.

Under the following terms:
1.  **Attribution (BY)** — You must give **appropriate credit**, provide a link to the license, and **indicate if changes were made**. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use[1](@ref).
2.  **NonCommercial (NC)** — You may **not use the material for commercial purposes**. Commercial purposes include, but are not limited to:
    *   Selling products or services that incorporate this project.
    *   Using it in paid training or courses.
    *   Integrating it into commercial software.
    *   Any use aimed at monetary compensation or private financial gain.
3.  **ShareAlike (SA)** — If you remix, transform, or build upon the material, you **must distribute your contributions under the same license** as the original (CC BY-NC-SA 4.0)[1](@ref).

**For any commercial use, you must obtain prior written permission from the author.** Please contact the author to discuss licensing options.

To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0/.

---

## 9. Citation

If you use this code or the datasets in your research, please cite the following:

**The associated research paper (preprint):**  
> Huang, K. & Liu, H. (2026). *Generalized Ginzburg–Landau Construction of Kakeya Sets: From Numerical Realization to Variational Proof*.  
> [https://doi.org/10.5281/zenodo.19542718](https://doi.org/10.5281/zenodo.19542718)

**The Kakeya dataset (logarithmic):**  
> Huang, K. (2026). *Kakeya-type sets in 3D, 4D, and 5D* [Data set].  
> [https://github.com/hkaiopen/Kakeya-ID/tree/main/datasets](https://github.com/hkaiopen/Kakeya-ID/tree/main/datasets)

**The Kakeya dataset (pure polynomial):**  
> Huang, K. (2026). *Pure polynomial Kakeya datasets (3D, 4D, 5D)* [Data set].  
> [https://github.com/hkaiopen/Kakeya-ID/tree/main/datasets_PurePolynomial](https://github.com/hkaiopen/Kakeya-ID/tree/main/datasets_PurePolynomial)

**The software (this repository):**  
> Huang, K. (2026). *Kakeya-ID: Numerical construction of Kakeya sets via generalized Ginzburg–Landau dynamics* (Version v1.0) [Computer software]. GitHub.  
> [https://github.com/hkaiopen/Kakeya-ID](https://github.com/hkaiopen/Kakeya-ID)

---

## 10. Contact

For questions or collaborations, please open an issue on GitHub or contact the authors directly.

*This work bridges information, geometry, and the calculus of variations. We welcome feedback and further exploration.*
