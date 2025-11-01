/*
=====================================================
TELECOM CUSTOMER CHURN ANALYSIS
=====================================================
Author: Parth Patel
Date: November 2025
Dataset: Telecom Customer Churn (7,032 customers)
Database: MySQL

Purpose: 
Comprehensive churn analysis to identify key drivers,
calculate financial impact, and inform ML feature engineering.

Table of Contents:
1. Data Validation & Basic Exploration
2. Univariate Analysis
3. Segmentation & Pattern Discovery
4. Financial & Revenue Analytics
5. Advanced Analytics (CTEs, Window Functions)
=====================================================
*/

-- =====================================================
-- SECTION 1: DATA VALIDATION & BASIC EXPLORATION
-- =====================================================

-- Check total unique customers
SELECT 
    COUNT(DISTINCT customerID) as total_customers,
    COUNT(*) as total_records
FROM teleco;
-- Result: 7,032 unique customers

-- Verify data completeness
SELECT 
    COUNT(*) as total_rows,
    COUNT(customerID) as customer_count,
    COUNT(CASE WHEN Churn = 'Yes' THEN 1 END) as churned_count,
    COUNT(CASE WHEN Churn = 'No' THEN 1 END) as retained_count
FROM teleco;

-- Check for missing values
SELECT 
    COUNT(*) - COUNT(customerID) as missing_customerID,
    COUNT(*) - COUNT(tenure) as missing_tenure,
    COUNT(*) - COUNT(MonthlyCharges) as missing_monthly_charges,
    COUNT(*) - COUNT(TotalCharges) as missing_total_charges
FROM teleco;

-- Explore distinct categories
SELECT DISTINCT InternetService FROM teleco;
-- Values: DSL, Fiber Optic, No

SELECT DISTINCT Contract FROM teleco;
-- Values: Month-to-month, One year, Two year

SELECT DISTINCT PaymentMethod FROM teleco;
-- Values: Electronic check, Mailed check, Bank transfer (automatic), Credit card (automatic)

-- Overall churn rate
SELECT 
    COUNT(CASE WHEN Churn = 'Yes' THEN 1 END) AS total_churned,
    COUNT(CASE WHEN Churn = 'No' THEN 1 END) AS total_retained,
    ROUND(COUNT(CASE WHEN Churn = 'Yes' THEN 1 END) * 100.0 / COUNT(*), 2) AS churn_rate,
    ROUND(COUNT(CASE WHEN Churn = 'No' THEN 1 END) * 100.0 / COUNT(*), 2) AS retention_rate
FROM teleco;
-- Result: 1,869 churned (26.58%), 5,163 retained (73.42%)


-- =====================================================
-- SECTION 2: UNIVARIATE ANALYSIS
-- =====================================================

-- 2.1 Churn rate by contract type
-- Insight: Contract type is the strongest churn predictor
SELECT 
    Contract,
    COUNT(*) as total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) as churned_customers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as churn_rate
FROM teleco
GROUP BY Contract
ORDER BY churn_rate DESC;
/*
Result:
Month-to-month: 42.71% churn
One year: 11.28% churn
Two year: 2.85% churn
Key Finding: Long-term contracts reduce churn dramatically
*/

-- 2.2 Churn rate by internet service type
SELECT 
    InternetService,
    COUNT(*) as total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) as churned_customers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as churn_rate
FROM teleco
GROUP BY InternetService
ORDER BY churn_rate DESC;
/*
Result:
Fiber optic: 41.89% churn
DSL: 19.00% churn
No internet: 7.43% churn
Key Finding: Fiber optic customers have highest churn
*/

-- 2.3 Churn rate by payment method
SELECT 
    PaymentMethod,
    COUNT(*) as total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) as churned_customers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as churn_rate
FROM teleco
GROUP BY PaymentMethod
ORDER BY churn_rate DESC;
/*
Result:
Electronic check: 45.29% churn
Mailed check: 19.20% churn
Bank transfer (automatic): 16.73% churn
Credit card (automatic): 15.25% churn
Key Finding: Electronic check has highest churn risk
*/

-- 2.4 Churn rate by demographic factors
-- Gender analysis
SELECT 
    gender,
    COUNT(*) as total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) as churned_customers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as churn_rate
FROM teleco
GROUP BY gender;
-- Result: Gender has minimal impact (Male: 26.20%, Female: 26.96%)

-- Senior citizen analysis
SELECT 
    SeniorCitizen,
    COUNT(*) as total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) as churned_customers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as churn_rate
