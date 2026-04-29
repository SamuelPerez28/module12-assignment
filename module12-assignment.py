# Module 12 Assignment: Business Analytics Fundamentals and Applications
# GreenGrocer Data Analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

print("=" * 60)
print("GREENGROCER BUSINESS ANALYTICS")
print("=" * 60)

# ---------------------------------------------------------
# ALL DATA CREATION CODE (DO NOT MODIFY)
# THIS MUST BE AT TOP LEVEL — NOT INSIDE ANY FUNCTION
# ---------------------------------------------------------

np.random.seed(42)

stores = ["Tampa", "Orlando", "Miami", "Jacksonville", "Gainesville"]
store_data = {
    "Store": stores,
    "SquareFootage": [15000, 12000, 18000, 10000, 8000],
    "StaffCount": [45, 35, 55, 30, 25],
    "YearsOpen": [5, 3, 7, 2, 1],
    "WeeklyMarketingSpend": [2500, 2000, 3000, 1800, 1500]
}

store_df = pd.DataFrame(store_data)

departments = ["Produce", "Dairy", "Bakery", "Grocery", "Prepared Foods"]
categories = {
    "Produce": ["Organic Vegetables", "Organic Fruits", "Fresh Herbs"],
    "Dairy": ["Milk & Cream", "Cheese", "Yogurt"],
    "Bakery": ["Bread", "Pastries", "Cakes"],
    "Grocery": ["Grains", "Canned Goods", "Snacks"],
    "Prepared Foods": ["Hot Bar", "Salad Bar", "Sandwiches"]
}

sales_data = []
dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")

store_performance = {
    "Tampa": 1.0, 
    "Orlando": 0.85, 
    "Miami": 1.2, 
    "Jacksonville": 0.75, 
    "Gainesville": 0.65
}

dept_performance = {
    "Produce": 1.2,
    "Dairy": 1.0,
    "Bakery": 0.85,
    "Grocery": 0.95,
    "Prepared Foods": 1.1
}

for date in dates:
    month = date.month
    seasonal_factor = 1.0
    if month in [6, 7, 8]:
        seasonal_factor = 1.15
    elif month == 12:
        seasonal_factor = 1.25
    elif month in [1, 2]:
        seasonal_factor = 0.9

    dow_factor = 1.3 if date.dayofweek >= 5 else 1.0

    for store in stores:
        store_factor = store_performance[store]

        for dept in departments:
            dept_factor = dept_performance[dept]

            for category in categories[dept]:
                base_sales = np.random.normal(loc=500, scale=100)
                sales_amount = base_sales * store_factor * dept_factor * seasonal_factor * dow_factor
                sales_amount *= np.random.normal(loc=1.0, scale=0.1)

                base_margin = {
                    "Produce": 0.25,
                    "Dairy": 0.22,
                    "Bakery": 0.35,
                    "Grocery": 0.20,
                    "Prepared Foods": 0.40
                }[dept]

                profit_margin = base_margin * np.random.normal(loc=1.0, scale=0.05)
                profit_margin = max(min(profit_margin, 0.5), 0.15)

                profit = sales_amount * profit_margin

                sales_data.append({
                    "Date": date,
                    "Store": store,
                    "Department": dept,
                    "Category": category,
                    "Sales": round(sales_amount, 2),
                    "ProfitMargin": round(profit_margin, 4),
                    "Profit": round(profit, 2)
                })

sales_df = pd.DataFrame(sales_data)

# CUSTOMER DATA
customer_data = []
total_customers = 5000
age_mean, age_std = 42, 15
income_mean, income_std = 85, 30

segments = ["Health Enthusiast", "Gourmet Cook", "Family Shopper", "Budget Organic", "Occasional Visitor"]
segment_probabilities = [0.25, 0.20, 0.30, 0.15, 0.10]

store_probs = {
    "Tampa": 0.25,
    "Orlando": 0.20,
    "Miami": 0.30,
    "Jacksonville": 0.15,
    "Gainesville": 0.10
}

