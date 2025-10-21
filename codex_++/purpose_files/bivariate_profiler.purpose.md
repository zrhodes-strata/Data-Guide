# @codex-role: architect
# @codex-objective: generate or upgrade `.purpose.md` with:
# - output schema
# - coordination logic
# - integration points
# - ecosystem anchoring
# Follow AGENTS.md G-10 and Section 9 enrichment instructions.
- @ai-path: data_pipeline.bivariate_profiler
- @ai-source-files: [bivariate_profiler.py]
- @ai-role: analysis
- @ai-intent: "Explore relationships between pairs of variables"
- @ai-version: 0.1.0
- @ai-generated: true
- @ai-verified: false
- @schema-version: 0.3
- @ai-risk-pii: medium
- @ai-risk-performance: high
- @ai-risk-drift: "Uses heavy numeric libraries; performance may vary"
- @ai-used-by: pipeline_transformed
- @ai-downstream: bivariate_plots

# Module: bivariate_profiler
> Provides correlation matrices, clustering metrics, logistic regression and other bivariate analyses.

---

### 🎯 Intent & Responsibility
- Normalise column roles (numeric, categorical, temporal) using `TypeResolver`
- Produce correlation matrices, VIF scores, and statistical tests per column pair
- Auto-route visual generation for numeric–numeric, numeric–categorical, and categorical–categorical pairs
- Persist plots and metrics for downstream reporting and dashboarding

---

### 📥 Inputs & 📤 Outputs
| Direction | Name | Type | Description |
|-----------|------|------|-------------|
| 📥 In | dataframe | `pd.DataFrame` | dataset to analyze |
| 📥 In | custom_types | `dict[str,str]` | optional semantic overrides reused from DataProfiler |
| 📤 Out | results | `Dict[str,Any]` | correlation matrices, pairwise metrics, type metadata |
| 📤 Out | plots | `Dict[str,str]` | relative paths to saved PNG visualisations |

---

### 🔗 Dependencies
- pandas, numpy, seaborn, matplotlib
- scipy (stats, KDE), scikit-learn, statsmodels
- internal: `data_profiler.TypeResolver`

---

### 🗣 Dialogic Notes
- Contains advanced analytics; may require sample size reduction for speed
- Some functions may overlap with other profiling modules

---

### 9 Pipeline Integration
#### Coordination Mechanics
- Triggered from `DataProfiler.profile_bivariate` or pipeline stages after column profiling
- `profile()` returns structured metrics and plot paths keyed by column pairs

#### Integration Points
- Upstream: cleaned dataset from DataTransform / DataProfiler outputs
- Downstream: Markdown reports, analyst notebooks, interactive dashboards

#### Risks
- High memory usage when computing pairwise metrics on wide datasets

---

### 🧠 Tags
@ai-role: analysis
@ai-intent: bivariate statistics
@ai-cadence: drift-preferred
@ai-risk-recall: high
@ai-semantic-scope: analytics
@ai-coordination: offline
