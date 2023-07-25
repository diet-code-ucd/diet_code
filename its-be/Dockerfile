FROM python:3 as build-env
WORKDIR /app
COPY . ./
RUN pip install build
RUN python -m build --wheel

FROM python:3
WORKDIR /app
COPY --from=build-env /app/dist/*.whl .
RUN pip install *.whl
RUN pip install waitress
ENTRYPOINT [ "waitress-serve", "--call", "be:create_app" ]
