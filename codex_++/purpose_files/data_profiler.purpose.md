# @codex-role: architect
# @codex-objective: generate or upgrade `.purpose.md` with:
# - output schema
# - coordination logic
# - integration points
# - ecosystem anchoring
# Follow AGENTS.md G-10 and Section 9 enrichment instructions.
- @ai-path: data_profiler
- @ai-source-files: [data_profiler.py]
- @ai-role: profiler
- @ai-intent: "Generate dataset and column level profiling information"
- @ai-version: 0.1.0
- @ai-generated: true
- @ai-verified: false
- @schema-version: 0.3
- @ai-risk-pii: medium
- @ai-risk-performance: medium
- @ai-risk-drift: "Interface may change as profiling logic evolves"
- @ai-used-by: pipeline,pipeline_transformed,main_pipeline,run_profiler
- @ai-downstream: reports,plots

# Module: data_profiler
> Provides a DataProfiler class to summarize datasets and produce Markdown reports.

---

### 🎯 Intent & Responsibility
- Normalise column types via a resolver that merges pandas inference with config overrides
- Profile dataset-level metadata, per-column statistics, and temporal behaviour
- Generate Markdown reports with linked visualisations for each column category
- Optionally orchestrate bivariate analysis through `data_pipeline.bivariate_profiler`
- Store results (including column types, plots, and optional pair metrics) for programmatic use

---

### 📥 Inputs & 📤 Outputs
| Direction | Name | Type | Description |
|-----------|------|------|-------------|
| 📥 In | dataframe | `pd.DataFrame` | dataset to profile |
| 📥 In | custom_types | `dict[str,str]` | optional column type hints |
| 📤 Out | results | `Dict[str,Any]` | metadata, column profiles, plot paths, optional bivariate metrics |
| 📤 Out | column_types | `Dict[str,Dict[str,str]]` | semantic/logical typing per column |
| 📤 Out | report | `str` | Markdown document saved to disk when generated |

---

### 🔗 Dependencies
- pandas, numpy, seaborn, matplotlib, missingno
- optional: phonenumbers (phone validation)
- internal: `data_pipeline.bivariate_profiler.BivariateProfiler` (lazy import)
- re-exports mirrored in `profiler.py` for legacy compatibility

---

### 🗣 Dialogic Notes
- Combines column profiling with optional bivariate analysis.
- Assumes small to medium data size; may require sampling for large datasets.

---

### 9 Pipeline Integration
#### Coordination Mechanics
- Pipelines supply datasets plus optional `custom_types`
- `profile_dataset` normalises types, runs column routing, and (optionally) triggers bivariate profiling
- `generate_report` materialises Markdown referencing artefacts in `output_dir/plots`

#### Integration Points
- Upstream: `pipeline.py`, `main_pipeline.py`, `data_pipeline/pipeline.py`
- Downstream: Markdown reports, plot images, and optional bivariate result bundles consumed by reporting tooling

#### Risks
- Profiling large datasets may exhaust memory
- Temporary files (plots) may accumulate

---

### 🧠 Tags
@ai-role: profiler
@ai-intent: data quality summary
@ai-cadence: drift-preferred
@ai-risk-recall: medium
@ai-semantic-scope: reports
@ai-coordination: analysis pipeline
