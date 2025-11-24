# Modbus TCP Simulator (Docker)

This project provides a simple Modbus TCP server written in Python, designed to simulate a device that provides various data types. This README provides instructions for the Docker version.

For the full source code and local script-based usage, please visit the [GitHub repository](https://github.com/miikue/modbus-simulator).

## Features

-   **Modbus TCP Server:** Runs on port `5020`.
-   **Periodic Data Updates:** Every second, the server updates several holding registers with new values:
    -   **Registers 0-9 (uint16):** Ten 16-bit integers that cycle through values from 0 to 50.
    -   **Registers 20-23 (float32):** Two 32-bit floating-point values (Big-Endian).
    -   **Registers 30-37 (float64):** Two 64-bit floating-point values (Big-Endian).

## Usage with Docker

The simulator is available as a pre-built image on Docker Hub, which is the easiest way to run it without setting up a local Python environment.

**Step 1: Pull the Docker Image**

Pull the desired version of the image from Docker Hub. You can use `latest` for the most recent build or a specific version tag (e.g., `0.1`).

```bash
# For the latest version
docker pull miikue/modbus-simulator:latest

# For a specific version
docker pull miikue/modbus-simulator:0.1
```

**Step 2: Run the Container**

Run the simulator in a detached container, mapping the Modbus port `5020` to your host machine.

```bash
docker run -d -p 5020:5020 --name modbus-sim miikue/modbus-simulator:latest
```

The server is now running in the background. You can view its logs using `docker logs modbus-sim`. To stop and remove the container, use `docker stop modbus-sim` and `docker rm modbus-sim`.
