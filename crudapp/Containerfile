# 1. Use an official lightweight Python base image
FROM docker.io/library/python:3.12-slim

# 2. Set the internal working directory
WORKDIR /app

# 3. Copy only dependency files first to utilize caching layers
COPY requirements.txt .

# 4. Install production dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the remaining application source code
COPY . .

# 6. Expose the port your application listens on
EXPOSE 8080

# 7. Define the default startup command
CMD ["python", "app.py"]
