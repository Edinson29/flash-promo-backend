# flash-promo-backend
This is a project with flash promo in a marketplace

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

# Create mock data for create users, store and products
# This commando create mock data for the next models
# - User, UserProfile, UserSegment, UserDevice
# - Store, Product, StoreProduct
# This information is the base for test apis
python manage.py create_mock_data
