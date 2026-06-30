# SynapShield: Mathematical Models & PDEs

## Table of Contents
1. [Governing Equations](#governing-equations)
2. [Shear-Thinning Hydrogel Rheology](#shear-thinning-hydrogel-rheology)
3. [Drug Release Kinetics](#drug-release-kinetics)
4. [Alpha-Synuclein Transport & Trapping](#alpha-synuclein-transport--trapping)
5. [Computational Implementation](#computational-implementation)
6. [Validation Metrics](#validation-metrics)

---

## Governing Equations

### 1. Mass Transport Equation (Modified Fick's Second Law)

The fundamental equation governing drug release and alpha-synuclein transport:

```
∂C/∂t = D·∇²C + S(x,t) - R(C)
```

Where:
- `C` = Concentration [mol/m³]
- `D` = Diffusion coefficient [m²/s]
- `∇²` = Laplacian operator (spatial diffusion)
- `S(x,t)` = Source term (drug release from hydrogel)
- `R(C)` = Sink term (drug clearance / protein trapping)

---

## Shear-Thinning Hydrogel Rheology

### Herschel-Bulkley Fluid Model

The hydrogel must flow easily during injection (high shear) but solidify instantly in tissue (zero shear).

**Equation:**
```
τ = τ₀ + K·γ̇ⁿ
```

**Parameters:**
- `τ` = Shear stress [Pa]
- `τ₀` = Yield stress [Pa] (gel holds shape when τ < τ₀)
- `K` = Consistency index [Pa·sⁿ]
- `γ̇` = Shear rate [s⁻¹]
- `n` = Flow behavior index (**n < 1** for shear-thinning)

**Injection Criteria:**
```
If τ > τ₀ → Hydrogel flows like liquid (needle injection)
If τ < τ₀ → Hydrogel solidifies (tissue residence)
```

**Computational Implementation:**
```python
def herschel_bulkley_shear_rate(tau, tau_0, K, n):
    if tau < tau_0:
        return 0  # Solid phase
    else:
        return ((tau - tau_0) / K)**(1/n)  # Liquid phase
```

---

## Drug Release Kinetics

### 1. First-Order Cleavage (Short-Term)

For rapid initial release (days to weeks):

```
dCbound/dt = -kcleave·Cbound
```

**Solution:**
```
Cbound(t) = C₀·e^(-kcleave·t)
```

**Problem:** This depletes the drug reservoir in days, not 15 years.

---

### 2. Zero-Order Degradation (Long-Term)

To achieve 10-15 year release, we use **matrix erosion kinetics**:

```
dCbound/dt = -kerosion·(Cbound)ⁿ
```

Where `n < 1` (dispersive release) or coupling to hydrogel mass loss:

```
dM/dt = -kd·A(t)·Cwater
```

**Parameters:**
- `kd` = Degradation rate constant [s⁻¹]
- `A(t)` = Surface area of hydrogel at time t [m²]
- `Cwater` = Local interstitial fluid concentration [mol/m³]

**Target:** `kd ≈ 10⁻¹⁵ s⁻¹` (extremely slow degradation)

---

### 3. Host-Guest Caging (β-Cyclodextrin)

Drugs are trapped inside β-cyclodextrin "cages" via non-covalent interactions.

**Equilibrium:**
```
Drug_free + β-CD ⇌ Drug·β-CD_complex
```

**Dissociation constant:**
```
Kd = [Drug_free][β-CD] / [Complex]
```

**Release rate:**
```
d[Drug_free]/dt = koff·[Complex] - kon·[Drug_free][β-CD]
```

Where:
- `koff` = Dissociation rate [s⁻¹]
- `kon` = Association rate [s⁻¹]

---

## Alpha-Synuclein Transport & Trapping

### 1. Diffusion Equation with Sink Term

Alpha-synuclein moves from tissue (x = L) toward hydrogel (x = 0):

```
∂C₄/∂t = D₄·∇²C₄ - Rsink(C₄)
```

**Boundary Conditions:**
- **Left (x = 0):** `C₄ = 0` (infinite sink, perfect trapping)
- **Right (x = L):** `C₄ = C₄,influx` (constant shedding from EECs)

---

### 2. Michaelis-Menten Sink (Gel Trapping)

The hydrogel acts as a "chemical sink" for alpha-synuclein:

```
Rsink(C₄) = (Vmax·C₄) / (Km + C₄)
```

**Parameters:**
- `Vmax` = Maximum trapping rate [mol/(m³·s)]
- `Km` = Michaelis constant (affinity) [mol/m³]
- **Low `Km`** = High affinity (traps even trace amounts)

**Interpretation:**
- If `C₄ << Km`: `Rsink ≈ (Vmax/Km)·C₄` (linear trapping)
- If `C₄ >> Km`: `Rsink ≈ Vmax` (saturation)

---

### 3. Pharmacodynamic Clearance (Drug Boosts Clearance)

Antioxidants (caffeine/CGA) and NSAIDs (ibuprofen) enhance alpha-synuclein clearance:

```
Rclearance = kclear·(C₁ + C₂)·C₄
```

Where:
- `C₁` = Caffeine concentration
- `C₂` = Ibuprofen concentration
- `kclear` = Clearance rate constant [m³/(mol·s)]

**Full Alpha-Synuclein PDE:**
```
∂C₄/∂t = D₄·∇²C₄ - (Vmax·C₄)/(Km + C₄) - kclear·(C₁ + C₂)·C₄
```

---

## Computational Implementation

### 1. Spatial Discretization (Finite Differences)

```
∂²C/∂x² ≈ (C[i+1] - 2C[i] + C[i-1]) / Δx²
```

**Grid:**
- `Nx = 200` points
- `Δx = L / (Nx - 1) = 10 μm`

---

### 2. Time Integration (Method of Lines)

Convert PDEs to ODEs using spatial discretization, then solve with `scipy.integrate.solve_ivp`:

```python
def synapshield_odes(t, U):
    # U = [C1, C2, C3, C4] flattened
    # Compute dU/dt using finite differences
    dUdt = ...  # See simulations/python/synapshield_pde_solver.py
    return dUdt

sol = solve_ivp(synapshield_odes, t_span, U0, method='BDF')
```

---

### 3. Boundary Conditions (Ghost Points)

**Zero-flux (left boundary):**
```
dC/dx|ₓ₌₀ = 0 → C[0] = C[1]
```

**Sink (right boundary, drug washout):**
```
C[Nx-1] = 0  (drugs enter bloodstream, cleared)
```

**Constant influx (right boundary, alpha-synuclein):**
```
D₄·dC₄/dx|ₓ₌ₗ = -J_influx  (particles entering)
```

---

## Validation Metrics

### 1. Alpha-Synuclein Reduction at Vagus Nerve

**Primary metric:** Concentration at `x = L_gel` (nerve boundary)

```
Reduction = (C₄,initial - C₄,final) / C₄,initial × 100%
```

**Success criteria:** `Reduction > 90%`

---

### 2. Drug Release Duration

**Metric:** Time until `C₃ < 0.01·C₃,initial` (99% depleted)

**Target:** `t_depletion > 10 years (3.15×10⁸ seconds)`

---

### 3. Tissue Penetration Depth

**Metric:** Distance drugs diffuse into tissue (`C₁ > 0.1·C₁,max`)

**Target:** Penetration `> 0.5 mm` (reaches vagus nerve terminals)

---

## Dimensional Analysis

### Key Dimensionless Numbers

1. **Peclet Number (Pe):**
   ```
   Pe = v·L / D
   ```
   - `v` = Convective velocity [m/s] (peristalsis-induced)
   - `L` = Characteristic length [m]
   - `D` = Diffusion coefficient [m²/s]
   
   **Interpretation:** `Pe >> 1` → Convection dominates; `Pe << 1` → Diffusion dominates

2. **Damköhler Number (Da):**
   ```
   Da = kcleave·L² / D
   ```
   **Interpretation:** `Da >> 1` → Reaction (cleavage) fast; `Da << 1` → Diffusion fast

---

## Analytical Solutions (Simplified Cases)

### 1. Steady-State Drug Release (1D)

Assuming `∂C/∂t = 0` and constant `D`:

```
D·d²C/dx² + kcleave·C₃ = 0
```

**Solution:**
```
C₁(x) = A·sinh(λx) + B·cosh(λx)
```
Where `λ = sqrt(kcleave/D)`

---

### 2. Instantaneous Sink (Alpha-Synuclein)

If `Vmax → ∞` (perfect trapping), then `C₄(x) = 0` for all `x ≤ L_gel`.

**Problem reduces to:** Diffusion from boundary at `x = L_gel`

```
C₄(x) = C₄,influx · (x - L_gel) / (L - L_gel)  for x > L_gel
```

---

## References

1. **Braak's Hypothesis:** Alpha-synuclein pathology starts in gut, ascends vagus nerve.
2. **Herschel-Bulkley Model:** Rheology of shear-thinning biomaterials.
3. **Michaelis-Menten Kinetics:** Enzyme-substrate / sink-trapping models.
4. **Fick's Laws:** Diffusion-controlled drug release.

---

## Next Steps

- [ ] Validate 4-species model against in vitro data
- [ ] Optimize `kcleave` and `Km` for 15-year release
- [ ] Add mechanical coupling (hydrogel deformation during peristalsis)
- [ ] Scale up to 3D geometry (full duodenum cross-section)

---

**"From PDEs to Richard's tablet."** 🧠💙
