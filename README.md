# Home Assistant
A Python / Flask app that helps keep on top of what's in the kitchen cupboards

## Setup
The app runs as a Docker container so it's nice and portable.

Replace the contents of app/variables.py with your credentials.

```bash
docker build -t home-assistant .
docker run -d --name my-container -p 80:8080 home-assistant
``` 

The app can also be run with the Flask server for debugging. This is faster as it doesn't require a container rebuild each time. 

```bash
cd app
export FLASK_APP=main.py
export FLASK_ENV=development
flask run
```