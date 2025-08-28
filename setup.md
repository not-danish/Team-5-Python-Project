# Setup Instruction

## 1. Project Overview

In this project, generally, the aim is to provide one platform which can help users to match their favorite Airbnb places with given conditions, including budget, location, group size, preferred environment, and preferred features. Based on the given information, the platform will provide the best 5 results based on the different conditions with weighted consideration. 

## 2. Prerequisites

### 2.1 Python and Dependencies
-[Python 3.9 or later]
-[Pandas]
-[Numpy]

### 2.2 Recommendation tools
-[Jupyter Notebook or Visual Studio Code]
-[Github (for installation)]
-[Virtualenv for environment management]

## 3. Installation

### 3.1 Clone the repository
git clone https://github.com/not-danish/Team-5-Python-Project
cd property-matching

### 3.2 Create a virtual environment
python -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows

### 3.3 Install dependencies
pip install -r requirements.txt

## 4. Running the Project

```python
import pandas as pd
from match import match_step   # your function file

# Load property & user JSON
property_df = pd.read_json("property_data.json")["data"].apply(pd.Series)
import json
with open("user_data.json") as f:
    user_json = json.load(f)

# Run matching
results = match_step(property_df, user_json)

print(results[["City","Type","Nightly price","match_score"]].head())
 ```

## 5. Customization

For the customized utilization of this application, one useful aspect is always considered: **Scoring Weighted System**.

The Scoring Weighted System mainly refers the part for measuring how much the property matched with users' condition, and in the part, the default system consider for the budget, preferred type, features, cancellation policy, and the preferred environment. In the default system, the weights for each parts are: 0.1 for environment match, 0.1 for type match, 0.1 for cancellation policy, 0.4 for budget percentage, and 0.3 for features match. To customize the diffenert weights which can help user to priortize the result by their preferences, the effective way is to operate in **Step 3**, and the following is one example:

The original code is:

```python
### Step3
class PropertyRecommender:
    def __init__(self, dataset_path="/Users/yoyoyue/Desktop/properties_updated.json"):
        # Insert the csv file
        self.df = pd.read_json("properties_updated.json")

    def compute_fit_score(self, profile, property_row):
        """
        Compute fit score for a single property.
        profile: dict
        property_row: pandas.Series
        """
        score = 0

        # 1. preferred_environment (Weight 0.1, full score 10)
        W_ENV = 0.1
        env_value = str(property_row.data["Environment"]).lower()
        env_score = (10 * W_ENV) if profile["preferred_environment"].lower() == env_value else 0
        
        # 2. preferred_type (Weight 0.1, full score 10)
        W_TYPE = 0.1
        type_value = str(property_row.data["Type"]).lower()
        type_score = (10 * W_TYPE) if profile["preferred_type"].lower() == type_value else 0

        # 3. cancellation_policy (Weight 0.1, full score 10)
        W_CANCELLATION = 0.1
        cancellation_policy = str(property_row.data["Cancellation_policy"]).lower()
        cancel_score = (10 * W_CANCELLATION) if cancellation_policy in ["flexible", "moderate"] else 0

        # 4. Budget
        W_BUDGET = 0.4
        price_of_property = int(property_row.data["Nightly price"])
        user_budget = int(profile["budget"])
        budget_score = (((user_budget - price_of_property)/user_budget) * 10 ) * W_BUDGET

        # 5. Features
        W_FEATURES  = 0.3
        must_have_features = [f.strip().lower() for f in profile.get("Must_have_features",[]) if f.strip()]
        property_features = str(property_row.data["features"]).lower().split(",")
        property_features = [f.strip() for f in property_features]

        if must_have_features:
            matched = sum(1 for feature in must_have_features if feature in property_features)
            feat_score = (10 * (matched / len(must_have_features))) * W_FEATURES

        score = env_score + type_score + cancel_score + budget_score + feat_score

        return round(score,2)
```

For users who only focuses one the type who do not matter environment, budget, features, and the features, the new code will be:

```python
### Step3
class PropertyRecommender:
    def __init__(self, dataset_path="/Users/yoyoyue/Desktop/properties_updated.json"):
        # Insert the csv file
        self.df = pd.read_json("properties_updated.json")

    def compute_fit_score(self, profile, property_row):
        """
        Compute fit score for a single property.
        profile: dict
        property_row: pandas.Series
        """
        score = 0

        # 1. preferred_environment (Weight 0.1, full score 10)
        W_ENV = 0
        env_value = str(property_row.data["Environment"]).lower()
        env_score = (10 * W_ENV) if profile["preferred_environment"].lower() == env_value else 0
        
        # 2. preferred_type (Weight 0.1, full score 10)
        W_TYPE = 1
        type_value = str(property_row.data["Type"]).lower()
        type_score = (10 * W_TYPE) if profile["preferred_type"].lower() == type_value else 0

        # 3. cancellation_policy (Weight 0.1, full score 10)
        W_CANCELLATION = 0
        cancellation_policy = str(property_row.data["Cancellation_policy"]).lower()
        cancel_score = (10 * W_CANCELLATION) if cancellation_policy in ["flexible", "moderate"] else 0

        # 4. Budget
        W_BUDGET = 0
        price_of_property = int(property_row.data["Nightly price"])
        user_budget = int(profile["budget"])
        budget_score = (((user_budget - price_of_property)/user_budget) * 10 ) * W_BUDGET

        # 5. Features
        W_FEATURES  = 0
        must_have_features = [f.strip().lower() for f in profile.get("Must_have_features",[]) if f.strip()]
        property_features = str(property_row.data["features"]).lower().split(",")
        property_features = [f.strip() for f in property_features]

        if must_have_features:
            matched = sum(1 for feature in must_have_features if feature in property_features)
            feat_score = (10 * (matched / len(must_have_features))) * W_FEATURES

        score = env_score + type_score + cancel_score + budget_score + feat_score

        return round(score,2)

```

By this way, it can serve for users with their condition preference.
