# Project Name: DOPCS Simulation

## Description
This project simulates the production process based on various demands and configurations. It uses a Python-based simulator to manage and visualize the production data.

## Installation and Setup

### Prerequisites
- [Anaconda](https://www.anaconda.com/products/individual) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) must be installed on your system.

Below uses a manual approach for creating a suitable environment, and running it. Alternatively, you can use any other python distribution and make sure your interpreter has the packages listed under environment.yml. You can then run
the simulator.py script using that interpreter. 

### Setting Up the Conda Environment
1. **Clone the Repository**:
   If you have access to the repository, clone it using Git:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
 
2. **Clone the Conda environment**: 
   If you have access to the repository, clone it using Git:
   ```bash
   conda env create -f environment.yml
   
3. **Activate the Environment**: 
   If you have access to the repository, clone it using Git:
   ```bash
   conda activate dopcs
   
### Running the simulator

   Start the simulator with the following command:  ```bash
   ```bash
   python simulator.py
   ```
### Content
`settings.py` contains some simulation constants. `dataloader.py` loads the excel data and puts it to a suitable data 
format. `plotting_utils.py` has some logic for plotting some key simulation information. `simulator.py` is the main 
simulation script. `simulationstatus.py` creates an objects (with several nested objects) that together hold the status 
of the system from day to day.   

### Important
The provided simulation code is a starting point. It may need some corrections, and it needs further work. For example, 
the code only simulates the filling line, and it does not actually consume any mix while filling. Also, the logic 
pertaining to the numbering of days may be off. 

### Notes
The simulation does not use a future event set (FES), nor does it use SimPy. For the present system, both are not really needed and might be overkill, plus they 
do not always make the code more understandable if you are unfamiliar with the packages. Instead, we inspect the status of the system at the beginning of
every day, and by using suitable data structures (like Deque) we can determine what happens on that day. This is fairly 
suitable since the system changes in discrete time, except for things happening in production units, which can be handled in relative
isolation to things happening in other PUs. However, if you strongly prefer a FES, then you are welcome
to refactor, of course. 