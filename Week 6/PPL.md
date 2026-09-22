# Quantitative Methods for Finance (TCH442E) — Empirical Project Guide
## Cross-Sectional Determinants of Bank Returns Around SBV Credit Quota Announcements

---

## 1. Empirical Results and Regression Interpretation

### 1.1 Model Performance and Global Significance
The updated cross-sectional regression incorporates the pairwise data cleaning protocol, expanding the working sample size from 119 to **135 bank-event observations** across 17 listed Vietnamese commercial banks[cite: 14, 15]. Pairwise slicing preserved the July 15, 2021 credit-room allocation event (`2021_room_adj`) across all operating commercial banks, maintaining representation across all eight central bank announcements[cite: 14, 15].

* **Sample Size ($N$):** 135 observations across 17 banks and 8 policy events[cite: 15].
* **Explanatory Power ($R^2$):** The regression explains **22.2%** of the cross-sectional variance in 3-day Cumulative Abnormal Returns ($\text{CAR}[-1, +1]$), with an adjusted $R^2$ of **14.5%**[cite: 15]. For short-horizon event studies examining announcement-window abnormal returns, an $R^2$ in this range represents strong explanatory power[cite: 4, 15].
* **Joint Significance ($F$-test):** The overall model $F$-statistic is **3.081** ($p = 0.000787$)[cite: 15]. Evaluated with MacKinnon-White heteroskedasticity-robust standard errors (HC3), the model rejects the joint null hypothesis ($H_0: \beta_1 = \beta_2 = \dots = \beta_k = 0$) at the 0.1% significance level[cite: 2, 6, 15].
* **Collinearity Status:** Demeaning the asset size variable ($\text{Size\_dev}$) reduced the model condition number from $3.08 \times 10^3$ to $1.01 \times 10^3$[cite: 7, 14, 15].

### 1.2 OLS Regression Output Summary Table

| Explanatory Variable | Estimated Coef. ($\hat{\beta}$) | Robust Std. Error (HC3) | $z$-statistic | $p$-value | 95% Confidence Interval | Statistical Significance |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **const** | $+0.2371$ | $2.7680$ | $+0.09$ | $0.932$ | $[-5.188, +5.662]$ | Statistically Insignificant[cite: 15] |
| **SOE** | $-2.8032$ | $1.4080$ | $-1.99$ | $0.046$ | $[-5.562, -0.044]$ | Significant at 5% Level ($p < 0.05$)[cite: 15] |
| **NPL_pct** | $-0.0903$ | $0.3720$ | $-0.24$ | $0.808$ | $[-0.819, +0.638]$ | Statistically Insignificant[cite: 15] |
| **ROA_pct** | $-1.3116$ | $0.6720$ | $-1.95$ | $0.051$ | $[-2.628, +0.005]$ | Significant at 10% Level ($p \approx 0.05$)[cite: 15] |
| **LDR_pct** | $+0.0212$ | $0.0260$ | $+0.80$ | $0.423$ | $[-0.031, +0.073]$ | Statistically Insignificant[cite: 15] |
| **Size_dev** | $+1.3963$ | $0.6280$ | $+2.22$ | $0.026$ | $[+0.165, +2.628]$ | Significant at 5% Level ($p < 0.05$)[cite: 15] |
| **2022_room_exp** | $+0.5891$ | $1.3950$ | $+0.42$ | $0.673$ | $[-2.145, +3.323]$ | Base: `2021_room_adj`[cite: 1, 15] |
| **Event Dummies (6)** | *Included* | *Robust* | — | — | *Event Fixed Effects* | Controls for macro shocks[cite: 1, 15] |

---

### 1.3 Economic Interpretation of Regressors

#### State Ownership Discount (`SOE`, $\hat{\beta} = -2.8032, p = 0.046$)
Holding profitability, asset quality, liquidity, bank size, and macroeconomic conditions fixed, State-Owned Commercial Banks (Vietcombank, BIDV, VietinBank) experience a **2.80 percentage point lower Cumulative Abnormal Return** relative to private joint-stock commercial banks[cite: 1, 7, 15].
* *Economic Mechanism:* In Vietnam's banking system, state-owned lenders operate under systemic mandates to maintain credit availability for state-targeted sectors and public infrastructure projects. They maintain predictable, pre-allocated credit quotas and benefit from preferential refinancing channels from the State Bank of Vietnam (SBV). In contrast, private joint-stock banks (such as Techcombank, VPBank, MB, and ACB) are tightly constrained by annual regulatory lending limits. When the SBV issues unexpected credit-quota adjustments, private lenders experience a direct loosening of their revenue-generating capacity, eliciting a stronger positive equity market re-rating[cite: 15].

#### Bank Scale Premium (`Size_dev`, $\hat{\beta} = +1.3963, p = 0.026$)
A 1-unit increase in log total assets above the sample average increases the 3-day abnormal announcement return by **1.40 percentage points** ($p < 0.05$)[cite: 7, 15].
* *Economic Mechanism:* Large commercial banks possess syndicated loan syndication teams, established corporate relationships, and nationwide branch networks. Upon receiving an administrative expansion in lending room, large-cap institutions possess the balance sheet capacity and underwriting pipeline to deploy new capital quickly into interest-earning assets. Smaller tier-3 lenders face borrower creditworthiness constraints and higher underwriting friction, resulting in lower expected cash flow accretion per percentage point of granted quota[cite: 15].

