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

### 3.4 LLM Integration
.env file to be created and the unique Open Router API key to be added in the .env file as below
OPENROUTER_API_KEY=your_unique_openrouter_api_key

## 4. Running the Project

```python
python3 score_my_stay.py
 ```

And here is what will show

```python
-----Score My Stay-----
1. Create Profile
2. View Profile
3. Edit Profile
4. Delete Profile
5. Property Recommendations
6. Exit
```

For these choices,

- 1. Create profile: Input the users' information
- 2. View Profile: Get and view the existing profiles
- 3. Edit Profile: Change some attributes in the existing profile
- 4. Delete Profile: Delete the existing profile
- 5. Property Recommendatioin: See the Airbnb Advice
- 6. Exist: Leave the System 

## 5. Customization

For the customized utilization of this application, one useful aspect is always considered: **Scoring Weighted System**.

The Scoring Weighted System mainly refers the part for measuring how much the property matched with users' condition, and in the part, the default system consider for the budget, preferred type, features, cancellation policy, and the preferred environment. In the default system, the weights for each parts are: 0.1 for environment match, 0.1 for type match, 0.1 for cancellation policy, 0.3 for budget percentage, and 0.4 for features match. To customize the diffenert weights which can help user to priortize the result by their preferences, the effective way is to operate in **Step 3**, and the following is one example:

The original code is:

```python
def compute_fit_score(self, profile, property_row):
        """
        Compute fit score for a single property.
        profile: dict
        property_row: pandas.Series
        """
        score = 0

        # 1. preferred_environment (weight 0.1, out of 1)
        W_ENV = 0.1
        env_value = str(property_row.data["Environment"]).lower()
        env_score = (10 * W_ENV) if profile["preferred_environment"].lower() == env_value else 0
        
        # 2. preferred_type (weight 0.1, out of 1)
        W_TYPE = 0.1
        type_value = str(property_row.data["Type"]).lower()
        type_score = (10 * W_TYPE) if profile["preferred_type"].lower() == type_value else 0

        # 3. cancellation_policy (weight 0.1, out of 1)
        W_CANCELLATION = 0.1
        cancellation_policy = str(property_row.data["Cancellation_policy"]).lower()
        cancel_score = (10 * W_CANCELLATION) if cancellation_policy in ["flexible", "moderate"] else 0

        # 4. Budget (weight 0.3, out of 1)
        W_BUDGET = 0.3
        price_of_property = int(property_row.data["Nightly price"])
        user_budget = int(profile["budget"])
        budget_score = (((user_budget - price_of_property) / user_budget) * 10) * W_BUDGET

        # 5. Features (weight 0.4, out of 1)
        W_FEATURES  = 0.4
        must_have_features = [f.strip().lower() for f in profile.get("Must_have_features",[]) if f.strip()]
        property_features = str(property_row.data["features"]).lower().split(",")
        property_features = [f.strip() for f in property_features]

        if must_have_features:
            matched = sum(1 for feature in must_have_features if feature in property_features)
            feat_score = (10 * (matched / len(must_have_features))) * W_FEATURES

        score = env_score + type_score + cancel_score + budget_score + feat_score

        return round(score,2)
```

For users who only focuses one the type who do not matter environment, budget, features, and the cancellation policy, the new code will be:

```python
def compute_fit_score(self, profile, property_row):
        """
        Compute fit score for a single property.
        profile: dict
        property_row: pandas.Series
        """
        score = 0

        # 1. preferred_environment (weight 0.1, out of 1)
        W_ENV = 0
        env_value = str(property_row.data["Environment"]).lower()
        env_score = (10 * W_ENV) if profile["preferred_environment"].lower() == env_value else 0
        
        # 2. preferred_type (weight 0.1, out of 1)
        W_TYPE = 1
        type_value = str(property_row.data["Type"]).lower()
        type_score = (10 * W_TYPE) if profile["preferred_type"].lower() == type_value else 0

        # 3. cancellation_policy (weight 0.1, out of 1)
        W_CANCELLATION = 0
        cancellation_policy = str(property_row.data["Cancellation_policy"]).lower()
        cancel_score = (10 * W_CANCELLATION) if cancellation_policy in ["flexible", "moderate"] else 0

        # 4. Budget (weight 0.3, out of 1)
        W_BUDGET = 0
        price_of_property = int(property_row.data["Nightly price"])
        user_budget = int(profile["budget"])
        budget_score = (((user_budget - price_of_property) / user_budget) * 10) * W_BUDGET

        # 5. Features (weight 0.4, out of 1)
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
