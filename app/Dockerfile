FROM python:3.8

WORKDIR /app

RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    alsa-utils \
    pulseaudio \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/templates /app/static

COPY . .

ENV PULSE_SERVER=unix:/run/user/1000/pulse/native
ENV PULSE_COOKIE=/root/.config/pulse/cookie
ENV AUDIODEV=hw:0,0

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
