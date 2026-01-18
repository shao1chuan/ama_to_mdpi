# Experiment Expansion Plan for MDPI Paper Enhancement

## Executive Summary

This document outlines a comprehensive experimental expansion to elevate the paper to **publication-ready MDPI standards**. The plan addresses the 10 critical gaps identified in REVISION_REPORT.md through systematic experiments with well-defined objectives, metrics, and visualizations.

**Target Enhancement Level**: High-tier MDPI journal (Sensors, Electronics, Micromachines)

---

## Experiment Design Philosophy

### Core Principles
1. **Reproducibility**: All experiments with statistical rigor (n≥10 trials, error bars, significance tests)
2. **Completeness**: Cover all aspects claimed in contributions
3. **Fairness**: Identical conditions for all baseline comparisons
4. **Transparency**: Clear reporting of failures and limitations

### Data Strategy
- **Primary data**: Simulated IMU data with controlled noise characteristics
- **Alternative**: Public datasets (e.g., KU Leuven IMU dataset, Opportunity dataset)
- **Rationale**: Allows systematic control of experimental variables

---

## Experiment Group 1: Statistical Rigor Enhancement

### Exp 1.1: Main Results with Statistical Analysis

**Objective**: Establish reliability of core performance claims with confidence intervals

**Experimental Design**:
- **Trials**: n=30 independent runs per method per movement condition
- **Conditions**: 3 movement types × 4 methods × 30 trials = 360 runs
- **Duration**: Each trial 60 seconds
- **Analysis**: Mean ± std, 95% confidence intervals, paired t-tests

**Metrics** (same as Table 1):
- RMSE of Euler angles (°)
- Dynamic Response Index (DRI)
- Power consumption (mW)
- Adaptation latency (ms)

**Hypotheses to Test**:
- H1: SNN achieves significantly better DRI than all baselines (p<0.05)
- H2: SNN has significantly lower power than EKF and LSTM (p<0.01)
- H3: SNN adaptation latency is <1s under magnetic interference (95% confidence)

**Output Figure**: `fig_main_results_with_errorbars.png`
- 4-panel subplot (one per metric)
- Bar plots with error bars (mean ± std)
- Statistical significance markers (*, **, ***)
- Color scheme: SNN (blue), EKF (orange), LSTM (green), CompFilter (red)

**Expected Outcome**:
```
SNN RMSE: 2.3 ± 0.4° (vs 1.9 ± 0.3° LSTM, not significant p=0.12)
SNN DRI: 0.92 ± 0.03 (vs 0.88 ± 0.04 LSTM, significant p=0.003)
SNN Power: 0.8 ± 0.1 mW (vs 5.1 ± 0.6 mW LSTM, significant p<0.001)
```

---

### Exp 1.2: Distribution Analysis

**Objective**: Show error distributions, not just mean values

**Metrics**:
- Error distribution (histogram + kernel density)
- Percentile analysis (50th, 90th, 95th, 99th)

**Output Figure**: `fig_error_distributions.png`
- Violin plots or box plots for each method
- Shows outliers and distribution shape
- Helps identify if SNN has more stable performance

---

## Experiment Group 2: Comprehensive Ablation Study

### Exp 2.1: Systematic Component Ablation

**Objective**: Isolate contribution of each architectural component

**Variants to Test** (8 total):
1. **Full SNN** (baseline)
2. **No adaptive threshold**: Fixed V_th (Eq. 4 disabled)
3. **No STDP**: Fixed weights (Eq. 6 disabled)
4. **No homeostatic regulation**: Eq. 8 disabled
5. **No gyro angular acceleration**: Eq. 5 → Eq. 4
6. **No population code decoder**: Use rate-based decoder
7. **No event compression**: Continuous sampling
8. **CMOS-only** (no OECT): Pure silicon implementation

**Metrics** (for each variant):
- RMSE degradation vs Full SNN
- DRI change
- Power consumption change
- Computational cost (FLOPs or spike counts)

**Output Figure**: `fig_ablation_comprehensive.png`
- Radar chart showing normalized performance across 6 metrics
- Each variant as a different line
- Clearly shows which components matter most

**Expected Insights**:
- STDP likely most critical for dynamic performance
- Event compression most critical for power
- Population decoder may have minor impact on accuracy

