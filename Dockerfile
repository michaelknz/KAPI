FROM python:3.9
WORKDIR /wrk 
COPY ./reqirements.txt /wrk/reqirements.txt
RUN pip install --no-cache-dir --upgrade -r /wrk/reqirements.txt
COPY ./app /wrk/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]