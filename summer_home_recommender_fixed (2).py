import os
import json
import pandas as pd
import requests

# ------------------- LLM Query -------------------
def query_openrouter(prompt):
    API_KEY = "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"
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
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        if "choices" not in result or len(result["choices"]) == 0:
            print("⚠️ No response returned from LLM")
            return None

        return result["choices"][0]["message"]["content"]

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
        num_users = len(self.load_profiles()['data'])
        return num_users + 1

    def create_profile(self):
        user_id = self.get_next_user_id()
        name = input("Enter name: ")
        group_size = input("Enter group size: ")
        preferred_environment = input("Enter preferred environment (Ex: Mountain, Beach, City): ")
        preferred_type = input("Enter preferred type (Ex: house, cabin, condo): ")
        must_have_features = input("Enter preferred features (comma separated, Ex: WI-FI, BBQ Grill, Washer): ").split(',')
        budget = input("Enter budget (per night): ")
        check_in = input("Enter check-in date (YYYY-MM-DD): ")
        check_out = input("Enter check-out date (YYYY-MM-DD): ")
        travel_dates = [check_in, check_out]
        location = input("Enter preferred location: ")

        profile = {
            "user_id": user_id,
            "name": name,
            "group_size": group_size,
            "preferred_environment": preferred_environment,
            "preferred_type": preferred_type,
            "Must_have_features": must_have_features,
            "budget": budget,
            "travel_dates": travel_dates,
            "location": location
        }

        print(f"Profile created with user_id: {user_id}")
        return profile

    def save_profile(self, profile):
        data = self.load_profiles()
        data["data"].append(profile)
        with open("users.json", "w") as f:
            json.dump(data, f, indent=4)

    def delete_profile(self, profile):
        data = self.load_profiles()
        data["data"] = [u for u in data["data"] if u["user_id"] != profile["user_id"]]
        with open("users.json", "w") as f:
            json.dump(data, f, indent=4)
        print("Profile successfully deleted!")

    def edit_profile(self, profile, attribute, new_value):
        data = self.load_profiles()
        for user in data['data']:
            if user == profile:
                if attribute == 'travel_dates':
                    date_changed = input("Which date to change? (check_in/check_out): ")
                    if date_changed == 'check_in':
                        user['travel_dates'][0] = new_value
                    else:
                        user['travel_dates'][1] = new_value
                else:
                    if attribute in user:
                        user[attribute] = new_value
        with open("users.json", "w") as f:
            json.dump(data, f, indent=4)
        print(f"Profile successfully edited with new {attribute}: {new_value}!")

    def view_profile(self, user_id):
        data = self.load_profiles()
        if user_id == 'ALL':
            for user in data['data']:
                print(f"\nUSER {user['user_id']}: {user['name']}, Location: {user['location']}")
        else:
            user_profile = next((u for u in data['data'] if u['user_id'] == int(user_id)), None)
            if user_profile:
                print(f"USER {user_profile['user_id']}: {user_profile['name']}, Location: {user_profile['location']}")
            else:
                print("Profile not found.")

# ------------------- Property Recommender -------------------
class PropertyRecommender:
    def __init__(self, dataset_path="properties.json"):
        self.df = pd.read_json(dataset_path)

    def compute_fit_score(self, profile, property_row):
        W_ENV, W_TYPE, W_CANCELLATION, W_BUDGET, W_FEATURES = 0.1, 0.1, 0.1, 0.4, 0.3
        score = 0

        env_tags = [t.lower() for t in property_row.data.get("Tags", [])]
        if profile["preferred_environment"].lower() in env_tags:
            score += 10 * W_ENV

        type_value = str(property_row.data["Type"]).lower()
        if profile["preferred_type"].lower() == type_value:
            score += 10 * W_TYPE

        cancel_policy = str(property_row.data["Cancellation_policy"]).lower()
        if cancel_policy in ["flexible", "moderate"]:
            score += 10 * W_CANCELLATION

        price = int(property_row.data["Nightly price"])
        budget = int(profile["budget"])
        score += (((budget - price) / budget) * 10) * W_BUDGET

        must_have = [f.strip().lower() for f in profile.get("Must_have_features", []) if f.strip()]
        property_feats = [f.strip("'").lower() for f in property_row.data.get("features", [])]
        if must_have:
            matched = sum(1 for f in must_have if f in property_feats)
            score += (10 * (matched / len(must_have))) * W_FEATURES

        location = profile.get("location", '').lower()
        if location in str(property_row.data["City"]).lower():
            score += 2

        return round(score, 2)

    def recommend(self, profile, top_n=5):
        self.df["fit_score"] = self.df.apply(lambda row: self.compute_fit_score(profile, row), axis=1)
        df_expanded = pd.concat([self.df.drop(columns=['data']), self.df['data'].apply(pd.Series)], axis=1)
        recommendations = df_expanded.sort_values('fit_score', ascending=False).head(top_n).to_dict(orient="records")

        print("\nTop Property Recommendations:")
        for i, prop in enumerate(recommendations, 1):
            print(f"{i}. {prop['City']} — {prop['Type']} | ${prop['Nightly price']} per night | Features: {prop['features']} | Fit Score: {prop['fit_score']}")

        return recommendations

# ------------------- Main -------------------
def main():
    manager = UserProfileManager()
    recommender = PropertyRecommender()

    while True:
        print("\nUser Profile Manager")
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
            user_id = int(input("Enter user ID to edit: "))
            profiles = manager.load_profiles()["data"]
            profile = next((p for p in profiles if p["user_id"] == user_id), None)
            if profile:
                attr = input("Attribute to edit: ")
                new_val = input("New value: ")
                manager.edit_profile(profile, attr, new_val)
        elif choice == "4":
            user_id = int(input("Enter user ID to delete: "))
            profiles = manager.load_profiles()["data"]
            profile = next((p for p in profiles if p["user_id"] == user_id), None)
            if profile:
                manager.delete_profile(profile)
        elif choice == "5":
            user_id = int(input("Enter user ID for recommendations: "))
            profiles = manager.load_profiles()["data"]
            profile = next((p for p in profiles if p["user_id"] == user_id), None)

            if profile:
                top_properties = recommender.recommend(profile, top_n=5)
                properties_text = "\n".join([
                    f"{i+1}. {prop['City']} — {prop['Type']} | Price: ${prop['Nightly price']} | Features: {', '.join([f.replace('"','').replace("'",'') for f in prop['features']])}"
                    for i, prop in enumerate(top_properties)
                ])

                prompt = f"You are a smart real-estate recommender system.\n" \
                         f"User profile: {profile}\n" \
                         f"Consider all North American locations.\n" \
                         f"Top 5 candidate properties:\n{properties_text}\n" \
                         f"Recommend the best properties, rank 1-5 with simple numbering, and give a 1-2 line explanation for each."

                llm_response = query_openrouter(prompt)
                if llm_response:
                    print("\n🔮 AI-Powered Property Recommendations:")
                    print(llm_response)
                else:
                    print("\n⚠️ LLM failed, showing local recommendations:")
                    for i, prop in enumerate(top_properties, 1):
                        print(f"{i}. {prop['City']} — {prop['Type']} | ${prop['Nightly price']} per night")
            else:
                print("Profile not found.")
        elif choice == "6":
            print("Thank you! Have a great day!")
            break

if __name__ == "__main__":
    main()
