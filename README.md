## 1. Project information
Title: LLM-Powered Summer Home Recommender
Course: RSM8431 – Python 
Instructor: Arik Senderovich
Team: Synergy Six
Member: Danish Siddiqui, Haolong Yang, Junyan Yue, 
Krishitha Muddasani, Siyan Li, Yuyan Zhang

## 2. Overview

This project is a Python-based command-line application that provides personalized recommendations for summer home rentals, inspired by Airbnb. The platform calculates a fit score for each property based on factors such as budget, property type, cancellation policy, must-have features, and preferred environment. Using these scores, it delivers the top five property matches tailored to the user’s needs, making it easy to discover and compare the best rental options.

## 3. Features
- User Profile Management
 - Create, edit, view, delete profiles
 - Input: user_id, name, group_size, preferred_environment, preferred_type, Must_have_features, budget, travel_dates, location
- Property Listings
 - Load property data from JSON
 - Properties include city, type, nightly price, cancellation policy, review scores rating, picture url, tags, features, and environment
- Recommender System
 - Fit score based on budget match, type, cancellation policy, must-have features, and preferred environment preferences
 - Top-5 ranking output
- LLM Integration (optional)
 - Generate listings, descriptions, travel tips
 - Powered by OpenRouter or OpenAI
- Command-Line Interface
 - Menu-driven commands like create_user, view_properties, get_recommendations, etc.

## 4.	Installation/Setup (Donald)
## 5.	Usage Guide (example of input/output & Screenshots of GUI)

Upon launch, you'll see a CLI menu with the following options:
1.	Create Profile – Enter user information such as name, group size, environment, preferred type, budget, dates, and location. Saved to users.json.
2.	View Profile – (Not yet implemented)
3.	Edit Profile – Update specific fields in an existing profile by providing the attribute and a new value.
4.	Delete Profile – Remove a user profile from the system.
5.	Property Recommendations – Enter your user ID to receive your Top-5 recommended listings ranked by a fit score.
6.	Exit – Quit the application.
  
Sample Input Flow:
Enter name: Alice
Enter group size: 3
Enter preferred environment (Ex: Mountain, Beach, City): beach
Enter preferred type (Ex: house, cabin, condo): house
Enter preferred features (comma separated): WiFi, BBQ, Washer
Enter budget (per night): 200
Enter check in date: 2025-08-01
Enter check out date: 2025-08-05
Enter location: Miami

Sample Output (Property Recommendation):
1. Location: Miami
   Type: House, Environment: Beach
   Cancellation: Flexible
   Features: WiFi, BBQ, Washer
   Price: 185
   Fit_Score: 8.6

## 6. Team contributions 
| Member             | Contribution                              |
|--------------------|-------------------------------------------|
| Danish Siddiqui    | JSON property loader, Recommender logic, UI Design |
| Haolong Yang       | Recommender logic, Documentation          |
| Junyan Yue         | Recommender logic, Testing                |
| Krishitha Muddasani| User flow design, LLM Integration         |
| Siyan Li           | Data cleaning, Scoring logic, Documentation |
| Yuyan Zhang        | Data cleaning, Testing                    |


## 7. Limitation for future improvement 
- No authentication or login system
- Currently CLI-based — GUI or web version would improve usability
- Scoring model is basic — can let the users decide the weight based on their own preferences to allow maximum customization

## 8. Reference: original data source is from Airbnb Listing
To ensure consistent and relevant data for the recommender system, the following data cleaning steps were applied to the original dataset:
1.	Remove Unnecessary Attributes
Columns that were irrelevant to the recommendation logic (e.g., host info, reviews, URLs) were dropped to reduce complexity.
2.	Handle Missing Data
Entries with critical missing fields such as price, location, or property type were removed. Empty cells were filtered or filled when appropriate.
3.	Normalize Formats and Types
Ensured consistency in data types (e.g., prices as integers, features as lists). All text fields were converted to lowercase to support case-insensitive matching.
4.	Tag Extraction from Descriptions
Tags such as "family-friendly", "remote", and "pet-friendly" were programmatically extracted from the property descriptions using keyword matching to enrich each listing's metadata.

## License
Educational use only. No commercial redistribution.
