# Use official Python image
FROM python:3.12

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for Streamlit UI
EXPOSE 8501

# Run Streamlit app
CMD ["streamlit", "run", "src/main.py"]