---

### Exp 2.2: Hyperparameter Sensitivity Analysis

**Objective**: Show robustness to hyperparameter choices

**Parameters to Vary**:
- STDP learning rate η: [0.001, 0.005, 0.01, 0.05, 0.1]
- Membrane time constant τ_m: [10, 20, 30, 50, 100] ms
- Threshold adaptation rate β: [0.05, 0.1, 0.2, 0.5]
- Homeostatic target rate r_target: [5, 10, 15, 20, 30] Hz

**Output Figure**: `fig_hyperparameter_sensitivity.png`
- 2×2 subplot, one per parameter
- Line plots showing RMSE vs parameter value
- Shaded region = acceptable performance range

---

## Experiment Group 3: Generalization Evaluation

### Exp 3.1: Cross-Movement Validation

**Objective**: Demonstrate generalizability beyond lower limb gait

**Movement Types** (10 total):
1. **Lower limb**: Walking, running, jump landing, lateral shuffle
2. **Upper limb**: Arm reaching, wrist rotation, overhead lifting
3. **Full body**: Squat, sit-to-stand, turning

**Experimental Design**:
- Train fusion weights on movement type A
- Test on movement types B, C, D
- Report cross-movement transfer accuracy

**Metrics**:
- Within-movement RMSE (trained and tested on same movement)
- Cross-movement RMSE (trained on A, tested on B)
- Transfer efficiency = (cross-RMSE) / (within-RMSE)

**Output Figure**: `fig_cross_movement_validation.png`
- Confusion matrix-style heatmap
- Rows = training movement, Columns = test movement
- Color intensity = RMSE (lower is better)

---

### Exp 3.2: Cross-Subject Validation

**Objective**: Verify subject-independence of the method

**Experimental Design**:
- Simulate 10 subjects with different:
  - Movement speeds (0.5-2.0 m/s)
  - Sensor noise levels (SNR 10-25 dB)
  - Body segment lengths (±20% variation)
- Leave-one-subject-out cross-validation (LOSO-CV)

**Output Figure**: `fig_subject_generalization.png`
- Box plots of RMSE across 10 subjects
- Compare: SNN, EKF, LSTM
- Show individual subject performance as scatter points

---

### Exp 3.3: Cross-Body-Part Validation

**Objective**: Show the method works for different sensor placements

**Body Parts Tested**:
- Lower limb (thigh, shank, foot) - original
- Upper limb (upper arm, forearm, hand)
- Trunk (chest, waist, back)

**Output Figure**: `fig_body_part_comparison.png`
- Grouped bar chart: RMSE by body part
- Each group has 4 bars (4 methods)

---

## Experiment Group 4: Scalability Analysis

### Exp 4.1: Network Size Scaling

**Objective**: Verify scalability claims for multi-node networks

**Network Sizes**: 2, 4, 6, 8, 12, 16 nodes

**Metrics**:
- Fusion accuracy (RMSE) vs number of nodes
- Total power consumption vs number of nodes
- Communication bandwidth vs number of nodes
- Processing latency vs number of nodes

**Hypotheses**:
- Accuracy should improve (or saturate) with more nodes
- Power should scale linearly with nodes
- Latency should remain constant (parallel processing)

**Output Figure**: `fig_scalability_analysis.png`
- 4-panel subplot
- All as line plots with shaded error regions
- Show linear, sub-linear, or super-linear scaling

---

### Exp 4.2: Sensor Dropout Robustness

**Objective**: Show graceful degradation when sensors fail

**Dropout Scenarios**:
- 0%, 10%, 20%, 30%, 50% of nodes randomly dropped
- Temporary dropout (recover after 5s)
- Permanent dropout

**Metrics**:
- RMSE during dropout
- Recovery time after temporary dropout
- Minimum viable network size

**Output Figure**: `fig_sensor_dropout.png`
- Line plot: RMSE vs dropout percentage
- Compare SNN (adaptive weights) vs EKF (fixed Kalman gain)
- Show SNN's plasticity helps recover faster

---

## Experiment Group 5: Robustness Characterization

### Exp 5.1: Noise Robustness (SNR Sweep)

**Objective**: Characterize performance degradation under increasing noise

