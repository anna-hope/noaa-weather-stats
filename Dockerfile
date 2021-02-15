FROM continuumio/miniconda3
RUN conda install -y joblib=1.0.0 pandas=1.2.1 tqdm=4.56
WORKDIR /app
COPY . /app
ENTRYPOINT ["python3", "runme.py"]