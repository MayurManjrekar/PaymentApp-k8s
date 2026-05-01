FROM python:3.9-slim

# Create user
RUN useradd -m appuser && \
    mkdir -p /app && \
    chown -R appuser:appuser /app

WORKDIR /app

RUN pip install flask requests

# Copy app code and set ownership
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Run app
CMD ["python", "app.py"]