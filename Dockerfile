FROM python:3.9.9-bullseye

COPY . /root/doml_poc
RUN pip install -r /root/doml_poc/requirements.txt
WORKDIR /root/doml_poc

CMD ["python", "-i", "-m", "doml_parser", "check", "./tests/examples/doml/piacere/examples/wordpress/aws.doml"]
