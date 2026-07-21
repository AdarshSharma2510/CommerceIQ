# CommerceIQ — E-Commerce Sales Analytics & Predictive Insights

> An end-to-end data analytics and machine learning project built to transform raw e-commerce transaction data into actionable business insights using Python, SQL, Machine Learning, and Power BI.

---

## 📌 Project Overview

**CommerceIQ** is an end-to-end e-commerce analytics project that combines data engineering fundamentals, exploratory data analysis, SQL-based business analysis, customer segmentation, predictive machine learning, and interactive business intelligence dashboards.

The project was developed to analyze the complete e-commerce business lifecycle — from customer purchasing behavior and product performance to revenue generation and delivery operations.

The primary objective was to move beyond simply analyzing datasets and build a complete analytical workflow capable of answering real-world business questions.

The project focuses on answering questions such as:

- How much revenue is the business generating?
- How does revenue change over time?
- Which product categories generate the most revenue?
- Which payment methods are most commonly used?
- How many unique customers does the business have?
- What percentage of customers make repeat purchases?
- Which customers are the most valuable?
- Which customers are becoming inactive?
- Can customers be segmented based on purchasing behavior?
- Which product categories experience longer delivery times?
- Which geographic regions experience slower delivery?
- How many orders are delayed?
- Can delivery delays be predicted using machine learning?

---

## 🔄 End-to-End Project Workflow

    Raw E-Commerce Datasets
              │
              ▼
    Data Loading & Inspection
              │
              ▼
    Data Cleaning & Integration
              │
              ▼
    Feature Engineering
              │
              ▼
    Exploratory Data Analysis
              │
              ▼
    SQL Business Analysis
              │
              ▼
    RFM Customer Analysis
              │
              ▼
    K-Means Customer Segmentation
              │
              ▼
    Random Forest Delay Prediction
              │
              ▼
    Power BI Dashboard
              │
              ▼
    Business Insights

---

## 🚀 Key Project Highlights

- Processed and integrated multiple relational e-commerce datasets.
- Worked with approximately **99,000 orders** and over **112,000 order-item records**.
- Built a complete data cleaning and preprocessing pipeline using Python and Pandas.
- Aggregated order items, payment records, and review data before integration to prevent duplication and inflated business metrics.
- Performed exploratory data analysis using Pandas, Matplotlib, and Seaborn.
- Conducted SQL-based analysis to answer revenue, customer, product, and logistics-related business questions.
- Performed customer-level RFM analysis using Recency, Frequency, and Monetary Value.
- Applied K-Means clustering to segment customers according to purchasing behavior.
- Built a Random Forest classification model to predict delivery delays.
- Achieved approximately **98.14% accuracy** and **0.9961 ROC-AUC** on the delivery delay prediction task.
- Built a four-page interactive Power BI dashboard covering executive performance, sales, customer behavior, and logistics.
- Translated machine learning outputs into business-friendly customer segments and actionable insights.

---

## 🛠️ Technology Stack

### Programming & Data Analysis

- Python
- Pandas
- NumPy

### Data Visualization

- Matplotlib
- Seaborn

### Database & Querying

- SQL

### Machine Learning

- Scikit-Learn
- K-Means Clustering
- Random Forest Classifier
- RFM Analysis

### Business Intelligence

- Microsoft Power BI

### Development Tools

- VS Code
- Jupyter Notebook
- Git
- GitHub
- Python Virtual Environment

---

# 📊 Dataset

The project uses a multi-table e-commerce dataset containing information related to customers, orders, products, payments, reviews, sellers, and logistics.

The dataset was treated as a relational business database consisting of multiple connected entities.

### Dataset Components

| Dataset | Description |
|---|---|
| Customers | Customer identifiers and geographic information |
| Orders | Order lifecycle, status, purchase timestamps, and delivery timestamps |
| Order Items | Products purchased, sellers, prices, and freight values |
| Payments | Payment methods, payment values, and installment information |
| Products | Product attributes and product categories |
| Reviews | Customer review scores and review information |
| Sellers | Seller identifiers and geographic information |
| Translation | Product category translations |

