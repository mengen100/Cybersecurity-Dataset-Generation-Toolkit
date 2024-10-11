# Cybersecurity Dataset Generation Toolkit (CDGT)

## Overview

The Cybersecurity Dataset Generation Toolkit (CDGT) is an extensible framework designed to generate customized, realistic, balanced, and labeled datasets for machine learning models in intrusion detection systems (IDS). 

## Features

- **Customizable Scenarios**: Generate datasets based on different levels of network sophistication.
- **Realistic Traffic Simulation**: Produce both malicious and benign network traffic.
- **Containerized Environment**: Utilize Docker for isolated and reproducible network simulations.
- **Extensible Framework**: Easily add new attack vectors and network configurations.

Tested on Ubuntu 22.04.4 LTS

## Installation

1. Clone the repository:
```
git clone https://github.com/mengen100/Cybersecurity-Dataset-Generation-Toolkit.git
cd Cybersecurity-Dataset-Generation-Toolkit
```
2. Set up the environment:
```
sudo ./setuo.sh
```
3. Start the CDGT web interface:
```
sudo flask run
```
4. Access the web interface at `http://localhost:5000`.
5. Select a scenario and start the simulation.
6. Once the simulation is complete, download the generated PCAP files for analysis.