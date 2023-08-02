FROM python:3.9
WORKDIR /app
COPY . ./
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install build
RUN python -m build --wheel
RUN pip install .
RUN useradd -m its
RUN chown -R its:its /opt/venv /app
USER its
ENV PATH="/opt/venv/bin:$PATH"
ENTRYPOINT [ "/app/launchers/debug-app.sh" ]
