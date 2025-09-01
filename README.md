
---
- **Author:**
  - _Edinson Gutierrez_
---

# flash-promo-backend
This is a project with flash promo in a marketplace
The scope of this project is for the flash_promo to be validated and sent to users within a maximum distance of 2 km.

# install venv
command: 
python3 -m venv venv

# active virtual environment
# windows
venv\Scripts\activate

# macOs/linux
source venv/bin/activate

# install requirements
# This file contains all libraries necesary to work in this project
pip install -r requirements.txt


# UP DOCKER FOR DATABASE
docker-compose up -d

# Execute the migrations
python3 manage.py migrate

# Create mock data for create users, store and products
# This commando create mock data for the next models
# - User, UserProfile, UserSegment, UserDevice
# - Store, Product, StoreProduct
# This information is the base for test apis
python manage.py create_mock_data

# if you want delete all data, use the next command
python3 manage.py delete_all_data

# Up the project
python3 manage.py runserver