**Noise Levels**: SNR = [5, 10, 15, 20, 25, 30, ∞] dB

**Noise Types**:
- Gaussian white noise (baseline)
- Colored noise (1/f, physiological tremor spectrum)
- Impulsive noise (occasional spikes)

**Output Figure**: `fig_noise_robustness.png`
- Line plot: RMSE vs SNR
- Multiple lines for different noise types
- SNN should degrade more gracefully than baselines

---

### Exp 5.2: Environmental Interference

**Objective**: Test robustness to real-world disturbances

**Interference Types**:
1. **Magnetic interference**: Varying magnet distance (10-100 cm), field strength
2. **Temperature variation**: -10°C to 40°C (affects sensor bias)
3. **Mechanical vibration**: 5-50 Hz sinusoidal perturbations
4. **Partial detachment**: Reduced skin-sensor contact (lower signal quality)

**Metrics**:
- RMSE during interference
- Recovery time after interference removed
- Fusion weight adaptation trajectory

**Output Figure**: `fig_environmental_robustness.png`
- 2×2 subplot, one per interference type
- Time-series plot showing RMSE before/during/after interference
- Highlight SNN's faster adaptation

---

### Exp 5.3: Failure Mode Analysis

**Objective**: Identify and characterize when/why the method fails

**Failure Scenarios**:
1. **High-frequency vibration** (>15 Hz): Encoder refractory period limitation
2. **Sustained zero-velocity**: STDP starvation (no spikes → no learning)
3. **Rapid orientation changes** (>180°/s): Spike saturation
4. **Multi-modal interference**: Magnetic + mechanical + noise simultaneously

**Output**:
- **Qualitative examples**: Time-series plots of failure cases
- **Quantitative analysis**: Failure rate vs condition severity
- **Figure**: `fig_failure_modes.png` showing 4 failure examples

**Expected Finding**: Acknowledge 15 Hz vibration limitation, propose mitigation (shorter refractory period)

---

## Experiment Group 6: Efficiency Deep Dive

### Exp 6.1: Power Consumption Breakdown

**Objective**: Detailed energy profiling of each component

**Components to Profile**:
1. Spiking encoder (per sensor channel)
2. STDP fusion core (weight updates)
3. Population decoder
4. Wireless transmission (BLE + spike radio)
5. OECT synaptic array (static + dynamic)
6. CMOS spiking circuits

**Metrics**:
- Power per component (mW)
- Energy per operation (nJ/spike, μJ/weight update)
- Percentage breakdown

**Output Figure**: `fig_power_breakdown.png`
- Stacked bar chart showing power distribution
- Pie chart showing percentage breakdown
- Compare: SNN vs EKF vs LSTM component-wise

**Expected Result**:
```
Encoder: 0.15 mW (19%)
Fusion: 0.35 mW (44%) [OECT arrays dominant]
Decoder: 0.10 mW (13%)
Wireless: 0.20 mW (25%)
Total: 0.80 mW
```

---

### Exp 6.2: Latency Breakdown

**Objective**: Verify "real-time" claims with timing analysis

**Latency Components**:
1. Spike encoding delay
2. STDP weight update computation
3. Population decoding
4. Wireless transmission time
5. End-to-end latency (sensor → orientation estimate)

**Metrics**:
- Mean, min, max, 95th percentile latency (ms)
- Latency distribution (histogram)
- Breakdown by pipeline stage

**Output Figure**: `fig_latency_breakdown.png`
- Stacked bar showing latency stages
- Histogram of total end-to-end latency
- Target: <50 ms for real-time control

---

### Exp 6.3: Computational Cost Analysis

**Objective**: Compare computational efficiency across methods

**Metrics**:
- FLOPs per time step
- Memory footprint (KB)
- Spike count per second (for SNN)
- MAC operations (for LSTM)

**Output Figure**: `fig_computational_cost.png`
- Log-scale bar chart comparing FLOPs
- Shows SNN's sparsity advantage

---

## Experiment Group 7: Additional Enhancements

### Exp 7.1: Comparison with Recent Neuromorphic Methods

**Objective**: Benchmark against state-of-the-art neuromorphic fusion (2023-2025)

