## 1. Project information
- Title: LLM-Powered Summer Home Recommender
- Course: RSM8431 – Python 
- Instructor: Arik Senderovich
- Team: Synergy Six
- Member: Danish Siddiqui, Haolong Yang, Junyan Yue, 
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

## 4.	Usage Guide (example of input/output)

Upon launch, you'll see a CLI menu with the following options:
1.	Create Profile – Enter user information such as name, group size, environment, preferred type, budget, dates, and location. Saved to users.json.
2.	View Profile – (Not yet implemented)
3.	Edit Profile – Update specific fields in an existing profile by providing the attribute and a new value.
4.	Delete Profile – Remove a user profile from the system.
5.	Property Recommendations – Enter your user ID to receive your Top-5 recommended listings ranked by a fit score.
6.	Exit – Quit the application.
  
Sample Input Flow:
- Enter your choice: 1
- Enter name: Ryan Zhang
- Enter group size: 4
- Enter preferred environment (Ex: Mountain, Beach, City): city    
- Enter preferred type (Ex: house, cabin, condo): Apartment
- Enter preferred features (comma separated) (Ex: WI-FI, BBQ Grill, Washer): Coffee maker,Sauna
- Enter budget (per night): 100
- Enter check in date: Dec 01
- Enter check out date: Dec 05
- Enter location: Miami
- profile created with user_id: 2

Sample Output (Property Recommendation):
- 1. Location: Miami
   - Type: Apartment, Environment: city
   - Cancellation: flexible
   - Features: ["'Washer & Dryer'", "'Basic toiletries'", "'Crib / High chair'", "'Concierge services'", "'Sauna'"]
   - Price: 42
   - Fit_Score: 5.32

## 5. Team contributions 
| Member             | Contribution                              |
|--------------------|-------------------------------------------|
| Danish Siddiqui    | JSON property loader, Recommender logic，LLM Integration |
| Haolong Yang       | Recommender logic, Documentation          |
| Junyan Yue         | Recommender logic, Testing                |
| Krishitha Muddasani| User flow design, LLM Integration         |
| Siyan Li           | Data cleaning, Scoring logic, Documentation |
| Yuyan Zhang        | Data cleaning, Testing                    |


## 6. Limitation for future improvement 
- No authentication or login system
- Currently CLI-based — GUI or web version would improve usability
- Scoring model is basic — can let the users decide the weight based on their own preferences to allow maximum customization

## 7. Reference: original data source is from Airbnb Listing （https://www.kaggle.com/code/qusaybtoush1990/airbnb-analysis-dataset/input）
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
