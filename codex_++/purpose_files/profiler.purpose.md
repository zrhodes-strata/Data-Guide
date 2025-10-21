# @codex-role: architect
# @codex-objective: generate or upgrade `.purpose.md` with:
# - output schema
# - coordination logic
# - integration points
# - ecosystem anchoring
# Follow AGENTS.md G-10 and Section 9 enrichment instructions.
- @ai-path: profiler
- @ai-source-files: [profiler.py]
- @ai-role: profiler
- @ai-intent: "Generate plots and advanced profiling for datasets"
- @ai-version: 0.1.0
- @ai-generated: true
- @ai-verified: false
- @schema-version: 0.3
- @ai-risk-pii: medium
- @ai-risk-performance: medium
- @ai-risk-drift: "Large file with experimental features"
- @ai-used-by: data_profiler,pipeline
- @ai-downstream: plots,markdown_reports

# Module: profiler
> Provides a compatibility shim that re-exports the profiling toolkit implemented in `data_profiler`.

---

### 🎯 Intent & Responsibility
- Maintain backwards-compatible imports for legacy modules referencing `profiler.DataProfiler`
- Delegate all profiling behaviours to `data_profiler` without duplicating logic
- Surface the same public API (`DataProfiler`, `NumericProfiler`, etc.) for downstream callers

---

### 📥 Inputs & 📤 Outputs
| Direction | Name | Type | Description |
|-----------|------|------|-------------|
| 📥 In | *delegated* | — | All inputs forwarded to `data_profiler` exports |
| 📤 Out | *delegated* | — | Outputs identical to `data_profiler` symbols |

---

### 🔗 Dependencies
- internal: `data_profiler`

---

### 🗣 Dialogic Notes
- Module kept for import stability; implementation resides in `data_profiler`
- Future refactors may deprecate this shim once call sites migrate

---

### 9 Pipeline Integration
#### Coordination Mechanics
- Acts as thin wrapper; pipelines should import `DataProfiler` from `data_profiler`
- Existing scripts importing `profiler` continue to operate without code changes

#### Integration Points
- Upstream/Downstream identical to `data_profiler` due to re-exported API

#### Risks
- Mirrors `data_profiler` risks (plot generation cost, file naming collisions)

---

### 🧠 Tags
@ai-role: profiler
@ai-intent: visualization helper
@ai-cadence: drift-preferred
@ai-risk-recall: medium
@ai-semantic-scope: plots
@ai-coordination: analysis pipeline