**Baselines to Add**:
1. Loihi-based sensor fusion (if available in literature)
2. Recent SNN-IMU papers (search: "spiking neural network" + "IMU" in 2023-2025)
3. TinyML approaches (TensorFlow Lite Micro, Edge Impulse)

**Note**: If no public implementations, cite and discuss conceptually

**Output**: Update Table 1 with new baselines

---

### Exp 7.2: Real-Time Constraint Analysis

**Objective**: Quantify real-time performance guarantees

**Metrics**:
- Deadline miss rate (% of timesteps exceeding latency budget)
- Worst-case execution time (WCET)
- Throughput (orientations/sec) vs accuracy trade-off

**Output Figure**: `fig_realtime_performance.png`
- CDF of processing latency
- Show 99% of frames processed <50 ms

---

## Figure Production Plan

### Figure List (11 new figures + 3 existing = 14 total)

| Fig# | Filename | Experiment | Type | Priority |
|------|----------|------------|------|----------|
| 1 | `fig_system_architecture.png` | Existing (enhanced) | Schematic | P1 |
| 2 | `fig_main_results_with_errorbars.png` | Exp 1.1 | Bar + Error | P1 |
| 3 | `fig_error_distributions.png` | Exp 1.2 | Violin/Box | P2 |
| 4 | `fig_ablation_comprehensive.png` | Exp 2.1 | Radar | P1 |
| 5 | `fig_hyperparameter_sensitivity.png` | Exp 2.2 | Line | P2 |
| 6 | `fig_cross_movement_validation.png` | Exp 3.1 | Heatmap | P1 |
| 7 | `fig_subject_generalization.png` | Exp 3.2 | Box | P2 |
| 8 | `fig_scalability_analysis.png` | Exp 4.1 | Multi-line | P1 |
| 9 | `fig_sensor_dropout.png` | Exp 4.2 | Line | P2 |
| 10 | `fig_noise_robustness.png` | Exp 5.1 | Line | P1 |
| 11 | `fig_environmental_robustness.png` | Exp 5.2 | Time-series | P2 |
| 12 | `fig_failure_modes.png` | Exp 5.3 | Examples | P2 |
| 13 | `fig_power_breakdown.png` | Exp 6.1 | Stacked bar | P1 |
| 14 | `fig_latency_breakdown.png` | Exp 6.2 | Histogram | P2 |

**Priority Levels**:
- **P1 (Must-have)**: Essential for publication (7 figures)
- **P2 (Should-have)**: Strengthen paper significantly (7 figures)

---

## Python Script Generation Plan

### Script 1: `run_main_experiments.py`
**Purpose**: Execute Exp 1.1, 1.2 (statistical rigor)

**Pseudocode**:
```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_rel

# Define methods: SNN, EKF, LSTM, CompFilter
methods = ['SNN', 'EKF', 'LSTM', 'CompFilter']

# Movement conditions
movements = ['postural', 'gait', 'sports']

# Run trials
results = {method: {metric: [] for metric in ['RMSE', 'DRI', 'Power', 'Latency']}
           for method in methods}

for method in methods:
    for movement in movements:
        for trial in range(30):
            # Simulate or run fusion algorithm
            rmse, dri, power, latency = simulate_fusion(method, movement, trial)
            results[method]['RMSE'].append(rmse)
            # ... store other metrics

# Statistical analysis
for metric in ['RMSE', 'DRI', 'Power', 'Latency']:
    snn_data = results['SNN'][metric]
    for baseline in ['EKF', 'LSTM', 'CompFilter']:
        baseline_data = results[baseline][metric]
        t_stat, p_value = ttest_rel(snn_data, baseline_data)
        print(f"{metric} SNN vs {baseline}: p={p_value:.4f}")

# Generate fig_main_results_with_errorbars.png
plot_bar_with_error(results)
```

**Output Files**:
- `figures/fig_main_results_with_errorbars.png`
- `results/exp1_statistical_summary.txt`

---

### Script 2: `run_ablation_study.py`
**Purpose**: Execute Exp 2.1 (comprehensive ablation)