---

## 📈 Dataset Scale

The following datasets were processed:

| Dataset | Rows |
|---|---:|
| Customers | 99,441 |
| Orders | 99,441 |
| Order Items | 112,650 |
| Payments | 103,886 |
| Products | 32,951 |
| Reviews | 99,224 |
| Sellers | 3,095 |
| Translations | 71 |

After cleaning, aggregation, and integration:

**Final Dataset Shape:** 99,441 rows × 22 columns

**Duplicate Rows Removed:** 0

The cleaned dataset was exported to:

`data/processed/ecommerce_cleaned.csv`

---

# 🗂️ Project Structure

    CommerceIQ/
    │
    ├── data/
    │   │
    │   ├── raw/
    │   │   ├── customers.csv
    │   │   ├── orders.csv
    │   │   ├── order_items.csv
    │   │   ├── payments.csv
    │   │   ├── products.csv
    │   │   ├── reviews.csv
    │   │   ├── sellers.csv
    │   │   └── product_category_name_translation.csv
    │   │
    │   └── processed/
    │       ├── ecommerce_cleaned.csv
    │       └── customer_segments.csv
    │
    ├── images/
    │   └── eda/
    │       ├── sales/
    │       ├── customers/
    │       ├── products/
    │       ├── logistics/
    │       └── correlations/
    │
    ├── models/
    │   └── delivery_delay_model.pkl
    │
    ├── notebooks/
    │   └── exploratory_analysis.ipynb
    │
    ├── sql/
    │   └── analysis.sql
    │
    ├── src/
    │   ├── data/
    │   │   └── data_cleaning.py
    │   │
    │   ├── analysis/
    │   │   └── eda.py
    │   │
    │   └── ml/
    │       ├── customer_segmentation.py
    │       └── delivery_delay_prediction.py
    │
    ├── requirements.txt
    ├── .gitignore
    └── README.md

---

# 1️⃣ Data Loading and Inspection

The project begins by loading all raw datasets into Pandas DataFrames.

Each dataset was inspected for:

- Number of rows and columns
- Data types
- Missing values
- Duplicate records
- Unique identifiers
- Relationships between tables
- Data granularity

The initial dataset loading process produced:

    customers       (99441, 5)
    orders          (99441, 8)
    order_items     (112650, 7)
    payments        (103886, 5)
    products        (32951, 9)
    reviews         (99224, 7)
    sellers         (3095, 4)
    translation     (71, 2)

All datasets were successfully loaded and prepared for cleaning.

---

# 2️⃣ Data Cleaning and Integration

The raw datasets existed at different levels of granularity.

For example:

    One Customer
         │
         ├── Multiple Orders
         │       │
         │       ├── Multiple Order Items
         │       │
         │       ├── Multiple Payments
         │       │
         │       └── Reviews
         │
         └── Customer Information

Directly joining all datasets together could create duplicate rows and inflate metrics such as revenue, order value, or payment totals.

To avoid this problem, lower-level data was aggregated before being merged into the main order-level dataset.

---

## 🧹 Datetime Processing

Relevant date columns were converted to proper datetime formats.

This enabled the creation of:

- Purchase year
- Purchase month
- Purchase quarter
- Actual delivery duration
- Delivery delay

---

## 📦 Order Item Aggregation

A single order can contain multiple products.

Order item data was aggregated to the order level to calculate:

- Total order value
- Number of items in an order
- Total freight value
- Product-level information

---

## 💳 Payment Aggregation

An order can contain multiple payment records.

Payment data was aggregated to prevent duplicated order-level records and to calculate:

- Total payment value
- Payment method information
- Installment information

---

## ⭐ Review Aggregation

Review information was aggregated and connected with order-level data.

This allowed analysis of:

- Average review score
- Customer satisfaction
- Review behavior

---