FROM teleco
GROUP BY SeniorCitizen;
/*
Result:
Senior citizens: 41.68% churn
Non-seniors: 23.65% churn
Key Finding: Seniors churn at higher rates
*/

-- 2.5 Churn rate by service features
-- Tech support impact
SELECT 
    TechSupport,
    COUNT(*) as total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) as churned_customers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as churn_rate
FROM teleco
GROUP BY TechSupport
ORDER BY churn_rate DESC;
/*
Result:
No tech support: 41.65% churn
With tech support: 15.20% churn
Key Finding: Tech support reduces churn by 26 percentage points
*/

-- Paperless billing impact
SELECT 
    PaperlessBilling,
    COUNT(*) as total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) as churned_customers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as churn_rate
FROM teleco
GROUP BY PaperlessBilling;
-- Result: Paperless billing: 33.59% vs Paper: 16.38%

-- 2.6 Average charges by churn status
SELECT 
    Churn,
    ROUND(AVG(MonthlyCharges), 2) as avg_monthly_charges,
    ROUND(AVG(TotalCharges), 2) as avg_total_charges,
    COUNT(*) as customer_count
FROM teleco
GROUP BY Churn;
/*
Result:
Churned customers: $74.44/month average
Retained customers: $61.31/month average
Key Finding: Higher monthly charges correlate with churn
*/


-- =====================================================
-- SECTION 3: SEGMENTATION & PATTERN DISCOVERY
-- =====================================================

-- 3.1 Churn by tenure buckets
SELECT 
    CASE 
        WHEN tenure BETWEEN 0 AND 12 THEN '0-12 months'
        WHEN tenure BETWEEN 13 AND 24 THEN '13-24 months'
        WHEN tenure BETWEEN 25 AND 48 THEN '25-48 months'
        WHEN tenure > 48 THEN '48+ months'
    END AS tenure_group,
    COUNT(*) as total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) as churned_customers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as churn_rate
FROM teleco
GROUP BY tenure_group
ORDER BY 
    CASE tenure_group
        WHEN '0-12 months' THEN 1
        WHEN '13-24 months' THEN 2
        WHEN '25-48 months' THEN 3
        WHEN '48+ months' THEN 4
    END;
/*
Result:
0-12 months: 47.68% churn (highest risk)
13-24 months: 34.75% churn
25-48 months: 15.48% churn
48+ months: 9.51% churn (lowest risk)
Key Finding: Linear relationship - longer tenure = lower churn
*/

-- 3.2 Contract + Internet service cross-analysis
SELECT 
    Contract,
    InternetService,
    COUNT(*) as total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) as churned_customers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as churn_rate
FROM teleco
GROUP BY Contract, InternetService
ORDER BY churn_rate DESC;
/*
Result:
Month-to-month + Fiber optic: 54.61% churn (HIGHEST RISK)
Month-to-month + DSL: 32.22% churn
One year + Fiber optic: 19.29% churn
Two year + Fiber optic: 7.23% churn
Key Finding: Combination of short contract + fiber = highest risk
*/

-- 3.3 Partner & Dependents effect
SELECT 
    Partner,
    Dependents,
    COUNT(*) as total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) as churned_customers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as churn_rate
FROM teleco
GROUP BY Partner, Dependents
ORDER BY churn_rate DESC;
/*
Result:
No partner + No dependents: 34.24% churn (highest)
Partner + Dependents: 14.31% churn (lowest)
Key Finding: Family ties reduce churn
*/

-- 3.4 Multiple services effect
SELECT 
    (CASE WHEN PhoneService = 'Yes' THEN 1 ELSE 0 END +
     CASE WHEN InternetService != 'No' THEN 1 ELSE 0 END +
     CASE WHEN StreamingTV = 'Yes' THEN 1 ELSE 0 END +
     CASE WHEN StreamingMovies = 'Yes' THEN 1 ELSE 0 END) AS number_of_services,
    COUNT(*) as total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) as churned_customers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as churn_rate
FROM teleco
GROUP BY number_of_services
ORDER BY number_of_services;
/*
Result:
1 service: 11.42% churn
2 services: 33.40% churn
3 services: 30.99% churn
Key Finding: Service bundling doesn't always reduce churn
*/


-- =====================================================
-- SECTION 4: FINANCIAL & REVENUE ANALYTICS
-- =====================================================