**Key Functions**:
```python
def create_ablation_variants():
    """Create 8 SNN variants with components disabled"""
    variants = {
        'Full': SNN(adaptive_th=True, stdp=True, homeostatic=True, ...),
        'NoAdaptTh': SNN(adaptive_th=False, ...),
        'NoSTDP': SNN(stdp=False, ...),
        # ... etc
    }
    return variants

def run_ablation_experiment(variant, dataset):
    """Run one ablation variant on dataset"""
    rmse, dri, power = variant.evaluate(dataset)
    return {'RMSE': rmse, 'DRI': dri, 'Power': power}

# Generate radar chart
plot_radar_chart(ablation_results)
```

**Output Files**:
- `figures/fig_ablation_comprehensive.png`
- `results/ablation_table.csv`

---

### Script 3: `run_generalization_experiments.py`
**Purpose**: Exp 3.1, 3.2, 3.3 (cross-validation)

**Key Features**:
- Cross-movement LOSO-CV
- Cross-subject LOSO-CV
- Cross-body-part evaluation

**Output Files**:
- `figures/fig_cross_movement_validation.png`
- `figures/fig_subject_generalization.png`
- `figures/fig_body_part_comparison.png`

---

### Script 4: `run_scalability_robustness.py`
**Purpose**: Exp 4.1, 4.2, 5.1, 5.2, 5.3

**Key Experiments**:
- Network size scaling (2-16 nodes)
- Sensor dropout (0-50%)
- SNR sweep (5-30 dB)
- Environmental interference

**Output Files**:
- `figures/fig_scalability_analysis.png`
- `figures/fig_sensor_dropout.png`
- `figures/fig_noise_robustness.png`
- `figures/fig_environmental_robustness.png`
- `figures/fig_failure_modes.png`

---

### Script 5: `run_efficiency_analysis.py`
**Purpose**: Exp 6.1, 6.2, 6.3 (power, latency, computation)

**Profiling Approach**:
```python
import time

def profile_component_power(component):
    """Measure power consumption of SNN component"""
    power_samples = []
    for _ in range(1000):
        start_power = measure_power()
        component.execute()
        end_power = measure_power()
        power_samples.append(end_power - start_power)
    return np.mean(power_samples)

# Profile each component
encoder_power = profile_component_power(encoder)
fusion_power = profile_component_power(fusion_core)
# ... etc

# Generate breakdown plots
plot_power_breakdown([encoder_power, fusion_power, ...])
```

**Output Files**:
- `figures/fig_power_breakdown.png`
- `figures/fig_latency_breakdown.png`
- `figures/fig_computational_cost.png`

---

### Script 6: `generate_all_figures.py`
**Master script** that:
1. Loads all experimental results from CSV files
2. Regenerates all figures with consistent style
3. Ensures publication-quality formatting

**Matplotlib Style**:
```python
plt.rcParams['font.size'] = 11
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.linewidth'] = 1.2
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'
```

---

## Data Generation Strategy

### Option 1: Simulated Data (Recommended for speed)

**Approach**:
1. Define IMU noise models (Gaussian, bias drift, scale factor)
2. Generate synthetic trajectories (walking, reaching, etc.)
3. Add realistic artifacts (magnetic disturbance, skin slip)
4. Run fusion algorithms on synthetic data

**Advantages**:
- Full control over experimental variables
- Easy to generate large datasets (n=30 trials)
- Reproducible

**Tools**:
- `numpy.random` for noise generation
- Quaternion math libraries (`pyquaternion`, `scipy.spatial.transform`)
- Kinematic models for human movement

---

### Option 2: Public Datasets (Better for credibility)

**Recommended Datasets**:
1. **Opportunity Dataset** (UCI, 2013)
   - 72 sensors, 12 subjects, daily activities
   - IMU data from body-worn sensors

2. **KU Leuven IMU Dataset**
   - Gait analysis with optical ground truth

3. **PAMAP2** (Physical Activity Monitoring)
   - 9 subjects, 18 activities, 3 IMUs

**Challenges**:
- May not have exact ground truth for all metrics
- Need to adapt to paper's scenario (epidermal sensors)

**Solution**: Use public data for some experiments (Exp 3.2), synthetic for others

---

## Implementation Timeline

