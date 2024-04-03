FROM python:3.6
RUN apt-get update
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app


RUN echo Y |  apt-get install libgdal-dev
RUN echo Y | apt install libspatialindex-dev

RUN pip install --upgrade pip
RUN pip install pandas fiona shapely pyproj rtree
RUN pip install geopandas 


COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

EXPOSE 8080

ENTRYPOINT ["python3"]

CMD ["-m", "swagger_server"]