# Mathematical model

## Candidate and control

Candidate:

```text
∂C/∂t = ∂x(D(x)∂xC) - I_sink(x) Vmax C/(Km+C)
```

Control:

```text
∂C/∂t = ∂x(D(x)∂xC)
```

## Units

| Quantity | Unit |
|---|---|
| `x`, `L` | m |
| `t` | s |
| `C`, `Km` | mol m^-3 |
| `D` | m^2 s^-1 |
| `Vmax` | mol m^-3 s^-1 |

Both diffusion and reaction terms therefore have units `mol m^-3 s^-1`.

## Finite-volume flux

At face `i+1/2`:

```text
J[i+1/2] = -D_face (C[i+1]-C[i])/Δx
D_face = 2 D[i]D[i+1]/(D[i]+D[i+1])
```

For interior cells:

```text
dC[i]/dt = (J[i-1/2]-J[i+1/2])/Δx - R(C[i]).
```

Harmonic averaging is used to preserve flux continuity across discontinuous diffusivity.

## Boundary conditions

```text
J[-1/2] = 0
C(L,t) = C_source
```

## Estimand

```text
r = 1 - C_sink(x_interface,T)/C_control(x_interface,T)
```

`r` is dimensionless. It is only a model-relative concentration change.

## Release arithmetic

For first-order release:

```text
C(t)=C0 exp(-kt)
t_half=ln(2)/k
```

The legacy combined rate `k=1.6e-5 s^-1` gives `t_half≈12.0 h`, contradicting the former multi-year claim.

## Required numerical checks

- grid refinement;
- time/tolerance refinement;
- positivity;
- finite values;
- no-sink control;
- zero-sink identity;
- mass-balance residual;
- parameter uncertainty;
- reproducible random seed.

See `MODEL_LIMITATIONS.md` for interpretation limits.