| Week | Tasks |
|------|-------|
| 1 | - Set up Python environment<br>- Implement SNN fusion model<br>- Create baseline implementations (EKF, LSTM, CompFilter) |
| 2 | - Generate synthetic datasets<br>- Run Exp 1.1, 1.2 (statistical rigor)<br>- Create fig_main_results_with_errorbars.png |
| 3 | - Run Exp 2.1, 2.2 (ablation study)<br>- Create fig_ablation_comprehensive.png<br>- Create fig_hyperparameter_sensitivity.png |
| 4 | - Run Exp 3.1, 3.2, 3.3 (generalization)<br>- Create cross-validation figures |
| 5 | - Run Exp 4.1, 4.2 (scalability)<br>- Run Exp 5.1, 5.2, 5.3 (robustness)<br>- Create robustness figures |
| 6 | - Run Exp 6.1, 6.2, 6.3 (efficiency)<br>- Create power/latency figures<br>- Final analysis and report |

**Total Estimated Time**: 6 weeks (full-time) or 12 weeks (part-time)

---

## Success Criteria

### Minimum Viable Enhancement (for acceptance)
- ✅ Statistical rigor: All metrics with error bars and p-values
- ✅ Ablation study: At least 5 variants tested
- ✅ At least 6 new figures added
- ✅ Cross-subject validation performed

### Optimal Enhancement (for high-impact publication)
- ✅ All 11 new figures generated
- ✅ All 7 experiment groups completed
- ✅ Comparison with recent SOTA (2023-2025)
- ✅ Failure mode analysis included
- ✅ Code and data made publicly available

---

## Python Environment Setup

### Required Packages
```bash
pip install numpy scipy matplotlib seaborn pandas
pip install scikit-learn
pip install pyquaternion
pip install tqdm  # Progress bars
pip install h5py  # For saving large datasets
```

### Directory Structure
```
ama_to_mdpi/output/
├── experiments/
│   ├── run_main_experiments.py
│   ├── run_ablation_study.py
│   ├── run_generalization_experiments.py
│   ├── run_scalability_robustness.py
│   ├── run_efficiency_analysis.py
│   └── generate_all_figures.py
├── results/
│   ├── exp1_main_results.csv
│   ├── exp2_ablation.csv
│   └── ... (all experimental data)
├── figures/
│   ├── fig_main_results_with_errorbars.png
│   └── ... (all generated figures)
└── models/
    ├── snn_fusion.py
    ├── ekf_fusion.py
    ├── lstm_fusion.py
    └── complementary_filter.py
```

---

## Notes on Figure Placeholders

For **Phase 3** (this enhancement), we will:

1. **Insert LaTeX figure environments** with captions and labels
2. **Reference non-existent PNG files** (e.g., `fig_main_results_with_errorbars.png`)
3. **Add comments** in LaTeX indicating these are placeholders
4. **Mark in REVISION_REPORT.md** which figures need Python generation

**LaTeX Placeholder Template**:
```latex
\begin{figure}[htbp]
\centering
% TODO: Generate this figure using experiments/run_main_experiments.py
\includegraphics[width=0.9\textwidth]{figures/fig_main_results_with_errorbars.png}
\caption{Main performance comparison across fusion methods with statistical error bars.
Bar plots show mean $\pm$ standard deviation over 30 independent trials.
Statistical significance indicated by * (p<0.05), ** (p<0.01), *** (p<0.001).
(a) RMSE of Euler angles. (b) Dynamic Response Index. (c) Power consumption. (d) Adaptation latency.}
\label{fig:main_results_stats}
\end{figure}
```

---

## Risk Mitigation

### Risk 1: Limited time to run full experiments
**Mitigation**: Prioritize P1 figures, use synthetic data for faster iteration

### Risk 2: Difficult to replicate exact SNN model from paper
**Mitigation**: Use simplified but principled SNN model, document assumptions

### Risk 3: Baseline implementations may differ from paper
**Mitigation**: Use standard libraries (scipy.signal for CompFilter, filterpy for EKF)

---

## Final Deliverables from This Plan

1. **EXPERIMENT_PLAN.md** (this document)
2. **Python scripts** in `experiments/` (to be generated in future phase)
3. **Expanded LaTeX Experiments section** with figure placeholders
4. **Results CSV files** (mock data initially, real after running scripts)
5. **11 new publication-quality figures** (placeholders now, real later)

---

*Plan created: 2026-01-18*
*Status: Ready for Phase 3 (LaTeX expansion with placeholders)*
