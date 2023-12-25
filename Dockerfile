FROM python:3.11
EXPOSE 5000
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN playwright install
RUN playwright install-deps
RUN apt-get install libnss3\libnspr4\libdbus-1-3\libatk1.0-0\libatk-bridge2.0-0\libcups2\libdrm2\libxkbcommon0\libatspi2.0-0\libxcomposite1\libxdamage1\libxfixes3\libxrandr2\libgbm1\libasound2     
COPY . .
CMD [ "flask", "run","--host","0.0.0.0" ]
