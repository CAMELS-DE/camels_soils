# Pull python base image
FROM python:3.10

# Install R
RUN apt-get update && apt-get install -y r-base

# the parameter parsing function always needs the rjson and yaml packages
RUN R -e "install.packages(c('jsonlite', 'yaml'))"

# install remotes to install latest version of json2aRgs from Github
RUN R -e "install.packages('remotes')"
RUN R -e "remotes::install_github('VForWaTer/json2aRgs')"

# install json2aRgs v0.3.0 to parse parameters from /in/parameters.json
# RUN wget -q https://cran.r-project.org/src/contrib/json2aRgs_0.3.0.tar.gz
# RUN R CMD INSTALL json2aRgs_0.3.0.tar.gz

# # remove json2aRgs tarball
# RUN rm json2aRgs_0.3.0.tar.gz

# Install R dependencies for corine
RUN apt-get install -y libudunits2-dev libgdal-dev libharfbuzz-dev libfribidi-dev
RUN R -e "install.packages('exactextractr')"

# Install R dependencies for copernicus_dem30
RUN apt-get install -y libudunits2-dev libgdal-dev libharfbuzz-dev libfribidi-dev
RUN R -e "install.packages('exactextractr')"

# install json2args for Python
RUN pip install json2args==0.6.2

# Install Python dependencies for copernicus_dem30
RUN pip install geopandas==0.14.4 rasterio==1.3.9 numpy==1.26.4 OWSLib==0.29.3

# create the tool input structure
RUN mkdir /in
RUN mkdir /out
RUN mkdir /src
COPY ./src /src

# Change working directory
WORKDIR /src

# Run sh script to process ISRIC
CMD ["Rscript", "run.R"]