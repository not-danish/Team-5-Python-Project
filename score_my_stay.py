# This code is adopted from OpenAI's official examples.
# Source: OpenAI (2023) https://github.com/openai/openai-cookbook

import os
import json
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

# ------------------- LLM Query -------------------
def query_openrouter(prompt):
    API_KEY = os.getenv("OPENROUTER_API_KEY")
    if not API_KEY:
        raise ValueError("Please set OPENROUTER_API_KEY in your environment")

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "Summer Home Recommender"
    }
    data = {
        "model": "deepseek/deepseek-r1:free",
        "messages": [{"role": "user", "content": prompt}],
        "stream": True
    }

    try:
        with requests.post(url, headers=headers, json=data, stream=True) as response:
            response.raise_for_status()
            full_response = ""
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode("utf-8")
                    if decoded_line.startswith("data: "):
                        chunk = decoded_line[len("data: "):]
                        if chunk.strip() == "[DONE]":
                            break
                        try:
                            content = json.loads(chunk)
                            delta = content.get("choices", [{}])[0].get("delta", {}).get("content", "")
                            if delta:
                                print(delta, end="", flush=True)
                                full_response += delta
                        except json.JSONDecodeError:
                            continue
            print()
            return full_response if full_response else None

    except requests.exceptions.HTTPError as e:
        print("LLM request failed:", e.response.text)
        return None
    except Exception as e:
        print("Unexpected error:", e)
        return None

# ------------------- User Profile Management -------------------
if not os.path.exists("users.json"):
    with open("users.json", "w") as f:
        json.dump({"data": []}, f, indent=4)

class UserProfileManager:
    def load_profiles(self):
        with open("users.json", "r") as f:
            return json.load(f)

    def get_next_user_id(self):
        return len(self.load_profiles()['data']) + 1

    def create_profile(self):
        user_id = self.get_next_user_id()
        name = input("Enter name: ")
        preferred_environment = input("Enter preferred environment (Ex: Mountain, Beach, City): ")
        preferred_type = input("Enter preferred type (Ex: house, cabin, condo): ")
        must_have_features = input("Enter preferred features (comma separated, Ex: WI-FI, BBQ Grill, Washer): ").split(',')

        while True:
            try:
                budget = int(input("Enter budget (per night): "))
                break
            except ValueError:
                print("Please enter a valid number for the budget.")

        location = input("Enter preferred location: ")

        profile = {
            "user_id": user_id,
            "name": name,
            "preferred_environment": preferred_environment,
            "preferred_type": preferred_type,
            "Must_have_features": must_have_features,
            "budget": budget,
            "location": location
        }
        print(f"Profile created with user_id: {user_id}")
        return profile

    def save_profile(self, profile):
        data = self.load_profiles()
        data["data"].append(profile)
        with open("users.json", "w") as f:
            json.dump(data, f, indent=4)

    def delete_profile(self, user_id):
        data = self.load_profiles()
        updated_user_list = [data["data"][index] for index in range(len(data['data'])) 
                            if data['data'][index]["user_id"] != user_id]

        data["data"] = updated_user_list
        with open("users.json", "w") as f:
            json.dump(data, f, indent = 4)
        print("Profile successfully Deleted! ")

    def edit_profile(self, user_id, attribute, new_value):
        data = self.load_profiles()
        for user in data['data']:
            if int(user['user_id']) == int(user_id):
                if attribute == 'travel_dates':
                    date_changed = input("Which date would you like to change? (check_in/check_out): ")
                    if date_changed == 'check_in':
                        user['travel_dates'][0] = new_value
                    elif date_changed == 'check_out':
                        user['travel_dates'][1] = new_value
                else:
                    if attribute in user:
                        user[attribute] = new_value
                    else:
                        print(f"Attribute {attribute} does not exist in the profile.")
                        return
                user[attribute] = new_value

        with open("users.json", "w") as f:
            json.dump(data, f, indent = 4)
        print(f"Profile successfully edited with new attribute: {attribute}: {new_value}! ")

    def view_profile(self, user_id):
        data = self.load_profiles()

        if user_id == 'ALL':
            print("")
            print("------ ALL USERS ------")
            for user in data['data']:
                print("")
                print(f"-------------- USER {user['user_id']} --------------")
                print(f"User ID: {user['user_id']}")
                print(f"Name: {user['name']}")
                print(f"Preferred Environment: {user['preferred_environment']}")
                print(f"Preferred Type: {user['preferred_type']}")
                print(f"Preferred Features: {user['Must_have_features']}")
                print(f"Budget: {user['budget']}")
                print(f"Travel Location: {user['location']}")
                print()
        else:
            user_profile = [user for user in data['data'] 
                            if int(user['user_id']) == int(user_id)]
            print("")
            print(f"-------------- USER {user_id} --------------")
            print(f"User ID: {user_profile[0]['user_id']}")
            print(f"Name: {user_profile[0]['name']}")
            print(f"Preferred Environment: {user_profile[0]['preferred_environment']}")
            print(f"Preferred Type: {user_profile[0]['preferred_type']}")
            print(f"Preferred Features: {user_profile[0]['Must_have_features']}")
            print(f"Budget: {user_profile[0]['budget']}")
            print(f"Travel Location: {user_profile[0]['location']}")
            print("-----------------------------------")

