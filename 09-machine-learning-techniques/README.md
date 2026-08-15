# Machine Learning Techniques

Three university coursework projects applying machine learning across neural networks, regression, and clustering — covering model selection, hyperparameter tuning, and translating technical output into business recommendations.

**Note:** This page consolidates coursework from two units (a Data Science unit, and BUSA8001 – Applied Predictive Analytics) rather than standing as a single end-to-end project. It's presented here to showcase breadth across ML techniques rather than as a standalone production build.

## Overview

Three applied ML projects completed as part of coursework: a neural network classification problem identifying manuscript scribes from handwriting features, a regression problem forecasting used car prices in a class-wide Kaggle competition, and an unsupervised customer segmentation analysis for a supermarket chain. Together they span neural network architecture tuning, supervised regression, and unsupervised clustering — with model comparison and statistical validation running through all three.

## Part 1: Neural Network Classification (Data Science unit)

**Problem:** Classify medieval manuscript scribes from the Avila dataset using handwriting-derived features.

**Approach:**
- MLPClassifier (neural network) with systematic tuning across:
  - Number of hidden layers and hidden layer sizes
  - Solvers (lbfgs, sgd, adam)
  - Activation functions
  - Regularization (alpha)
  - Iteration counts
- 10-fold cross-validation throughout

**Result:** Default single-hidden-layer MLP achieved 77.4% mean cross-validated accuracy. Adding a second hidden layer (100×100) improved mean accuracy to 88.7% — a statistically significant improvement (t=-28.88, p<0.000001). Regularization sweep showed accuracy declining as alpha increased, indicating overfitting was not a significant issue on this dataset.

## Part 2: Used Car Price Prediction (BUSA8001 Kaggle Competition)

**Problem:** Predict used car sale prices as part of a class-wide Kaggle competition, working in a 3-person team.

**My role:** Responsible for Task 3 — model fitting, tuning, and final model selection, building on data cleaning and feature engineering completed by teammates in Task 2.

**Approach:**
- Trained and compared three ensemble regression models: Random Forest, XGBoost, Gradient Boosting Regressor
- Hyperparameter tuning via GridSearchCV
- Model selection based on RMSE

**Result:** Our team, BUSA8001_Data_Wizards, placed **3rd out of all teams** in the class-wide Kaggle competition (final leaderboard, scored against a held-out test set). Gradient Boosting was selected as the best-performing model on training data.

## Part 3: Customer Segmentation (BUSA8001 Programming Task 2)

**Problem:** Segment a supermarket's 4,000 loyalty card customers to inform targeted marketing strategy, using demographic and income data.

**Approach:**
- Standardised numeric features (age, income) with StandardScaler
- Determined optimal cluster count using the Elbow Method and Silhouette Analysis across multiple cluster counts
- Estimated segments using both K-means++ and Agglomerative Clustering, compared via silhouette score
- Profiled each cluster against the full set of demographic variables (gender, marital status, education, settlement size, occupation) and translated findings into segment-specific marketing recommendations for a non-technical audience

**Result:** Identified 3 optimal customer segments (young/low-income, middle-aged/high-income, older/high-income). K-means++ outperformed Agglomerative Clustering on silhouette score and was selected as the primary segmentation method.

**Note:** Clustering itself was performed on 2 standardised numeric variables (age, income); the remaining demographic variables were used to profile and interpret the resulting clusters rather than as direct clustering inputs.

## Tech Stack

- Python
- scikit-learn (MLPClassifier, RandomForestRegressor, GradientBoostingRegressor, KMeans, AgglomerativeClustering, GridSearchCV, StandardScaler)
- XGBoost
- pandas, NumPy
- SciPy (statistical testing)
- Matplotlib, Seaborn

## Skills Demonstrated

**Machine Learning**
- Neural networks: MLPClassifier architecture tuning, solver and activation function comparison
- Regression: ensemble methods (Random Forest, Gradient Boosting, XGBoost), hyperparameter optimisation
- Unsupervised learning: K-means++ and Agglomerative Clustering, cluster validation (Elbow Method, Silhouette Analysis)

**Statistical Validation**
- Cross-validation methodology
- Hypothesis testing (t-tests) to validate model performance differences

**Communication**
- Translating clustering output into segment-specific, non-technical marketing recommendations for a business audience

## Limitations

- All three are coursework assignments on academic/competition datasets, not production systems — no deployment, monitoring, or live data pipeline.
- The used-car pricing project was a group assignment; my individually-owned contribution was model fitting, tuning, and selection (Task 3), building on teammates' data cleaning and feature engineering work.
- Customer segmentation clustering used only 2 of 7 available features as direct clustering inputs.

## Key Takeaway

Applied breadth across the core machine learning toolkit — neural network classification, regression, and clustering — with consistent use of cross-validation, statistical comparison, and (in the Kaggle competition) genuine external validation through a held-out leaderboard result rather than training-set metrics alone.