## ✅ Final Cleaned Dataset

The data cleaning and integration pipeline produced:

- Converted datetime columns
- Aggregated order items
- Aggregated payments
- Aggregated reviews
- Final merged shape: **99,441 rows × 22 columns**
- Duplicate rows removed: **0**

The cleaned dataset was saved to:

`data/processed/ecommerce_cleaned.csv`

---

# 3️⃣ Feature Engineering

Feature engineering was performed to create analytical features for business analysis and machine learning.

---

## 📅 Time-Based Features

The following features were extracted from date columns:

- `purchase_year`
- `purchase_month`
- `purchase_quarter`

These features were used to analyze:

- Monthly revenue
- Monthly order volume
- Quarterly performance
- Seasonal patterns

---

## 💰 Revenue Features

Order-level financial features were created to support:

- Total revenue analysis
- Average Order Value calculation
- Customer monetary value calculation
- Product category performance analysis

The primary revenue metric was:

`total_order_value`

---

## 🚚 Delivery Features

The following delivery-related features were created:

- `delivery_days`
- `delivery_delay`
- `is_delayed`

These features supported both logistics analysis and delivery delay prediction.

---

## 👤 Customer Features

Customer-level analysis was performed using:

`customer_unique_id`

This allowed multiple orders belonging to the same real customer to be grouped together.

---

# 4️⃣ Exploratory Data Analysis

Exploratory Data Analysis was performed before machine learning to understand the underlying business patterns in the data.

The analysis covered:

- Revenue trends
- Order volume
- Product categories
- Customer behavior
- Payment methods
- Review scores
- Delivery performance
- Geographic patterns
- Numerical feature correlations

Visualizations were created using:

- Pandas
- Matplotlib
- Seaborn

The generated visualizations were saved to:

`images/eda/`

---

# 📌 Executive Business Metrics

The analysis generated the following high-level metrics:

- **Total Revenue:** $15,924,207.49
- **Total Orders:** 99,441
- **Unique Customers:** 96,096
- **Average Order Value:** $160.14
- **Average Review Score:** 4.09

These metrics provide a high-level overview of the overall business performance.

---

# 📈 Sales Analysis

The sales analysis focused on:

- Monthly revenue trends
- Order volume
- Average Order Value
- Product category revenue
- Payment method usage
- Quarterly sales performance

The analysis identified changes in revenue and order activity over time and helped identify the strongest-performing product categories.

---

# 👥 Customer Analysis

Customer analysis focused on:

- Number of unique customers
- Purchase frequency
- Customer spending
- Customer recency
- Repeat purchase behavior

A major observation from the data was that a significant portion of customers had a purchase frequency close to one.

This indicates a large one-time customer population and highlights potential opportunities for:

- Customer retention
- Repeat purchase strategies
- Re-engagement campaigns
- Loyalty programs

---

# 🛍️ Product Analysis

Product-level analysis examined:

- Revenue by product category
- Order volume by category
- Category performance
- Customer demand

This analysis helped identify the product categories contributing most significantly to business revenue and order volume.

---

# 🚚 Logistics Analysis

The logistics analysis focused on:

- Actual delivery time
- Delivery delays
- Delayed order volume
- Delivery performance by product category
- Geographic differences in delivery time

An important distinction was made between actual delivery time and delivery delay.

### Actual Delivery Time

Measures how long the customer actually waited:

`Actual Delivery Date - Purchase Date`

### Delivery Delay

Measures whether the order arrived later or earlier than the estimated delivery date:

`Actual Delivery Date - Estimated Delivery Date`

These metrics measure different aspects of the customer experience.

For example:

- Estimated Delivery: 100 days
- Actual Delivery: 90 days
- Delivery Delay: -10 days

The order arrived 10 days early relative to the estimate. However, the customer still waited 90 days.

Therefore, a negative delivery delay does not necessarily mean that the delivery process was efficient.

The project separates:

- Actual delivery time
- Delivery delay
- Delay rate

