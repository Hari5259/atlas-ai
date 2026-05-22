# Mathematics Knowledge Base

Structured reference data for Atlas AI covering core mathematics topics. Each topic file follows `schema.json` and can be loaded offline without cloud APIs.

## Topics

| File | Domain |
|------|--------|
| `topics/algebra.json` | Equations, polynomials, factoring |
| `topics/geometry.json` | Shapes, area, volume, theorems |
| `topics/calculus.json` | Limits, derivatives, integrals |
| `topics/trigonometry.json` | Ratios, identities, unit circle |
| `topics/statistics.json` | Descriptive stats, probability |
| `topics/linear_algebra.json` | Vectors, matrices, determinants |

## Usage

```bash
cd backend
python -m knowledge.math.seed_math_kb   # Load into ChromaDB (requires Ollama)
python -m knowledge.math.math_kb search "quadratic formula"
```

## Entry Format

Each entry includes: `id`, `topic`, `title`, `content`, `formula` (optional), `keywords`, `difficulty`.
