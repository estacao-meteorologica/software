FROM python3
COPY requirements.txt main.py models/ /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python3", "main.py"]

