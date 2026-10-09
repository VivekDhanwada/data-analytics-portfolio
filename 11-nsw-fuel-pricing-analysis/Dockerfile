FROM public.ecr.aws/lambda/python:3.12

COPY requirements.txt ${LAMBDA_TASK_ROOT}/
RUN pip install --no-cache-dir -r requirements.txt

COPY src/config.py src/auth.py src/ingest.py ${LAMBDA_TASK_ROOT}/

CMD ["ingest.lambda_handler"]
