FROM python AS py
COPY requirements.txt /project/requirements.txt
WORKDIR /project
RUN pip install -r requirements.txt
ENV FLASK_APP=run.py
#ENTRYPOINT ["/bin/bash", "-c", "flask run --host=0.0.0.0"]
#EXPOSE 5000

