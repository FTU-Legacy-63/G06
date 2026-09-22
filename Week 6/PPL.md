#### Economic Mechanisms Behind Each Regressor

* **The State-Ownership Discount (`SOE`, $\hat{\beta} = -2.8032, p = 0.046$):**  
  Holding profitability, credit risk, liquidity, total assets, and event-specific shocks fixed, State-Owned Commercial Banks (Vietcombank, BIDV, and VietinBank) experience a **2.80 percentage point lower 3-day abnormal return** relative to private joint-stock commercial banks ($p < 0.05$)[cite: 1, 7, 15].  
  *Economic justification for your report:* In Vietnam's commercial banking sector, state-owned lenders operate under direct policy mandates to support economic stability and often receive preferential baseline credit growth targets early in the fiscal year. Private joint-stock banks (such as VPBank, Techcombank, MB, and ACB), by contrast, face rigid regulatory ceilings that constrain aggressive credit expansion. Therefore, an administrative quota expansion represents a substantial upside surprise for private banks by directly loosening their binding growth constraints, producing a sharper equity re-rating[cite: 15].

* **The Bank Scale Premium (`Size_dev`, $\hat{\beta} = +1.3963, p = 0.026$):**  
  A one-unit increase in log total assets above the banking sector average is associated with a **1.40 percentage point increase in announcement CAR** ($p < 0.05$)[cite: 7, 15].  
  *Economic justification for your report:* Larger commercial banks possess established corporate customer ecosystems, syndicated lending infrastructure, and wider branch networks. When the central bank allocates additional lending room, Tier-1 institutions can disburse credit and convert additional quota into net interest income much faster than smaller Tier-3 institutions, making credit room economically more accretive to large-cap banks[cite: 15].

* **Profitability Operational Leverage (`ROA_pct`, $\hat{\beta} = -1.3116, p = 0.051$):**  
  A 1-percentage-point increase in pre-event Return on Assets corresponds to a **1.31 percentage point decrease in announcement CAR**[cite: 7, 15].  
  *Economic justification for your report:* High-ROA banks already operate near peak balance sheet efficiency, and their equity valuations already price in superior asset yields. Banks with moderate or lower baseline profitability gain disproportionately higher marginal operating leverage from incremental credit expansion, resulting in a stronger positive price reaction upon quota distribution[cite: 15].

* **The Insignificance of Accounting Ratios (`NPL_pct`, $p = 0.808$; `LDR_pct`, $p = 0.423$):**  
  Neither reported non-performing loan ratios nor accounting loan-to-deposit ratios display statistical significance[cite: 15].  
  *Economic justification for your report:* In Vietnam's domestic equity market, investors view credit-room allocation as driven primarily by bank scale, systemic capitalization, and regulatory standing rather than backward-looking financial ratios. Furthermore, reported non-performing loans frequently diverge from economic reality due to credit restructuring regulations (such as Circular 02/2023/TT-NHNN and Circular 06/2024/TT-NHNN), leading investors to discount accounting asset quality figures when reacting to policy announcements[cite: 15].

---

### Step-by-Step Instructions on What to Do Next

To complete the requirements specified in the TCH442E exam paper, execute the following four analytical steps in your project workflow[cite: 9]:

#### Step 1: Center `LDR_pct` to Eliminate the Collinearity Warning
In the notes beneath your regression table, statsmodels still displays Note [2] stating that the condition number is $1.01 \times 10^3$[cite: 15]. While demeaning `Size` eliminated the severe constant-collinearity problem, `LDR_pct` has a numerical mean near 105% while `ROA_pct` and `NPL_pct` have means near 1.6%[cite: 14, 15]. 
* **Action:** Demean the Loan-to-Deposit Ratio by subtracting its sample mean: $\text{LDR\_dev}_i = \text{LDR\_pct}_i - \overline{\text{LDR\_pct}}$[cite: 7].
* **Outcome:** When you substitute $\text{LDR\_dev}$ for $\text{LDR\_pct}$, the condition number will drop below 30, fully eliminating Note [2][cite: 7, 15]. The slope coefficients, standard errors, $t$-statistics, and $p$-values will remain unchanged, while the intercept will represent the expected return of an average-sized private bank with average liquidity during the reference event[cite: 1, 7].

#### Step 2: Construct the Stage 1 Event Study Summary (Table 2 in Your Report)
Before evaluating cross-sectional regressions, formal event study methodology requires documenting whether the market as a whole reacted positively or negatively to each announcement[cite: 9, 11].
* **Action:** Group your panel dataset by event date and calculate the cross-sectional Cumulative Average Abnormal Return ($\text{CAAR}[-1, +1]$) and standard deviation across all 17 banks for each event[cite: 6, 9].
* **Testing:** Compute a standard cross-sectional $t$-statistic for each event date:
  $$t = \frac{\text{CAAR}}{\text{Standard Deviation} / \sqrt{N}}$$
[cite: 6]
* **Reporting:** Present these findings in a summary table showing the event label, calendar date, number of active banks, average abnormal return, and whether the market response was statistically significant at the 5% or 1% level[cite: 6, 9].

