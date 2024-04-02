FROM python:3.8

ADD . /code
WORKDIR /code
RUN pip install opencv-python numpy
CMD ["python", "naloga1.py"]