FROM python:3.7

# Create git archive with:
#     $ git archive --output=git-archive.tar.gz \
#         --prefix=openhim-mediator-passthrough/ \
#         HEAD
ADD git-archive.tar.gz /usr/src/

WORKDIR /usr/src/openhim-mediator-passthrough/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r src/openhim-mediator-utils/requirements.txt

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE mediator.settings
EXPOSE 8000/tcp
WORKDIR /usr/src/openhim-mediator-passthrough/mediator/
ENTRYPOINT ["docker/entrypoint.sh"]
CMD ["--workers=2", "--bind=:8000"]
