import os
import json
import pandas as pd


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
        Must_have_features = input("Enter preferred features (comma separated) (Ex: WI-FI, BBQ Grill, Washer): ").split(",")
        budget = input("Enter budget (per night): ")
        
        check_in = input("Enter check in date: ")
        check_out = input("Enter check out date: ")

        travel_dates = [check_in, check_out]
        location = input("Enter location: ")

        new_profile = {
            "user_id": user_id,
            "name": name,
            "group_size": group_size,
            "preferred_environment": preferred_environment,
            "preferred_type": preferred_type,
            "Must_have_features": Must_have_features,
            "budget": budget,
            "travel_dates": travel_dates,
            "location": location
        }

        print(f"profile created with user_id: {user_id}")

        return new_profile

    def save_profile(self, profile):
        data = self.load_profiles()
        data["data"].append(profile)
        with open("users.json", "w") as f:
            json.dump(data, f, indent = 4)
        
    def delete_profile(self, profile):
        data = self.load_profiles()
        updated_user_list = [data["data"][index] for index in range(len(data['data'])) 
                            if data['data'][index]["user_id"] != profile["user_id"]]

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
                print(f"Group Size: {user['group_size']}")
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
            print(f"Group Size: {user_profile[0]['group_size']}")
            print(f"Preferred Environment: {user_profile[0]['preferred_environment']}")
            print(f"Preferred Type: {user_profile[0]['preferred_type']}")
            print(f"Preferred Features: {user_profile[0]['Must_have_features']}")
            print(f"Budget: {user_profile[0]['budget']}")
            print(f"Travel Location: {user_profile[0]['location']}")
            print("-----------------------------------")
        
### Step3
class PropertyRecommender:
    def __init__(self, dataset_path="/Users/yoyoyue/Desktop/properties_updated.json"):
        # 读入 CSV 文件
        self.df = pd.read_json("properties_updated.json")

    def compute_fit_score(self, profile, property_row):
        """
        Compute fit score for a single property.
        profile: dict
        property_row: pandas.Series
        """
        score = 0

        # 1. preferred_environment (权重 0.1, 满分 10)
        W_ENV = 0.1
        env_value = str(property_row.data["Environment"]).lower()
        env_score = (10 * W_ENV) if profile["preferred_environment"].lower() == env_value else 0
        
        # 2. preferred_type (权重 0.1, 满分 10)
        W_TYPE = 0.1
        type_value = str(property_row.data["Type"]).lower()
        type_score = (10 * W_TYPE) if profile["preferred_type"].lower() == type_value else 0

        # 3. cancellation_policy (权重 0.1, 满分 10)
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


    def recommend(self, profile, top_n=5):
        """
        根据 profile 推荐前 top_n 个房源
        """

        self.df["fit_score"] = self.df.apply(
            lambda row: self.compute_fit_score(profile, row), axis=1
        )

        expanded = self.df["data"].apply(pd.Series)
        df_fixed = pd.concat([expanded, self.df.drop(columns=["data"])], axis=1)

        df_fixed = df_fixed[df_fixed["City"].str.lower() == str(profile["location"]).lower()]
        recommendations = df_fixed.sort_values('fit_score', ascending=False).head(top_n)
        recommendations = recommendations.to_dict(orient="records")


        for i in range(len(recommendations)):
            print(f"{i+1}. Location: {recommendations[i]['City'] }")
            print(f"   Type: {recommendations[i]['Type']}, Environment: {recommendations[i]['Environment']}")
            print(f"   Cancellation: {recommendations[i]['Cancellation_policy']}")
            print(f"   Features: {recommendations[i]['features']}")
            print(f" Price: {recommendations[i]['Nightly price']}")
            print(f" Fit_Score: {recommendations[i]['fit_score']}")
            print()

    
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
            user_id = input("Enter the user profile you want to view (Enter 'ALL' for all users): ")
            manager.view_profile(user_id)
            continue
        elif choice == "3":
            user_id = input("Enter the user profile you want to delete: ")

            attribute = input("What attribute would you like to update?: ")
            new_value = input("What is the new value for this attribute? ")
            
            manager.edit_profile(user_id, attribute, new_value)
        elif choice == "4":
            user_id = input("Enter the user profile you want to delete: ")
            manager.delete_profile(user_id)
        elif choice == "6":
            print("Thank you! Have a great day! ")
        elif choice == "5":   # ⭐ 推荐功能
            user_id = int(input("Enter your user_id: "))
            profiles = manager.load_profiles()["data"]
            profile = next((p for p in profiles if p["user_id"] == user_id), None)
            if profile:
                recommender.recommend(profile, top_n=5)
            else:
                print("Profile not found.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()