# ------------------- Property Recommender -------------------
class PropertyRecommender:
    def __init__(self, dataset_path="/Users/yoyoyue/Desktop/properties_updated.json"):
        # read the file
        self.df = pd.read_json("properties_updated.json")

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

    def recommend(self, profile, top_n=5):
        self.df["fit_score"] = self.df.apply(
            lambda row: self.compute_fit_score(profile, row), axis=1
        )

        expanded = self.df["data"].apply(pd.Series)
        df_fixed = pd.concat([expanded, self.df.drop(columns=["data"])], axis=1)

        df_fixed = df_fixed[df_fixed["City"].str.lower() == str(profile["location"]).lower()]
        recommendations = df_fixed.sort_values('fit_score', ascending=False).head(top_n)
        recommendations = recommendations.to_dict(orient="records")

        print("\nTop Property Recommendations:")
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. Location: {rec['City']}")
            print(f"   Type: {rec['Type']}, Environment: {rec['Environment']}")
            print(f"   Cancellation: {rec['Cancellation_policy']}")
            print(f"   Features: {rec['features']}")
            print(f" Price: {rec['Nightly price']}")
            print(f" Fit_Score: {rec['fit_score']} \n")
        return recommendations

# ------------------- Main -------------------
def main():
    manager = UserProfileManager()
    recommender = PropertyRecommender()

    while True:
        print("\n-----Score My Stay-----")
        print("1. Create Profile")
        print("2. View Profile")
        print("3. Edit Profile")
        print("4. Delete Profile")
        print("5. Property Recommendations")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            profile = manager.create_profile()
            manager.save_profile(profile)
        elif choice == "2":
            user_id = input("Enter user ID (ALL for all users): ")
            manager.view_profile(user_id)
        elif choice == "3":
            user_id = input("Enter the user profile you want to edit: ")

            attribute = input("What attribute would you like to update?: ")
            new_value = input("What is the new value for this attribute? ")
            
            manager.edit_profile(user_id, attribute, new_value)
        elif choice == "4":
            user_id = int(input("Enter the user profile you want to delete: "))
            manager.delete_profile(user_id)
        elif choice == "5":
            user_id = int(input("Enter user ID for recommendations: "))
            profiles = manager.load_profiles()["data"]
            profile = next((p for p in profiles if p["user_id"] == user_id), None)

            if profile:
                top_properties = recommender.recommend(profile, top_n=5)

                for i, prop in enumerate(top_properties, 1):
                    prompt = f""" 
                        User reqs: {profile}.
                        Property: {prop['City']} — {prop['Type']} | Price: ${prop['Nightly price']} | Features: {', '.join(f.replace('"','').replace("'",'') for f in prop['features'])}
                        Task: ONLY 1 sentence (10-15 words), why property fits user reqs.
                        """
                    
                    print(f"\n--- Property {i} Justification---")
                    llm_response = query_openrouter(prompt)
                    if not llm_response:
                        print(f"⚠️ LLM failed for Property {i}. Local info: {prop['City']} — {prop['Type']} | ${prop['Nightly price']} per night")
            else:
                print("Profile not found.")
        elif choice == "6":
            print("Thank you! Have a great day!")
            break

if __name__ == "__main__":
    main()
