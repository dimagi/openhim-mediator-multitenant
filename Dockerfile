FROM python:3.7

# Create git archive with scripts/build-git-archive.sh to include required submodule
ADD git-archive.tar.gz /usr/src/

WORKDIR /usr/src/openhim-mediator-passthrough/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r submodules/openhim-mediator-utils-py/requirements.txt

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE mediator.settings
ENV PYTHONPATH /usr/src/openhim-mediator-passthrough/submodules/openhim-mediator-utils-py
EXPOSE 8000/tcp
WORKDIR /usr/src/openhim-mediator-passthrough/mediator/
ENTRYPOINT ["docker/entrypoint.sh"]
CMD ["--workers=2", "--bind=:8000"]
