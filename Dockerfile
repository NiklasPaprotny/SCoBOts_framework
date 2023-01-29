FROM ubuntu:20.04

WORKDIR /workdir

RUN apt-get update && apt-get install -y --no-install-recommends python3-pip python3-venv git
RUN python3 -m venv .venv
ENV PATH="/workdir/.venv/bin:$PATH"

COPY boca boca
COPY requirements.txt requirements.txt
RUN pip install -U pip
RUN pip install boca/
RUN pip install -r requirements.txt
RUN pip install opencv-python-headless

COPY experiments experiments
COPY scobi scobi
CMD ["cd", "experiments"]

WORKDIR experiments
ENTRYPOINT ["python3", "-u" , "train.py", "--config"]