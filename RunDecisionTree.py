import DecisionTree2
import numpy as np
import math
import deampy.econ_eval as econ

SE_DRUG_VAX_RR = (np.log(0.76) - np.log(0.30)) / 2 * 1.96
SE_DRUG_UNVAX_RR = (np.log(0.83) - np.log(0.01)) / 2 * 1.96
SE_PAX_VAX_RR = (np.log(0.81) - np.log(0.44)) / 2 * 1.96
SE_PAX_UNVAX_RR = (np.log(0.49) - np.log(0.15)) / 2 * 1.96
mean = math.pow(24826, 2) / math.pow((25858 - 23795 / 2 * 1.96), 2)
variance = math.pow((25858 - 23795 / 2 * 1.96), 2) / 24826
# PSA
cost_0 = []
cost_1 = []
cost_2 = []
cost_3 = []
cost_4 = []
eff_0 = []
eff_1 = []
eff_2 = []
eff_3 = []
eff_4 = []

for i in range(10000):
    np.random.seed(i)
    rng_hosp_cost = np.random.gamma(mean, variance)

    # rng_drug_vax_rr = np.random.normal(np.log(0.49), SE_DRUG_VAX_RR)
    rng_drug_vax_rr = np.random.uniform(0.245, 0.735)
    drug_vax_rr = math.exp(rng_drug_vax_rr)

    # rng_pax_vax_rr = np.random.normal(np.log(0.17), SE_PAX_VAX_RR)
    rng_pax_vax_rr = np.random.uniform(0.085, 0.255)
    pax_vax_rr = math.exp(rng_pax_vax_rr)

    # rng_pax_unvax_rr = np.random.normal(np.log(0.60), SE_PAX_UNVAX_RR)
    rng_pax_unvax_rr = np.random.uniform(0.30, 0.90)
    pax_unvax_rr = math.exp(rng_pax_unvax_rr)

    # rng_drug_unvax_rr = np.random.normal(np.log(0.11), SE_DRUG_UNVAX_RR)
    rng_drug_unvax_rr = np.random.uniform(0.055, 0.165)
    drug_unvax_rr = math.exp(rng_drug_unvax_rr)
    result = DecisionTree2.simulate_decision_tree(hosp_cost=rng_hosp_cost, rr_pax_unvax=pax_unvax_rr, rr_pax_vax=pax_vax_rr, relative_risk_unvax=drug_unvax_rr, relative_risk_vax=drug_vax_rr)

    cost_0.append(result[0])
    cost_1.append(result[1])
    cost_2.append(result[2])
    cost_3.append(result[3])
    cost_4.append(result[4])
    eff_0.append(result[5])
    eff_1.append(result[6])
    eff_2.append(result[7])
    eff_3.append(result[8])
    eff_4.append(result[9])

mean_cost_0 = sum(cost_0)/len(cost_0)
mean_cost_1 = sum(cost_1)/len(cost_1)
mean_cost_2 = sum(cost_2)/len(cost_2)
mean_cost_3 = sum(cost_3)/len(cost_3)
mean_cost_4 = sum(cost_4)/len(cost_4)
mean_eff_0 = sum(eff_0)/len(eff_0)
mean_eff_1 = sum(eff_1)/len(eff_1)
mean_eff_2 = sum(eff_2)/len(eff_2)
mean_eff_3 = sum(eff_3)/len(eff_3)
mean_eff_4 = sum(eff_4)/len(eff_4)

ICER_1 = (mean_cost_1 - mean_cost_0) / (mean_eff_1 - mean_eff_0)
ICER_2 = (mean_cost_2 - mean_cost_0) / (mean_eff_2 - mean_eff_0)
ICER_3 = (mean_cost_3 - mean_cost_0) / (mean_eff_3 - mean_eff_0)
ICER_4 = (mean_cost_4 - mean_cost_0) / (mean_eff_4 - mean_eff_0)

print(ICER_1)
print(ICER_2)
print(ICER_3)
print(ICER_4)

# define five strategies
baseline = econ.Strategy(
    name='Baseline',
    cost_obs=cost_0,
    effect_obs=eff_0,
    color='green'
)
high_unvax = econ.Strategy(
    name='High Risk and Unvax',
    cost_obs=cost_1,
    effect_obs=eff_1,
    color='blue'
)
high_all = econ.Strategy(
    name='High Risk',
    cost_obs=cost_2,
    effect_obs=eff_2,
    color='orange'
)
high_low_unvax = econ.Strategy(
    name='High Risk and Low Risk Unvax',
    cost_obs=cost_3,
    effect_obs=eff_3,
    color='red'
)

everyone = econ.Strategy(
    name='Everyone',
    cost_obs=cost_4,
    effect_obs=eff_4,
    color='yellow'
)

# do CEA
# (the first strategy in the list of strategies is assumed to be the 'Base' strategy)
CEA = econ.CEA(
    strategies=[baseline, high_unvax, high_all, high_low_unvax, everyone],
    if_paired=False
)

# plot cost-effectiveness figure
CEA.plot_CE_plane(
    title='Cost-Effectiveness Analysis',
    x_label='Additional Effect (Hospitalizations Averted)',
    y_label='Additional Cost ($)',
    interval_type='c',  # to show confidence intervals for cost and effect of each strategy
    file_name='cost_effectiveness.png'
)

# report the CE table
CEA.build_CE_table(
    interval_type='c',
    alpha=0.05,
    cost_digits=2,
    effect_digits=3,
    icer_digits=3,
    file_name='CETable.csv')