to provide a more meaningful analysis of logistics performance.

---

# 5️⃣ SQL Business Analysis

SQL was used to perform structured business analysis on the cleaned dataset.

The SQL analysis was designed to answer business questions such as:

- Which product categories generate the most revenue?
- What is the monthly revenue trend?
- Which payment methods are most commonly used?
- Which states generate the highest revenue?
- Which product categories have the highest average review scores?
- Which sellers generate the most revenue?

Example business analysis:

    SELECT
        main_category,
        SUM(total_order_value) AS total_revenue
    FROM ecommerce_cleaned
    GROUP BY main_category
    ORDER BY total_revenue DESC;

SQL complements the Python analysis by demonstrating the ability to query and analyze structured business data using database-oriented techniques.

---

# 6️⃣ Customer Segmentation Using RFM Analysis

Customer segmentation was performed using the RFM framework.

RFM analysis evaluates customers based on:

- Recency
- Frequency
- Monetary Value

---

## 🕒 Recency

Recency measures how recently a customer made a purchase.

- Lower recency value = more recent purchase
- Higher recency value = longer time since last purchase

---

## 🔁 Frequency

Frequency measures how often a customer makes purchases.

- Higher frequency = more repeat purchases
- Lower frequency = fewer purchases

---

## 💰 Monetary Value

Monetary value measures how much a customer has spent.

- Higher monetary value = higher customer value

---

## RFM Table

A customer-level RFM table was created with:

- `customer_unique_id`
- `Recency`
- `Frequency`
- `Monetary`

Example:

| Customer | Recency | Frequency | Monetary |
|---|---:|---:|---:|
| Customer A | 161 | 1 | $141.90 |
| Customer B | 164 | 1 | $27.19 |
| Customer C | 586 | 1 | $86.22 |

This transformed order-level transactional data into customer-level behavioral data.

---

# 7️⃣ K-Means Customer Segmentation

K-Means clustering was applied to the RFM features:

- Recency
- Frequency
- Monetary

The model grouped customers with similar purchasing behaviors into four clusters.

---

## Cluster Summary

| Cluster | Customers | Avg Recency | Avg Frequency | Avg Monetary |
|---|---:|---:|---:|---:|
| 0 | 52,037 | 178.37 | 1.00 | $134.63 |
| 1 | 2,963 | 269.24 | 2.12 | $289.59 |
| 2 | 38,633 | 438.82 | 1.00 | $133.83 |
| 3 | 2,463 | 289.75 | 1.02 | $1,173.57 |

---

# 👥 Customer Segment Interpretation

K-Means produces numerical cluster labels, but the numbers themselves do not have business meaning.

For example:

- Cluster 0
- Cluster 1
- Cluster 2
- Cluster 3

does not mean that Cluster 3 is automatically better than Cluster 0.

The business interpretation was created by analyzing the RFM characteristics of each group.

---

## 🟢 Recent Buyers

Characteristics:

- Lower recency values
- Mostly one purchase
- Moderate monetary value

These customers have purchased relatively recently but have not yet demonstrated strong repeat-purchase behavior.

---

## 🔵 Loyal Customers

Characteristics:

- Higher purchase frequency
- Higher monetary value
- More repeat purchases

These customers demonstrate stronger engagement and repeat purchasing behavior.

---

## 🟠 At-Risk Customers

Characteristics:

- High recency
- Low frequency
- Moderate monetary value

These customers have not purchased recently and generally have limited purchase history.

The large size of this segment is an important business insight.

It indicates that a significant portion of the customer base may not return after their initial purchase.

Potential strategies include:

- Re-engagement campaigns
- Personalized discounts
- Product recommendations
- Loyalty incentives

---

## 🟣 High-Value Customers

Characteristics:

- Extremely high monetary value
- Relatively small customer population

These customers generate significantly higher revenue per customer.

Potential strategies include:

- VIP loyalty programs
- Personalized offers
- Premium customer support
- Customer retention campaigns

