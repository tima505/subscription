#!/usr/bin/env bash
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies and build frontend
cd frontend
npm install
npm run build
cd ..

# Copy frontend build to backend templates and static
cp -r frontend/dist/assets staticfiles/
cp frontend/dist/index.html backend/templates/
cp frontend/dist/favicon.svg staticfiles/
cp frontend/dist/icons.svg staticfiles/

python manage.py collectstatic --no-input
python manage.py migrate
