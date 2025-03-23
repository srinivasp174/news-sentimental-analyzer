# Use an official Python image
FROM python:3.9

# Create a non-root user for security
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

# Set working directory inside container
WORKDIR /app

# Copy dependencies first (to optimize Docker caching)
COPY --chown=user ./requirements.txt requirements.txt

# Install dependencies (ensure Streamlit is installed)
RUN pip install --no-cache-dir -r requirements.txt streamlit

# Copy the application code
COPY --chown=user . /app

# Expose port 7860 (Hugging Face Spaces Requirement)
EXPOSE 7860

# Run both Flask and Streamlit together
CMD ["bash", "-c", "python api.py & streamlit run app.py --server.port 7860 --server.address 0.0.0.0"]
