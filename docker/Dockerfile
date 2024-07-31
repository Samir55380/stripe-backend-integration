FROM python:3.11.4 as base

# Create app directory
WORKDIR /usr/src/app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

###########START NEW IMAGE : DEBUGGER ###################
FROM base as debug
RUN pip install debugpy
CMD  python -m debugpy --listen 0.0.0.0:5678 --wait-for-client -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
###########START NEW IMAGE : PRODUCTION ###################
FROM base as prod
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]