#### Step 3: Estimate a Three-Model Architecture (Table 3 in Your Report)
The exam instructions encourage students to demonstrate econometric depth by comparing nested specifications[cite: 1, 9]. Present three progressive models in a side-by-side regression table:
1. **Model 1 (Baseline Fundamentals):** Regress $\text{CAR\_pct}$ exclusively on the bank balance sheet controls ($\text{SOE}$, $\text{NPL\_pct}$, $\text{ROA\_pct}$, $\text{LDR\_dev}$, $\text{Size\_dev}$) without event dummies[cite: 7]. This shows how much variation bank characteristics explain on a standalone basis[cite: 5, 7].
2. **Model 2 (Event Fixed Effects):** Introduce the seven event dummy variables (using the 2021 credit adjustment as the reference category under the $g-1$ rule)[cite: 1]. This controls for market-wide macroeconomic shocks specific to each announcement and corresponds to your current model[cite: 1, 15].
3. **Model 3 (Structural Interaction):** Add an interaction term between State Ownership and the demeaned Loan-to-Deposit Ratio: $\text{SOE} \times \text{LDR\_dev}$[cite: 1, 7]. This tests whether balance sheet liquidity constraints matter more for private commercial banks than for state-owned institutions that enjoy systemic state liquidity backstops[cite: 1].

#### Step 4: Execute the Course Diagnostic Suite (Table 4 in Your Report)
To satisfy the econometric testing requirements covered in Sessions 3, 7, and 8, generate a diagnostic table reporting[cite: 2, 5, 9, 10]:
1. **Variance Inflation Factors (VIF):** Calculate the VIF for each regressor in the baseline model[cite: 5]. Show that all values sit well below the rule-of-thumb threshold of 10 (and below 3 for financial ratios), proving that multicollinearity does not inflate parameter standard errors[cite: 5].
2. **Heteroskedasticity Tests:** Run both the Breusch-Pagan Lagrange Multiplier test and White's General Heteroskedasticity test[cite: 2]. Report the test statistics and $p$-values in your report to justify why your analysis employs MacKinnon-White HC3 robust standard errors[cite: 2].
3. **Functional Form Specification (Ramsey RESET):** Conduct the Ramsey RESET test using squared and cubed fitted values[cite: 10]. An insignificant $F$-test failure to reject the null hypothesis demonstrates that the linear specification adequately approximates the return-generating process[cite: 10].
4. **Outlier and Influential Point Diagnostics:** Compute studentized residuals for all 135 observations[cite: 10]. Flag observations where the absolute studentized residual exceeds 2.0 (such as sharp single-bank moves in Eximbank or LienVietPostBank during specific announcements)[cite: 10]. Re-estimate Model 2 on the trimmed sample to show that the statistical significance of $\text{SOE}$ and $\text{Size\_dev}$ remains robust and is not driven by individual outlier trading sessions[cite: 10, 15].

---

### Task Division Across Your 4 Group Members

| Member | Assigned Project Role | Specific Deliverables for the Final Report |
| :--- | :--- | :--- |
| **Member 1** | **Data Engineering & Event Study Lead** | 1. Calculate the demeaned liquidity ratio ($\text{LDR\_dev}$)[cite: 7].<br>2. Generate Table 1 (Summary Statistics of 17 Banks) and Table 2 (Stage 1 Event Study CAAR and $t$-tests across all 8 dates)[cite: 6, 9].<br>3. Write Section 3 of the report (Data Sources, Variable Definitions, and Circular 96/2020/TT-BTC Timing Lags)[cite: 9]. |
| **Member 2** | **Econometric Modeling & Diagnostics Lead** | 1. Estimate the 3-model regression table (Baseline, Event Fixed Effects, and Ownership-Liquidity Interaction)[cite: 1].<br>2. Execute the full diagnostic battery: VIF, Breusch-Pagan, White, Ramsey RESET, and studentized residuals[cite: 2, 5, 10].<br>3. Compile Table 3 and Table 4, and write Section 4 (Econometric Specification and Estimation Methodology)[cite: 9]. |
| **Member 3** | **Institutional Framework & Literature Lead** | 1. Document the regulatory mechanism of SBV credit quotas under the Law on the State Bank of Vietnam No. 46/2010/QH12 and Circular 22/2019/TT-NHNN.<br>2. Formulate three core research hypotheses ($H_1$: Ownership Disparity, $H_2$: Bank Scale Advantage, $H_3$: Profitability/Operating Leverage).<br>3. Synthesize 3 to 4 academic papers (including MacKinlay 1997 on event studies and Bernanke & Blinder 1992 on the bank lending channel) to write Section 1 (Introduction) and Section 2 (Literature Review)[cite: 9, 11]. |
| **Member 4** | **Economic Interpretation & Project Manager** | 1. Author Section 5 (Empirical Interpretation of Coefficients and Economic Impact) using the economic rationales detailed above[cite: 9].<br>2. Author Section 6 (Limitations, Endogeneity Considerations, and Policy Implications)[cite: 9, 10].<br>3. Conduct a full reproducibility check of the Jupyter Notebook, verify the 2,000–3,000 word count target, and compile the final signed contribution statements[cite: 9]. |
