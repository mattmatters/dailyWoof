FROM python:3.6.3
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV NAME image_manager

CMD ["python", "image.py"]