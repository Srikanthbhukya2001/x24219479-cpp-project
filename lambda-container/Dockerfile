FROM public.ecr.aws/lambda/python:3.11

# Install build dependencies
RUN yum install -y gcc gcc-c++ python3-devel && \
    yum clean all

COPY requirements.txt .

RUN cat requirements.txt

RUN python -m pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY lambda_function.py ${LAMBDA_TASK_ROOT}

CMD ["lambda_function.lambda_handler"]