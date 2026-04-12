# Visualizations of Kakeya Sets in 3D, 4D, and 5D

This folder contains example figures generated from the Kakeya datasets. Because humans can only perceive three spatial dimensions, the 4D and 5D sets are shown using **projections** and **slices** that reduce the dimensionality to 3D.

## What do the images show?

### `3D.png`
**Direct 3D scatter plot of the three‑dimensional Kakeya set.**

This image shows the actual 3D Kakeya set generated on a $32\times32\times32$ grid. Each colored dot represents a grid point where the field amplitude exceeds the threshold, and the color indicates the intensity. The final support contains **13 points**, occupying only about $0.04\%$ of the total volume, yet every randomly tested direction still intersects the set.

### `4D.png`
**3D projection and slice of the four‑dimensional Kakeya set.**

The four‑dimensional data ($24\times24\times24\times24$ grid) cannot be displayed directly. This figure combines two views:
- **Left panel**: A 3D *maximum intensity projection* along the 4th dimension ($w$). This means we take the highest field amplitude across all $w$ values for each $(x,y,z)$ coordinate and display it as a 3D scatter. Points that appear indicate that at least somewhere along the $w$‑axis the field is strong.
- **Right panel**: A single 3D *slice* taken at the midpoint of the 4th dimension ($w = L/2 = 4.0$). This is a cross‑section showing the structure exactly at that central hyperplane.

The final 4D set contains only **9 support points** out of over 330,000 grid points, a measure fraction of $0.003\%$. The projection and slice reveal how the extremely sparse set extends through the extra dimension.

### `5D.png`
**3D projection of the five‑dimensional Kakeya set.**

The five‑dimensional data ($16\times16\times16\times16\times16$ grid) is collapsed twice to produce a 3D view:
- First, a maximum intensity projection is taken along the 5th dimension ($v$).
- Then, another maximum projection is taken along the 4th dimension ($w$).

The resulting 3D scatter plot shows where the field amplitude is strongest in the reduced $(x,y,z)$ coordinates. Because the 5D set contains **only 1 support point** in the entire grid of over one million points, the projection may appear extremely sparse or even empty. This is expected: the single point, together with its periodic images, still intersects every unit line segment in every direction. The near‑emptiness of the image is a visual confirmation of the ultimate compression achieved in five dimensions.

## Why does the 5D image look almost empty?

The 5D dataset contains exactly **one** support point. Under periodic boundary conditions, a single point is sufficient to satisfy the Kakeya property because lines with irrational slopes produce dense orbits that eventually hit the point (or one of its periodic copies). The 3D projection shows only the $(x,y,z)$ coordinates of this point after collapsing the extra dimensions, so very few points are visible.

## Reproducing the figures

Run the corresponding generation script setting the parameter DIM, and the visualization code at the end of the script will automatically produce similar figures. You can also load the `.npz` datasets with Python and create your own custom visualizations.

---

*For more details on the Kakeya sets themselves, see the `datasets/README.md` file.*
