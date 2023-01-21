FROM python:3-slim
COPY jackpot1p.py /src/jackpot1p.py
COPY high_scores.py /src/high_scores.py
COPY high_scores.default /src/high_scores.dat