for i in range(total_customers):
    age = int(np.random.normal(loc=age_mean, scale=age_std))
    age = max(min(age, 85), 18)

    gender = np.random.choice(["M", "F"], p=[0.48, 0.52])

    income = int(np.random.normal(loc=income_mean, scale=income_std))
    income = max(income, 20)

    segment = np.random.choice(segments, p=segment_probabilities)
    preferred_store = np.random.choice(stores, p=list(store_probs.values()))

    if segment == "Health Enthusiast":
        visit_frequency = np.random.randint(8, 15)
        avg_basket = np.random.normal(loc=75, scale=15)
    elif segment == "Gourmet Cook":
        visit_frequency = np.random.randint(4, 10)
        avg_basket = np.random.normal(loc=120, scale=25)
    elif segment == "Family Shopper":
        visit_frequency = np.random.randint(5, 12)
        avg_basket = np.random.normal(loc=150, scale=30)
    elif segment == "Budget Organic":
        visit_frequency = np.random.randint(6, 10)
        avg_basket = np.random.normal(loc=60, scale=10)
    else:
        visit_frequency = np.random.randint(1, 5)
        avg_basket = np.random.normal(loc=45, scale=15)

    visit_frequency = max(min(visit_frequency, 30), 1)
    avg_basket = max(avg_basket, 15)

    monthly_spend = visit_frequency * avg_basket
    if monthly_spend > 1000:
        loyalty_tier = "Platinum"
    elif monthly_spend > 500:
        loyalty_tier = "Gold"
    elif monthly_spend > 200:
        loyalty_tier = "Silver"
    else:
        loyalty_tier = "Bronze"

    customer_data.append({
        "CustomerID": f"C{i+1:04d}",
        "Age": age,
        "Gender": gender,
        "Income": income * 1000,
        "Segment": segment,
        "PreferredStore": preferred_store,
        "VisitsPerMonth": visit_frequency,
        "AvgBasketSize": round(avg_basket, 2),
        "MonthlySpend": round(monthly_spend, 2),
        "LoyaltyTier": loyalty_tier
    })

customer_df = pd.DataFrame(customer_data)

# OPERATIONAL DATA
operational_data = []

for store in stores:
    store_row = store_df[store_df["Store"] == store].iloc[0]
    square_footage = store_row["SquareFootage"]
    staff_count = store_row["StaffCount"]

    store_sales = sales_df[sales_df["Store"] == store]["Sales"].sum()
    store_profit = sales_df[sales_df["Store"] == store]["Profit"].sum()

    sales_per_sqft = store_sales / square_footage
    profit_per_sqft = store_profit / square_footage
    sales_per_staff = store_sales / staff_count
    inventory_turnover = np.random.uniform(12, 18) * store_performance[store]
    customer_satisfaction = min(5, np.random.normal(loc=4.0, scale=0.3) * (store_performance[store] ** 0.5))

    operational_data.append({
        "Store": store,
        "AnnualSales": round(store_sales, 2),
        "AnnualProfit": round(store_profit, 2),
        "SalesPerSqFt": round(sales_per_sqft, 2),
        "ProfitPerSqFt": round(profit_per_sqft, 2),
        "SalesPerStaff": round(sales_per_staff, 2),
        "InventoryTurnover": round(inventory_turnover, 2),
        "CustomerSatisfaction": round(customer_satisfaction, 2)
    })

operational_df = pd.DataFrame(operational_data)

# ---------------------------------------------------------
# FUNCTION DEFINITIONS
# ---------------------------------------------------------

# 1.1 Calculate and display basic descriptive statistics for sales and profit
# REQUIRED: Store results in variables for testing
def analyze_sales_performance():
    """
    Analyze overall sales performance with descriptive statistics
    REQUIRED: Create and return dictionary with keys:
    - 'total_sales': float
    - 'total_profit': float
    - 'avg_profit_margin': float
    - 'sales_by_store': pandas Series
    - 'sales_by_dept': pandas Series
    """
    total_sales = sales_df["Sales"].sum()
    total_profit = sales_df["Profit"].sum()
    avg_profit_margin = sales_df["ProfitMargin"].mean()

    sales_by_store = sales_df.groupby("Store")["Sales"].sum()
    sales_by_dept = sales_df.groupby("Department")["Sales"].sum()

    return {
        "total_sales": total_sales,
        "total_profit": total_profit,
        "avg_profit_margin": avg_profit_margin,
        "sales_by_store": sales_by_store,
        "sales_by_dept": sales_by_dept
    }


