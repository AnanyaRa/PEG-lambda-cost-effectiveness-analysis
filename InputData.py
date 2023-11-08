# MODEL PARAMETERS #
HR = 0.37  # Proportion high risk for severe COVID-19 disease, US
HR_65 = 0.55  # Proportion of those high risk for severe COVID-19 disease who are over 65
HR_65_COMORB = 0.76  # Proportion of those over 65 who also have at least 1 comorbidity leading to increased risk for severe COVID-19 disease

HOSP_COMORB_65 = 0.110  # Probability of COVID hospitalization for those with at least 1 comorbidity, over 65
HOSP_COMORB_UNDER65 = 0.016  # Probability of COVID hospitalization for those with at least 1 comorbidity, under 65
HOSP_NOCOMORB_65 = 0.042  # Probability of COVID hospitalization for those with no comorbidities, over 65
HOSP_NOCOMORB_UNDER65 = 0.008  # Probability of COVID hospitalization for those with no comorbidities, under 65

VAX_UNDER_65 = 0.7  # US vaccinated percentage, over 65
VAX_OVER_65 = 0.9  # US vaccinated percentage, under 65
VAX_HOSP_MULT = 0.25  # Vaccination hospitalization multiplier

DRUG_RR_VAX_OR_LR = 0.49  # Relative risk of PEG-lambda for hospitalization if vaccinated
DRUG_RR_UNVAX_HR = 0.11  # Relative risk of PEG-lamda for hospitalization if  unvaccinated
DRUG_COST = 530  # Cost of PEG-lambda
PAXLOVID_COST = 530  # Cost of Paxlovid
PAXLOVID_RR_VAX_OR_LR = 0.30  # Relative risk of nirmatrelvir/ritonavir for hospitalization if vaccinated/low risk
PAXLOVID_RR_UNVAX_HR = 0.11  # Relative risk of Paxlovid for hospitalization if unvaccinated/high risk
HOSP_COST = 20000  # Cost of COVID hospitalization  in the US
