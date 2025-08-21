import os
import json

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
        Must_have_features = input("Enter must-have features (comma separated) (Ex: WI-FI, BBQ Grill, Washer): ").split(",")
        budget = input("Enter budget: ")
        
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
    
    def edit_profile(self, profile, attribute, new_value):
        data = self.load_profiles()
        for user in data['data']:
            if user == profile:
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
        
### Step3
import pandas as pd

class PropertyRecommender:
    def __init__(self, dataset_path="/Users/yoyoyue/Desktop/properties_updated.json"):
        # 读入 CSV 文件
        self.df = pd.read_json(dataset_path)

    def compute_fit_score(self, profile, property_row):
        """
        Compute fit score for a single property.
        profile: dict
        property_row: pandas.Series
        """
        score = 0
        total_score = 0

        # 1. preferred_environment (权重 0.1, 满分 10)
        env_value = str(property_row.data["Environment"]).lower()
        env_score = 10 if profile["preferred_environment"].lower() == env_value else 0
        score += env_score
        total_score += 10

        

        # 2. preferred_type (权重 0.1, 满分 10)
        type_value = str(property_row.data["Type"]).lower()
        type_score = 10 if profile["preferred_type"].lower() == type_value else 0
        score += type_score
        total_score += 10

        # 3. cancellation_policy (权重 0.1, 满分 10)
        cancellation_policy = str(property_row.data["Cancellation_policy"]).lower()
        cancel_score = 10 if cancellation_policy in ["flexible", "moderate"] else 0
        score += cancel_score
        total_score += 10

        return (score / total_score) * 100 if total_score > 0 else 0


    def recommend(self, profile, top_n=5):
        """
        根据 profile 推荐前 top_n 个房源
        """

        self.df["fit_score"] = self.df.apply(
            lambda row: self.compute_fit_score(profile, row), axis=1
        )
        
        '''
        for idx, row in self.df.iterrows():
            if str(profile["location"]).lower() != str(row.loc["City"]).lower():
                continue  # 跳过不在该城市的房源
            fit_score = self.compute_fit_score(profile, row)
            recommendations.append((row.to_dict(), fit_score))
        '''


        # 按照 fit_score 降序排列
        recommendations = self.df.sort_values('fit_score', ascending=False).head(5)
        recommendations = recommendations['data'].tolist()

        recommendations = [recommendations[i] for i in range(len(recommendations)) if str(profile["location"]).lower() == str(recommendations[i]["City"]).lower()]

                
        for i in range(len(recommendations)):
            #recommendations[i]['fit_score'] = self.compute_fit_score(profile, pd.Series({'data': property}))
            
            print(f"{i+1}. Location: {recommendations[i]['City'] }")
            print(f"   Type: {recommendations[i]['Type']}, Environment: {recommendations[i]['Environment']}")
            print(f"   Cancellation: {recommendations[i]['Cancellation_policy']}")
            print(f"   Features: {recommendations[i]['features']}")
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
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            profile = manager.create_profile()
            manager.save_profile(profile)
        elif choice == "2":
            #manager.view_profile()
            continue
        elif choice == "3":
            attribute = input("What attribute would you like to update?: ")
            
            new_value = input("What is the new value for this attribute? ")
            manager.edit_profile(profile, attribute, new_value)
        elif choice == "4":
            manager.delete_profile(profile)
        elif choice == "5":
            print("Thank you! Have a great day! ")
        elif choice == "6":   # ⭐ 推荐功能
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