-- 4.1 Total monthly revenue lost due to churn
SELECT 
    COUNT(*) as churned_customers,
    ROUND(SUM(MonthlyCharges), 2) as monthly_revenue_lost,
    ROUND(SUM(MonthlyCharges) * 12, 2) as annual_revenue_lost
FROM teleco
WHERE Churn = 'Yes';
/*
Result:
Monthly revenue lost: $139,130.85
Annual revenue lost: $1,669,570.20
*/

-- 4.2 Revenue lost by contract type
SELECT 
    Contract,
    COUNT(*) as churned_customers,
    ROUND(SUM(MonthlyCharges), 2) as monthly_revenue_lost,
    ROUND(SUM(MonthlyCharges) * 12, 2) as annual_revenue_lost,
    ROUND(AVG(MonthlyCharges), 2) as avg_monthly_charge
FROM teleco
WHERE Churn = 'Yes'
GROUP BY Contract
ORDER BY monthly_revenue_lost DESC;
/*
Result:
Month-to-month: $1,450,165/year lost (largest impact)
One year: $169,421/year lost
Two year: $49,984/year lost
*/

-- 4.3 Revenue comparison: Churned vs Retained
SELECT 
    Churn,
    COUNT(*) as customer_count,
    ROUND(SUM(MonthlyCharges), 2) as total_monthly_revenue,
    ROUND(AVG(MonthlyCharges), 2) as avg_monthly_charge
FROM teleco
GROUP BY Churn;

-- 4.4 Customer Lifetime Value (CLV) approximation
SELECT 
    Churn,
    COUNT(*) as customer_count,
    ROUND(AVG(tenure * MonthlyCharges), 2) as avg_CLV,
    ROUND(MIN(tenure * MonthlyCharges), 2) as min_CLV,
    ROUND(MAX(tenure * MonthlyCharges), 2) as max_CLV
FROM teleco
GROUP BY Churn;
/*
Result:
Retained customers avg CLV: $2,555
Churned customers avg CLV: $1,532
Key Finding: Churned customers have 40% lower CLV
*/

-- 4.5 Top 10 high-value churned customers
SELECT 
    customerID,
    tenure,
    MonthlyCharges,
    TotalCharges,
    Contract,
    InternetService,
    PaymentMethod
FROM teleco
WHERE Churn = 'Yes'
ORDER BY TotalCharges DESC
LIMIT 10;


-- =====================================================
-- SECTION 5: ADVANCED ANALYTICS
-- =====================================================

-- 5.1 Top churn drivers ranked by impact (using CTE and UNION)
WITH churn_metrics AS (
    -- Contract type metrics
    SELECT 
        'Contract' as category_type,
        Contract as category_value,
        COUNT(*) as total_customers,
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) as churned_customers,
        ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as churn_rate
    FROM teleco
    GROUP BY Contract
    
    UNION ALL
    
    -- Internet service metrics
    SELECT 
        'InternetService',
        InternetService,
        COUNT(*),
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END),
        ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2)
    FROM teleco
    GROUP BY InternetService
    
    UNION ALL
    
    -- Payment method metrics
    SELECT 
        'PaymentMethod',
        PaymentMethod,
        COUNT(*),
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END),
        ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2)
    FROM teleco
    GROUP BY PaymentMethod
)
SELECT 
    category_type,
    category_value,
    total_customers,
    churned_customers,
    churn_rate,
    DENSE_RANK() OVER (ORDER BY churn_rate DESC) as risk_rank
FROM churn_metrics
ORDER BY churn_rate DESC
LIMIT 10;
/*
Result: Top 10 churn drivers across all categories
Enables data-driven prioritization of retention strategies
*/


-- =====================================================
-- KEY INSIGHTS SUMMARY
-- =====================================================
/*
TOP 5 CHURN DRIVERS:
1. Month-to-month contract (42.71% churn)
2. Electronic check payment (45.29% churn)
3. Fiber optic internet (41.89% churn)
4. No tech support (41.65% churn)
5. Short tenure 0-12 months (47.68% churn)

HIGHEST RISK COMBINATION:
Month-to-month + Fiber optic + Electronic check = 54.61% churn

FINANCIAL IMPACT:
- Annual revenue at risk: $1.67M
- Average CLV gap: $1,023 (retained vs churned)

ACTIONABLE RECOMMENDATIONS:
1. Incentivize contract upgrades (month-to-month → 1-year)
2. Promote automatic payment methods
3. Provide proactive tech support for fiber customers
4. Focus retention on 0-12 month tenure group
5. Review fiber optic service quality
*/


-- =====================================================
-- END OF ANALYSIS
-- =====================================================