FROM python:3.9

# Move files
RUN mkdir /app
COPY . /app

# Install dependencies
RUN pip install --user -r requirements.txt

# Start update bot
CMD [ "python3", "/app/main.py" ]