
FROM python:3.11
WORKDIR /app
COPY . /app
RUN if [ -f "requirements.txt" ]; then pip install -r requirements.txt; fi
CMD ["python", "run.py"]



