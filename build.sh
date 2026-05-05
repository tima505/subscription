#!/usr/bin/env bash
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies and build frontend
cd frontend
npm install
npm run build
cd ..

# Copy frontend build files directly to staticfiles root
mkdir -p staticfiles
cp -r frontend/dist/* staticfiles/
cp frontend/dist/index.html backend/templates/

python manage.py collectstatic --no-input
python manage.py migrate
