FROM python
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]




