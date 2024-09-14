FROM python:3.9
EXPOSE 8000
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
CMD ["gunicorn", "-b", "0.0.0.0:8000", "--workers", "2", "app:app"]
