FROM python:3.9 as build-env
WORKDIR /app
COPY . ./
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install build
RUN python -m build --wheel
RUN pip install .

FROM python:3.9 as runtime-env
WORKDIR /app
RUN useradd -m its
COPY --from=build-env /opt/venv /opt/venv
COPY ./launchers/start-app.sh .
RUN chown -R its:its /opt/venv /app
USER its
ENV PATH="/opt/venv/bin:$PATH"
ENTRYPOINT [ "/app/start-app.sh" ]