---

# 8️⃣ Delivery Delay Prediction

A supervised machine learning model was developed to predict whether an order would experience a delivery delay.

The target variable was:

`is_delayed`

The classification problem was:

- `0` → Not Delayed
- `1` → Delayed

---

# 🌲 Random Forest Classifier

The selected model was:

`RandomForestClassifier`

Random Forest was chosen because it:

- Handles nonlinear relationships
- Works effectively with tabular data
- Captures feature interactions
- Is relatively robust to noise
- Provides feature importance information

---

# 📊 Model Performance

The model achieved:

- **Accuracy:** 0.9814
- **ROC-AUC:** 0.9961

Classification Report:

| Class | Precision | Recall | F1-Score | Support |
|---|---:|---:|---:|---:|
| 0 | 0.98 | 1.00 | 0.99 | 18,427 |
| 1 | 0.99 | 0.76 | 0.86 | 1,462 |

Overall:

- **Accuracy:** 0.98
- **Macro F1-score:** 0.92
- **Weighted F1-score:** 0.98

---

# 📐 Model Evaluation

Accuracy was not used as the only evaluation metric.

The model was evaluated using:

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC

This was important because the dataset contained significantly more non-delayed orders than delayed orders.

The model achieved strong performance for identifying non-delayed orders.

However, the recall for delayed orders was lower than the recall for non-delayed orders.

This demonstrates an important machine learning concept:

> A model can achieve high overall accuracy while still missing a meaningful number of examples from a minority class.

Therefore, multiple classification metrics were considered.

---

# 💾 Model Output

The trained model was saved to:

`models/delivery_delay_model.pkl`

The prediction results were integrated into the analytical dataset using:

`is_delayed`

This allowed machine learning outputs to be used in the Power BI logistics analysis.

---

# 9️⃣ Power BI Dashboard

The final project includes a four-page interactive Power BI dashboard.

---

# 📊 Page 1 — Executive Overview

The Executive Overview page provides a high-level summary of business performance.

### KPI Cards

- Total Revenue
- Total Orders
- Average Order Value
- Average Review Score

### Visualizations

- Monthly Revenue Trend
- Revenue by Product Category
- Orders by Payment Method
- Quarterly Revenue Performance

This page is designed for quickly understanding the overall performance of the business.

---

# 📈 Page 2 — Sales Performance

The Sales Performance page focuses on revenue and order behavior.

### Key Metrics

- Total Revenue
- Total Orders
- Average Order Value

### Visualizations

- Monthly Order Volume
- Average Order Value Trend
- Revenue by Product Category
- Revenue by Payment Method

This page helps analyze:

- Revenue trends
- Seasonal patterns
- Product category performance
- Payment behavior
- Changes in customer spending

---

# 👥 Page 3 — Customer Insights

The Customer Insights page combines customer analytics and machine learning outputs.

### Key Metrics

- Total Customers
- Average Customer Spend
- Average Review Score

### Visualizations

- Customer Segment Distribution
- Average Customer Value by Segment
- Average Recency by Segment
- Average Purchase Frequency by Segment

This page translates the output of K-Means clustering into understandable customer segments.

---

# 🚚 Page 4 — Logistics & Delivery

The Logistics & Delivery page focuses on operational performance.

### Key Metrics

- Total Orders
- Delayed Orders
- Delay Rate
- Average Delivery Time

### Visualizations

- On-Time vs Delayed Orders
- Average Delivery Time by Product Category
- Delayed Orders by Product Category
- Average Delivery Time by State

This page provides insight into:

- Actual delivery performance
- Delay frequency
- Product category logistics
- Geographic delivery differences

---

# 💡 Key Business Insights

## 1. A Large Portion of Customers Are One-Time Buyers

A large proportion of customers have a purchase frequency close to one.

This indicates a significant opportunity to improve:

- Customer retention
- Repeat purchase rates
- Loyalty programs
- Re-engagement campaigns

---