# 1.2 Create visualizations showing sales distribution by store, department, and time
# REQUIRED: Return matplotlib figures
def visualize_sales_distribution():
    """
    Create visualizations showing how sales are distributed
    REQUIRED: Return tuple of three figures (store_fig, dept_fig, time_fig)
    """
    # Sales by store
    store_sales = sales_df.groupby("Store")["Sales"].sum()
    store_fig, store_ax = plt.subplots()
    store_ax.bar(store_sales.index, store_sales.values)
    store_ax.set_title("Total Sales by Store")
    store_ax.set_xlabel("Store")
    store_ax.set_ylabel("Sales ($)")

    # Sales by department
    dept_sales = sales_df.groupby("Department")["Sales"].sum()
    dept_fig, dept_ax = plt.subplots()
    dept_ax.bar(dept_sales.index, dept_sales.values)
    dept_ax.set_title("Total Sales by Department")
    dept_ax.set_xlabel("Department")
    dept_ax.set_ylabel("Sales ($)")
    dept_ax.tick_params(axis="x", rotation=45)

    # Monthly sales trend
    monthly_sales = (
        sales_df
        .set_index("Date")["Sales"]
        .resample("M")
        .sum()
    )
    time_fig, time_ax = plt.subplots()
    time_ax.plot(monthly_sales.index, monthly_sales.values, marker="o")
    time_ax.set_title("Monthly Sales Trend")
    time_ax.set_xlabel("Month")
    time_ax.set_ylabel("Sales ($)")

    return store_fig, dept_fig, time_fig


# 1.3 Analyze customer segments and their spending patterns
# REQUIRED: Return analysis results
def analyze_customer_segments():
    """
    Analyze customer segments and their relationship to spending
    REQUIRED: Return dictionary with keys:
    - 'segment_counts': pandas Series
    - 'segment_avg_spend': pandas Series
    - 'segment_loyalty': pandas DataFrame
    """
    segment_counts = customer_df["Segment"].value_counts()
    segment_avg_spend = customer_df.groupby("Segment")["MonthlySpend"].mean()
    segment_loyalty = pd.crosstab(customer_df["Segment"], customer_df["LoyaltyTier"])

    return {
        "segment_counts": segment_counts,
        "segment_avg_spend": segment_avg_spend,
        "segment_loyalty": segment_loyalty
    }


# 2.1 Identify factors correlated with sales performance
# REQUIRED: Return correlation results
def analyze_sales_correlations():
    """
    Analyze correlations between various factors and sales performance
    REQUIRED: Return dictionary with keys:
    - 'store_correlations': pandas DataFrame
    - 'top_correlations': list of tuples (factor, correlation)
    - 'correlation_fig': matplotlib figure
    """
    store_sales = sales_df.groupby("Store")["Sales"].sum().reset_index()
    merged = pd.merge(store_sales, operational_df, on="Store")

    numeric_cols = ["Sales", "AnnualProfit", "SalesPerSqFt", "ProfitPerSqFt",
                    "SalesPerStaff", "InventoryTurnover", "CustomerSatisfaction"]

    store_correlations = merged[numeric_cols].corr()

    sales_corr = store_correlations["Sales"].drop("Sales")
    top = sales_corr.abs().sort_values(ascending=False).head(3)
    top_correlations = list(zip(top.index, sales_corr[top.index]))

    correlation_fig, ax = plt.subplots()
    cax = ax.matshow(store_correlations, cmap="coolwarm")
    plt.xticks(range(len(numeric_cols)), numeric_cols, rotation=90)
    plt.yticks(range(len(numeric_cols)), numeric_cols)
    plt.colorbar(cax)
    ax.set_title("Correlation Heatmap of Store Performance Metrics", pad=20)

    return {
        "store_correlations": store_correlations,
        "top_correlations": top_correlations,
        "correlation_fig": correlation_fig
    }


# 2.2 Compare stores based on operational metrics
# REQUIRED: Return comparison results
def compare_store_performance():
    """
    Compare stores across different operational metrics
    REQUIRED: Return dictionary with keys:
    - 'efficiency_metrics': pandas DataFrame (with SalesPerSqFt, SalesPerStaff)
    - 'performance_ranking': pandas Series (ranked by profit)
    - 'comparison_fig': matplotlib figure
    """
    efficiency_metrics = operational_df[["Store", "SalesPerSqFt", "SalesPerStaff"]].set_index("Store")
    performance_ranking = operational_df.set_index("Store")["AnnualProfit"].sort_values(ascending=False)

    comparison_fig, ax = plt.subplots()
    ax.bar(operational_df["Store"], operational_df["AnnualProfit"])
    ax.set_title("Annual Profit by Store")
    ax.set_xlabel("Store")
    ax.set_ylabel("Annual Profit ($)")
    ax.tick_params(axis="x", rotation=45)

    return {
        "efficiency_metrics": efficiency_metrics,
        "performance_ranking": performance_ranking,
        "comparison_fig": comparison_fig
    }


