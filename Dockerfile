FROM python:3.13

RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    fonts-liberation \
    libnss3 \
    libgconf-2-4 \
    libxi6 \
    libgdk-pixbuf2.0-0 \
    libappindicator3-1 \
    xdg-utils \
    libatk1.0-0 \
    libxrandr2 \
    libxss1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libgtk-3-0 \
    libvulkan1 \
    libvulkan-dev \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y wget gnupg && \
    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y default-jre && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://github.com/allure-framework/allure2/releases/download/2.32.0/allure-2.32.0.tgz | tar -xz && \
    mv allure-2.32.0 /opt/allure && \
    ln -s /opt/allure/bin/allure /usr/bin/allure

WORKDIR /app

COPY . /app

VOLUME /dev/shm

RUN pip install --no-cache-dir -r requirements.txt

VOLUME [ "/app/reports", "/app/allure-report" ]

CMD pytest --alluredir=reports && allure serve reports --host 0.0.0.0 --port 4040