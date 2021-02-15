FROM continuumio/miniconda3
RUN conda install -y joblib=1.0.1 pandas=1.2.1 tqdm=4.56
ENTRYPOINT ["python3", "runme.py"]