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

        print(f"profile created with ID: {user_id}. Please make sure to remember this ID!")

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

        profile = None

        if choice == "1":
            profile = manager.create_profile()
            manager.save_profile(profile)
        elif choice == "2":
            #manager.view_profile()
            continue
        elif choice == "3":
            try:
                user_id = input("Please input your user ID: ")
            except ValueError:
                print("You have entered an invalid user ID. Please try again...")

            if profile == None:
                print("You can't edit a profile before creating it! ")
            else:
                attribute = input("What attribute would you like to update?: ")
                new_value = input("What is the new value for this attribute? ")
                manager.edit_profile(profile, attribute, new_value)
        elif choice == "4":
            manager.delete_profile(profile)
        elif choice == "5":
            print("Thank you! Have a great day! ")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
