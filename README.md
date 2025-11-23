# Modbus TCP Simulator

This project provides a simple Modbus TCP server written in Python, designed to simulate a device that provides various data types. It also includes a client for testing and can be run either locally using scripts or as a Docker container.

## Features

-   **Modbus TCP Server:** Runs on port `5020`.
-   **Periodic Data Updates:** Every second, the server updates several holding registers with new values:
    -   **Registers 0-9 (uint16):** Ten 16-bit integers that cycle through values from 0 to 50.
    -   **Registers 20-23 (float32):** Two 32-bit floating-point values (Big-Endian):
        -   **Regs 20-21:** A sine wave value.
        -   **Regs 22-23:** A cosine wave value.
    -   **Registers 30-37 (float64):** Two 64-bit floating-point values (Big-Endian):
        -   **Regs 30-33:** A linear ramp value.
        -   **Regs 34-37:** A triangle wave value.

## Project Structure

-   `simulator.py`: The Modbus TCP server that simulates the device.
-   `modbus_client.py`: A simple client to connect to the server, read the registers, and print their values.
-   `init_venv.sh`: A script to create a Python virtual environment and install the required dependencies.
-   `start_simulation.sh`: A script to start the Modbus TCP server.
-   `Dockerfile`: Allows for building a Docker image of the simulator.

## Usage

There are two primary ways to run the simulation: locally using shell scripts or with Docker.

### 1. Running with Scripts (Linux/macOS)

This method is recommended for local development and testing.

**Step 1: Initialize the Environment**

First, run the initialization script. This will create a Python virtual environment (`venv` directory) and install the necessary dependencies from `requirements.txt`.

```bash
./init_venv.sh
```

**Step 2: Start the Server**

Once the environment is set up, you can start the Modbus server:

```bash
./start_simulation.sh
```

The server will start and run in the foreground. To stop it, press `Ctrl+C`.

**Step 3: Run the Client (Optional)**

To test the server, you can run the client in a separate terminal. Make sure to activate the virtual environment first:

```bash
source venv/bin/activate
python modbus_client.py
```

### 2. Running with Docker

The simulator is also available as a pre-built image on Docker Hub, which is the easiest way to run it without setting up a local Python environment.

**Step 1: Pull the Docker Image**

Pull the latest version of the image from Docker Hub.

```bash
docker pull miikue/modbus-simulator:latest
```

**Step 2: Run the Container**

Run the simulator in a detached container, mapping the Modbus port `5020` to your host machine.

```bash
docker run -d -p 5020:5020 --name modbus-sim miikue/modbus-simulator:latest
```