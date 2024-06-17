FROM python:latest

ENV GROUP_ID=1000 \
    USER_ID=1000

# Create app folder
RUN mkdir -p /server/app
# Create uploads folder
RUN mkdir -p /server/uploads && chmod 755 /server/uploads

# Copy app
ADD app/ /server/app/
COPY run.py /server/run.py
COPY requirements.txt /server/requirements.txt

WORKDIR /server/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN addgroup --gid $GROUP_ID www
RUN adduser --shell /bin/sh -u $USER_ID www --ingroup www
RUN chown -R www:www /server/uploads

USER www

# Run the application
CMD ["gunicorn", "-w", "1", "--reload", "--bind", "0.0.0.0:8000", "run:app"]