## 2. A Significant Customer Segment Is Inactive

The At-Risk segment is characterized by:

- High recency
- Low frequency
- Moderate monetary value

This group represents a potential opportunity for targeted reactivation campaigns.

---

## 3. A Small Group of Customers Generates Very High Value

The High-Value customer segment is relatively small but has significantly higher monetary value.

This demonstrates that customer value is not evenly distributed across the customer base.

---

## 4. Repeat Customers Are More Valuable

Customers with higher purchase frequency demonstrate stronger customer value.

This highlights the importance of retention and repeat-purchase strategies.

---

## 5. Delivery Performance Varies by Product Category

Different product categories demonstrate differences in:

- Actual delivery time
- Number of delayed orders

This may indicate differences in:

- Seller performance
- Supply chain requirements
- Product handling
- Logistics complexity

---

## 6. Delivery Performance Varies Across Geographic Regions

Average delivery time varies across customer states.

Potential factors include:

- Geographic distance
- Logistics infrastructure
- Seller location
- Regional transportation networks

---

# 🧠 Important Analytical Considerations

## Customer Segmentation Is Unsupervised

K-Means does not automatically understand labels such as:

- Loyal Customer
- At-Risk Customer
- High-Value Customer

The algorithm only identifies groups of similar observations.

The business interpretation was created by analyzing the RFM profiles of each cluster.

---

## Cluster Numbers Are Arbitrary

The following:

- Cluster 0
- Cluster 1
- Cluster 2
- Cluster 3

are simply identifiers.

The cluster number does not indicate:

- Importance
- Ranking
- Quality
- Customer value

The characteristics of each cluster determine its business meaning.

---

## Accuracy Should Not Be Used Alone

The delivery delay problem contains an imbalance between delayed and non-delayed orders.

Therefore, accuracy alone can provide an incomplete picture of model performance.

Precision, recall, F1-score, and ROC-AUC were also evaluated.

---

## Delivery Delay and Delivery Time Are Different Metrics

An order can arrive early relative to its estimated delivery date while still taking a long time to reach the customer.

For example:

- Estimated Delivery: 100 days
- Actual Delivery: 90 days
- Delivery Delay: -10 days

The order arrived early relative to the estimate, but the customer still waited 90 days.

Therefore:

- Actual Delivery Time
- Delivery Delay

measure different aspects of logistics performance.

The project therefore separates:

- Actual delivery time
- Delivery delay
- Delay rate
- Delayed order volume

---

# ⚙️ Technical Challenges

## Challenge 1: Multiple Data Granularities

The datasets existed at different levels:

    Customer Level
         ↓
    Order Level
         ↓
    Order Item Level
         ↓
    Payment Level
         ↓
    Review Level

Joining these datasets directly could result in duplicate records and inflated metrics.

The solution was to aggregate lower-level datasets before integrating them into the main analytical dataset.

---

## Challenge 2: Multiple Records Per Order

An order can contain:

- Multiple products
- Multiple payments
- Multiple review records

These relationships were handled through aggregation before merging.

---

## Challenge 3: Translating Machine Learning Results into Business Insights

K-Means produces numerical cluster labels.

The challenge was to transform those numerical clusters into meaningful business segments.

This was achieved by analyzing:

- Recency
- Frequency
- Monetary Value

for each cluster.

---

## Challenge 4: Imbalanced Classification

The delivery delay problem contained more non-delayed orders than delayed orders.

Therefore, the model was evaluated using multiple classification metrics rather than relying only on accuracy.

---

# 📚 What I Learned

Through this project, I worked through the complete data analytics lifecycle:

    Business Problem
          ↓
    Data Loading
          ↓
    Data Cleaning
          ↓
    Data Integration
          ↓
    Feature Engineering
          ↓
    Exploratory Data Analysis
          ↓
    SQL Analysis
          ↓
    Machine Learning
          ↓
    Model Evaluation
          ↓
    Business Intelligence
          ↓
    Actionable Insights