#### Profitability Operational Leverage (`ROA_pct`, $\hat{\beta} = -1.3116, p = 0.051$)
A 1-percentage-point increase in pre-event Return on Assets corresponds to a **1.31 percentage point decrease in announcement CAR** ($p \approx 0.05$)[cite: 7, 15].
* *Economic Mechanism:* Highly profitable commercial banks already operate near optimal capital efficiency, and their equity valuations already incorporate a performance premium. Conversely, banks with lower baseline profitability possess higher operating leverage: expanding lending volume allows them to dilute fixed funding and operating costs, generating a larger marginal impact on net interest margins and unexpected earnings growth[cite: 15].

#### Insignificance of Accounting Ratios (`NPL_pct`, $p = 0.808$; `LDR_pct`, $p = 0.423$)
Neither the reported non-performing loan ratio nor the loan-to-deposit ratio exhibits a statistically significant link with short-term abnormal returns[cite: 15].
* *Economic Mechanism:* Equity investors in Vietnam recognize that official credit-quota distribution is governed by systemic factors (bank tiering under Circular 52/2018/TT-NHNN, capital adequacy ratios, and state participation) rather than historical accounting metrics. Furthermore, reported NPL figures often diverge from real credit distress due to forbearance and debt restructuring circulars (such as Circular 02/2023/TT-NHNN and Circular 06/2024/TT-NHNN), causing market participants to discount official accounting quality metrics during monetary policy announcements[cite: 15].

---

## 2. Methodological Roadmap: Next Econometric Steps

To meet the structural and diagnostic criteria specified in the TCH442E Group Assignment Exam Paper, the empirical analysis requires four additional steps[cite: 9]:

### Step 1: Center `LDR_pct` to Eliminate the High Condition Number
Although demeaning `Size` resolved the intercept collinearity, `LDR_pct` has a numerical mean of approximately 105%, whereas `ROA_pct` and `NPL_pct` have means near 1.6%[cite: 14, 15].
* **Procedure:** Define $\text{LDR\_dev}_i = \text{LDR\_pct}_i - \overline{\text{LDR\_pct}}$[cite: 7].
* **Outcome:** Entering $\text{LDR\_dev}$ in place of $\text{LDR\_pct}$ reduces the matrix condition number below 30, fully resolving statsmodels Note [2] without altering slope coefficients, standard errors, $t$-statistics, or $p$-values[cite: 7, 15].

### Step 2: Construct the Stage 1 Event Study Summary Table
Formal event study methodology requires documenting whether the market as a whole reacted positively or negatively to each announcement before analyzing cross-sectional variations[cite: 9, 11].
* **Procedure:** Calculate the cross-sectional Cumulative Average Abnormal Return ($\text{CAAR}[-1, +1]$) and standard deviation across all 17 banks for each of the eight event dates[cite: 9].
* **Statistical Test:** Compute cross-sectional $t$-statistics:
  $$t = \frac{\text{CAAR}}{\text{Standard Deviation} / \sqrt{N}}$$
[cite: 6]
* **Deliverable:** Produce Table 2 in the report, showing event names, calendar dates, number of participating banks, mean CAAR, $t$-statistics, and two-tailed $p$-values[cite: 6, 9].

### Step 3: Implement a Three-Model Hierarchical Architecture
To demonstrate econometric rigor per Session 6 and the project rubric, estimate three nested regression specifications[cite: 1, 9]:
1. **Model 1 (Baseline Cross-Section):** Regress $\text{CAR\_pct}$ exclusively on bank balance sheet variables ($\text{SOE}$, $\text{NPL\_pct}$, $\text{ROA\_pct}$, $\text{LDR\_dev}$, $\text{Size\_dev}$) without event dummies to quantify fundamental explanatory power in isolation[cite: 7].
2. **Model 2 (Event Fixed Effects):** Incorporate the seven event dummies (using `2021_room_adj` as the omitted reference group under the $g-1$ rule) to isolate macro shocks from bank-level effects[cite: 1].
3. **Model 3 (Structural Interaction):** Introduce an interaction between ownership status and liquidity constraints ($\text{SOE} \times \text{LDR\_dev}$)[cite: 1, 7]. This tests whether regulatory liquidity pressure matters primarily for private joint-stock commercial banks rather than state-owned banks[cite: 1].

### Step 4: Run the Complete Course Diagnostic Battery
Fulfill the course diagnostic framework from Sessions 3, 7, and 8[cite: 2, 5, 10]:
1. **Multicollinearity:** Calculate Variance Inflation Factors (VIF) for all continuous and indicator regressors, documenting that all values sit well below the rule-of-thumb threshold of 10[cite: 5].
2. **Heteroskedasticity Tests:** Execute the Breusch-Pagan Lagrange Multiplier test and White's General test on OLS residuals[cite: 2]. Documenting rejection of homoskedasticity ($p < 0.05$) provides empirical justification for reporting MacKinnon-White (HC3) robust standard errors[cite: 2].
3. **Functional Form Specification (Ramsey RESET):** Perform the Ramsey RESET test using squared and cubed fitted values to confirm that linear parameterization is adequate and that higher-order polynomial terms are not omitted[cite: 10].
4. **Outlier and Studentized Residual Diagnostics:** Calculate studentized residuals for all 135 observations[cite: 10]. Identify observations where $\vert{}r_i\vert{} > 2.0$, and re-estimate Model 2 on the clean subsample to verify that the statistical significance of $\text{SOE}$ and $\text{Size\_dev}$ is not driven by isolated outliers[cite: 10, 15].

---

## 3. Four-Member Task Allocation and Milestone Timeline

Per the assessment instructions, each student must lead a distinct component of the empirical pipeline and write one signed paragraph summarizing their contributions in the final report[cite: 9].