# 2.3 Analyze seasonal patterns and their impact
# REQUIRED: Return seasonal analysis
def analyze_seasonal_patterns():
    """
    Identify and visualize seasonal patterns in sales data
    REQUIRED: Return dictionary with keys:
    - 'monthly_sales': pandas Series
    - 'dow_sales': pandas Series (day of week)
    - 'seasonal_fig': matplotlib figure
    """
    monthly_sales = (
        sales_df
        .set_index("Date")["Sales"]
        .resample("M")
        .sum()
    )

    sales_df["DayOfWeek"] = sales_df["Date"].dt.dayofweek
    dow_sales = sales_df.groupby("DayOfWeek")["Sales"].mean()

    seasonal_fig, ax = plt.subplots()
    ax.plot(monthly_sales.index, monthly_sales.values, marker="o", label="Monthly Sales")
    ax.set_title("Seasonal Sales Patterns")
    ax.set_xlabel("Month")
    ax.set_ylabel("Sales ($)")
    ax.legend()

    return {
        "monthly_sales": monthly_sales,
        "dow_sales": dow_sales,
        "seasonal_fig": seasonal_fig
    }


# 3.1 Create a simple linear regression model to predict store sales
# REQUIRED: Return model results
def predict_store_sales():
    """
    Use linear regression to predict store sales based on store characteristics
    REQUIRED: Return dictionary with keys:
    - 'coefficients': dict (feature: coefficient)
    - 'r_squared': float
    - 'predictions': pandas Series
    - 'model_fig': matplotlib figure
    """
    X = store_df[["SquareFootage", "StaffCount", "YearsOpen", "WeeklyMarketingSpend"]]
    y = operational_df["AnnualSales"]

    X_std = (X - X.mean()) / X.std()
    X_design = np.column_stack([np.ones(len(X_std)), X_std])

    beta, _, _, _ = np.linalg.lstsq(X_design, y, rcond=None)

    coefficients = {
        "Intercept": beta[0],
        "SquareFootage": beta[1],
        "StaffCount": beta[2],
        "YearsOpen": beta[3],
        "WeeklyMarketingSpend": beta[4]
    }

    predictions = pd.Series(X_design @ beta, index=store_df["Store"])

    ss_res = np.sum((y - predictions) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    r_squared = 1 - (ss_res / ss_tot)

    model_fig, ax = plt.subplots()
    ax.scatter(y, predictions)
    ax.plot([y.min(), y.max()], [y.min(), y.max()], color="red")
    ax.set_title("Actual vs Predicted Store Sales")
    ax.set_xlabel("Actual Sales")
    ax.set_ylabel("Predicted Sales")

    return {
        "coefficients": coefficients,
        "r_squared": r_squared,
        "predictions": predictions,
        "model_fig": model_fig
    }


# 3.2 Forecast departmental sales trends
# REQUIRED: Return forecast results
def forecast_department_sales():
    """
    Analyze and forecast departmental sales trends
    REQUIRED: Return dictionary with keys:
    - 'dept_trends': pandas DataFrame
    - 'growth_rates': pandas Series
    - 'forecast_fig': matplotlib figure
    """
    dept_trends = (
        sales_df
        .groupby(["Department", sales_df["Date"].dt.to_period("M")])["Sales"]
        .sum()
        .unstack(level=0)
        .fillna(0)
    )

    dept_trends.index = dept_trends.index.to_timestamp()

    growth_rates = (dept_trends.iloc[-1] - dept_trends.iloc[0]) / dept_trends.iloc[0]

    forecast_fig, ax = plt.subplots()
    for dept in dept_trends.columns:
        ax.plot(dept_trends.index, dept_trends[dept], marker="o", label=dept)

    ax.set_title("Department Sales Trends Over Time")
    ax.set_xlabel("Month")
    ax.set_ylabel("Sales ($)")
    ax.legend()

    return {
        "dept_trends": dept_trends,
        "growth_rates": growth_rates,
        "forecast_fig": forecast_fig
    }


# 4.1 Identify the most profitable combinations of store, department, and customer segments
# REQUIRED: Return opportunity analysis
def identify_profit_opportunities():
    """
    Identify the most profitable combinations and potential opportunities
    REQUIRED: Return dictionary with keys:
    - 'top_combinations': pandas DataFrame (top 10 store-dept combinations)
    - 'underperforming': pandas DataFrame (bottom 10)
    - 'opportunity_score': pandas Series (by store)
    """
    combo_profit = (
        sales_df
        .groupby(["Store", "Department"])["Profit"]
        .sum()
        .reset_index()
        .sort_values("Profit", ascending=False)
    )

    top_combinations = combo_profit.head(10)
    underperforming = combo_profit.tail(10)

    opportunity_score = (
        operational_df.set_index("Store")["ProfitPerSqFt"] +
        operational_df.set_index("Store")["CustomerSatisfaction"]
    )

    return {
        "top_combinations": top_combinations,
        "underperforming": underperforming,
        "opportunity_score": opportunity_score
    }


# 4.2 Develop recommendations for improving performance
# REQUIRED: Return list of recommendations
def develop_recommendations():
    """
    Develop actionable recommendations based on the analysis
    REQUIRED: Return list of at least 5 recommendation strings
    """
    recommendations = [
        "Increase marketing investment in high-performing stores like Miami and Tampa to further accelerate growth.",
        "Expand high-margin departments such as Produce and Prepared Foods in stores with available square footage.",
        "Improve operational efficiency in lower-performing stores by optimizing staffing levels and inventory turnover.",
        "Target high-value customer segments (Family Shoppers, Gourmet Cooks) with loyalty programs and personalized offers.",
        "Leverage strong weekend and seasonal demand with focused promotions and in-store events.",
        "Use predictive sales models to guide capital investments and resource allocation across stores.",
        "Monitor customer satisfaction closely and invest in training to sustain high service levels."
    ]
    return recommendations


# 5: Summary Report
# REQUIRED: Generate comprehensive summary
def generate_executive_summary():
    """
    Generate an executive summary of key findings and recommendations
    REQUIRED: Print executive summary with sections:
    - Overview (1 paragraph)
    - Key Findings (3-5 bullet points)
    - Recommendations (3-5 bullet points)
    - Expected Impact (1 paragraph)
    """
    print("\nEXECUTIVE SUMMARY")
    print("=" * 60)

    print("\nOverview:")
    print("GreenGrocer’s 2023 analysis shows strong performance in several core stores and departments, "
          "with clear opportunities to improve efficiency and deepen relationships with high-value customer segments. "
          "Sales patterns reveal meaningful seasonal and weekly trends that can be leveraged through targeted promotions "
          "and strategic resource allocation.")

    print("\nKey Findings:")
    print("- Miami and Tampa generate the highest annual sales and profit, supported by strong operational metrics.")
    print("- Produce and Prepared Foods are among the most profitable and fastest-growing departments.")
    print("- Family Shoppers and Gourmet Cooks exhibit the highest average monthly spend and loyalty tiers.")
    print("- Weekend and summer periods show elevated sales, indicating strong seasonal and timing effects.")
    print("- Store performance is strongly associated with SalesPerSqFt and CustomerSatisfaction metrics.")

    print("\nRecommendations:")
    print("- Invest additional marketing and staffing resources in high-growth, high-potential stores.")
    print("- Expand high-margin departments and refine product assortments based on departmental trends.")
    print("- Enhance loyalty and personalization efforts for top-spending customer segments.")
    print("- Design promotions around weekends and peak seasonal periods to maximize revenue.")
    print("- Use predictive modeling and correlation insights to guide long-term strategic decisions.")

    print("\nExpected Impact:")
    print("Implementing these recommendations is expected to increase overall profitability, improve operational efficiency, "
          "and strengthen customer loyalty across all GreenGrocer locations. By focusing on high-impact stores, departments, "
          "and customer segments, GreenGrocer can achieve sustainable growth and reinforce its competitive position in the "
          "organic grocery market.")


# ---------------------------------------------------------
# MAIN FUNCTION
# ---------------------------------------------------------

def main():
    print("\n" + "=" * 60)
    print("GREENGROCER BUSINESS ANALYTICS RESULTS")
    print("=" * 60)

    print("\n--- DESCRIPTIVE ANALYTICS: CURRENT PERFORMANCE ---")
    sales_metrics = analyze_sales_performance()
    dist_figs = visualize_sales_distribution()
    customer_analysis = analyze_customer_segments()

    print("\n--- DIAGNOSTIC ANALYTICS: UNDERSTANDING RELATIONSHIPS ---")
    correlations = analyze_sales_correlations()
    store_comparison = compare_store_performance()
    seasonality = analyze_seasonal_patterns()

    print("\n--- PREDICTIVE ANALYTICS: FORECASTING ---")
    sales_model = predict_store_sales()
    dept_forecast = forecast_department_sales()

    print("\n--- BUSINESS INSIGHTS AND RECOMMENDATIONS ---")
    opportunities = identify_profit_opportunities()
    recommendations = develop_recommendations()

    print("\n--- EXECUTIVE SUMMARY ---")
    generate_executive_summary()

    plt.show()

    return {
        'sales_metrics': sales_metrics,
        'customer_analysis': customer_analysis,
        'correlations': correlations,
        'store_comparison': store_comparison,
        'seasonality': seasonality,
        'sales_model': sales_model,
        'dept_forecast': dept_forecast,
        'opportunities': opportunities,
        'recommendations': recommendations
    }

if __name__ == "__main__":
    results = main()
