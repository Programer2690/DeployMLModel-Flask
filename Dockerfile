FROM python:3.11-slim

WORKDIR /app

# Install dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Generate model.pkl at build time
RUN python model.py

EXPOSE 5000

# Serve with Gunicorn: module=application, Flask instance=application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "application:application"]