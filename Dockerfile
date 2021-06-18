# first stage
FROM python:3.8 AS bulder
COPY requirements.txt .

#install dependencies to the local user directory (eg. /root/.local)
RUN pip install --user -r requirements.txt

# second unnamed stage
FROM python:3.8-slim
WORKDIR /

# copy only the dependencies that are needen for our application and the source files
COPY --from=bulder /root/.local /root/.local
COPY . /

# update PATH
ENV PATH=/root/.local:$PATH

# make sure you include the -u flag to have our stdout logged
CMD [ "python", "-u", "./app/main.py" ]