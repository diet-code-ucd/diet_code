FROM python:3 as build-env
WORKDIR /app
COPY . ./
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install build
RUN python -m build --wheel
RUN pip install .
RUN pip install waitress

FROM python:3
WORKDIR /app
RUN useradd -m its
COPY --from=build-env /opt/venv /opt/venv
RUN chown -R its:its /opt/venv /app
USER its
ENV PATH="/opt/venv/bin:$PATH"
ENTRYPOINT [ "waitress-serve", "--call", "be:create_app" ]
