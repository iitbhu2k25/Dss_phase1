# Use Ubuntu as base image
FROM ubuntu:22.04

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Set Python environment variables for better behavior
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Add UbuntuGIS PPA to get GDAL 3.8
RUN apt-get update && apt-get install -y software-properties-common && \
    add-apt-repository ppa:ubuntugis/ubuntugis-unstable

# Install system dependencies including Python and GDAL 3.8
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    gdal-bin \
    libgdal-dev \
    binutils \
    libproj-dev \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create Python symlinks
RUN ln -sf /usr/bin/python3 /usr/bin/python && \
    ln -sf /usr/bin/pip3 /usr/bin/pip

# Verify GDAL installation
RUN echo "GDAL library version:" && gdal-config --version && \
    echo "GDAL configuration:" && gdal-config --cflags --libs && \
    echo "GDAL info:" && gdalinfo --version

# Set the working directory in the container
WORKDIR /app

# Set GDAL environment variables
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Make sure GDAL Python package matches system GDAL version
RUN GDAL_VERSION=$(gdal-config --version) && \
    pip install --upgrade pip && \
    pip install GDAL==${GDAL_VERSION}

# Create non-root user for security
RUN useradd -m -s /bin/bash appuser

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the project files to the container
COPY . .

# Set correct ownership
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose the port Django runs on
EXPOSE 8000
 

# Run migrations and start the Django server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]