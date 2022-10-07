FROM python:3.10.7-bullseye
LABEL maintainer "nicomda@gmail.com"
WORKDIR /app
COPY yet_another_log_analyzer.py yet_another_log_analyzer.py
COPY src/ src/
RUN chmod +x /app/yet_another_log_analyzer.py
WORKDIR /data
ENTRYPOINT ["/app/yet_another_log_analyzer.py"]