The project strengthened my practical understanding of:

- Data cleaning
- Data integration
- Data transformation
- Exploratory data analysis
- SQL-based business analysis
- Feature engineering
- RFM analysis
- Customer segmentation
- K-Means clustering
- Classification modeling
- Model evaluation
- Power BI dashboard development
- Data visualization
- Business intelligence
- Translating technical results into business insights

---

# 🔮 Future Improvements

Potential improvements for future versions include:

## Customer Lifetime Value Prediction

Predict future customer value using:

- Historical spending
- Purchase frequency
- Recency
- Customer tenure

---

## Advanced Customer Segmentation

Experiment with:

- Hierarchical Clustering
- DBSCAN
- Gaussian Mixture Models

---

## Improved Delivery Prediction

Compare Random Forest with:

- Gradient Boosting
- XGBoost
- LightGBM

---

## Hyperparameter Optimization

Improve model performance using:

- GridSearchCV
- RandomizedSearchCV
- Bayesian Optimization

---

## Explainable Machine Learning

Use:

- SHAP
- Permutation Importance

to understand which factors influence delivery delay predictions.

---

## Automated Analytics Pipeline

The project could be extended into an automated workflow:

    New Data
        ↓
    Data Cleaning
        ↓
    Feature Engineering
        ↓
    Model Prediction
        ↓
    Updated Dataset
        ↓
    Power BI Refresh

---

# ▶️ How to Run the Project

## Clone the Repository

    git clone <YOUR_REPOSITORY_URL>
    cd CommerceIQ

## Create a Virtual Environment

    python -m venv .venv

Activate the environment on Windows:

    .venv\Scripts\activate

## Install Dependencies

    pip install -r requirements.txt

## Run the Data Cleaning Pipeline

The data cleaning pipeline:

- Loads the raw datasets
- Converts data types
- Aggregates order items
- Aggregates payment data
- Aggregates review data
- Merges the datasets
- Generates the cleaned analytical dataset

Output:

`data/processed/ecommerce_cleaned.csv`

## Run Exploratory Data Analysis

The EDA pipeline generates visualizations covering:

- Sales
- Customers
- Products
- Logistics
- Correlations

Output:

`images/eda/`

## Run Customer Segmentation

The segmentation workflow is:

    Customer Transactions
            ↓
        RFM Table
            ↓
    Feature Preparation
            ↓
    K-Means Clustering
            ↓
    Customer Segments

Output:

`data/processed/customer_segments.csv`

## Run Delivery Delay Prediction

The machine learning workflow is:

    Prepared Dataset
            ↓
    Feature Selection
            ↓
    Train/Test Split
            ↓
    Random Forest Training
            ↓
    Model Evaluation
            ↓
    Model Export

Output:

`models/delivery_delay_model.pkl`

## Open the Power BI Dashboard

Open the Power BI report file and connect it to the processed datasets.

The report contains:

- Page 1 — Executive Overview
- Page 2 — Sales Performance
- Page 3 — Customer Insights
- Page 4 — Logistics & Delivery

---

# 🏁 Project Outcome

CommerceIQ demonstrates how raw, multi-table e-commerce data can be transformed into a complete analytical solution.

The project combines:

- Data Cleaning
- Exploratory Data Analysis
- SQL
- RFM Analysis
- K-Means Clustering
- Random Forest Classification
- Power BI

The final outcome is an end-to-end analytics project that:

1. Cleans and integrates raw transactional data.
2. Identifies business patterns through exploratory analysis.
3. Answers business questions using SQL.
4. Segments customers using unsupervised machine learning.
5. Predicts delivery delays using supervised machine learning.
6. Communicates findings through interactive Power BI dashboards.

The project demonstrates the complete journey from:

> **Raw Data → Analysis → Machine Learning → Business Intelligence → Actionable Insights**

---

## 👨‍💻 Author

**Adarsh Sharma**

Data Analytics | Python | SQL | Machine Learning | Power BI