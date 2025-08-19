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
        min_budget = input("Enter Minimum budget: ")
        max_budget = input("Enter Maximum budget: ")
        
        check_in = input("Enter check in date: ")
        check_out = input("Enter check out date: ")

        travel_dates = [check_in, check_out]
        location = input("Enter location: ")

        new_profile = {
            "user_id": user_id,
            "name": name,
            "group_size": group_size,
            "preferred_environment": preferred_environment,
            "min_budget": min_budget,
            "max_budget": max_budget,
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
                user[attribute] = new_value

        with open("users.json", "w") as f:
            json.dump(data, f, indent = 4)
        print(f"Profile successfully edited with new attribute: {attribute}: {new_value}! ")
        
    


user_1 = UserProfileManager()
profile = user_1.create_profile()
user_1.save_profile(profile)

user_1.edit_profile(profile, 'min_budget', 1200)

query = input("Would you like to Delete User?: ")

if query == "y":
    user_1.delete_profile(profile)


'''
class UserProfileManager:
    def __init__(self, file_name="user_profiles.csv"):
        self.file_name = file_name
        self.df = self.load_profiles()

    def load_profiles(self):
        if os.path.exists(self.file_name):
            return pd.read_csv(self.file_name)
        else:
            return pd.DataFrame(columns=[
                "user_id", "name", "group_size", "preferred_environment",
                "min_budget","max_budget", "travel_dates" 
            ])

    def save_profiles(self):
        self.df.to_csv(self.file_name, index=False)

    def get_next_user_id(self):
        if self.df.empty:
            return 1
        else:
            return int(self.df["user_id"].max()) + 1

    def create_profile(self):
        user_id = self.get_next_user_id()
        name = input("Enter name: ")
        group_size = input("Enter group size: ")
        preferred_environment = input("Enter preferred environment: (Ex: Mountain, beach, City, etc) ")
        min_budget = input("Enter Minimum budget: ")
        max_budget = input("Enter Maximum budget: ")
        travel_dates = input("Enter travel dates (optional): ")

        new_profile = {
            "user_id": user_id,
            "name": name,
            "group_size": group_size,
            "preferred_environment": preferred_environment,
            "min_budget": min_budget,
            "max_budget": max_budget,
            "travel_dates": travel_dates
        }

        self.df = pd.concat([self.df, pd.DataFrame([new_profile])], ignore_index=True)
        self.save_profiles()
        print(f"Profile created. Your user ID is: {user_id}")

    def view_profile(self):
        user_id = input("Enter user ID to view: ")
        profile = self.df[self.df["user_id"] == int(user_id)]
        if not profile.empty:
            print(profile.to_string(index=False))
        else:
            print("Profile not found.")

    def edit_profile(self):
        user_id = input("Enter user ID to edit: ")
        index = self.df.index[self.df["user_id"] == int(user_id)].tolist()
        if not index:
            print("Profile not found.")
            return

        i = index[0]
        print("Leave blank to keep current value.")
        for col in ["name", "group_size", "preferred_environment", "min_budget","max_budget", "travel_dates"]:
            current = self.df.at[i, col]
            new_val = input(f"{col} [{current}]: ")
            if new_val:
                self.df.at[i, col] = new_val

        self.save_profiles()
        print("Profile updated.")

    def delete_profile(self):
        user_id = input("Enter user ID to delete: ")
        self.df = self.df[self.df["user_id"] != int(user_id)]
        self.save_profiles()
        print("Profile deleted.")

def main():
    manager = UserProfileManager()
    while True:
        print("\nUser Profile Manager")
        print("1. Create Profile")
        print("2. View Profile")
        print("3. Edit Profile")
        print("4. Delete Profile")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            manager.create_profile()
        elif choice == "2":
            manager.view_profile()
        elif choice == "3":
            manager.edit_profile()
        elif choice == "4":
            manager.delete_profile()
        elif choice == "5":
            print("Thank you! Have a great day! ")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()

'''