## Satellite contact automation tool (simulation)
**Manuel Cappuccio, April 2026**
OpenCosmos Candidate Challenge

*AutomationCode_Cappuccio_py is a simulation of an automated Python sequence implemented in a ground station during a satellite pass.
The code mimicks back and forth communications with the spacecraft, focusing on data integrity and 
risk mitigation. The simulation lasts about 2 minutes, during which a built-in timer tracks the 
evolution of the 10-minute contact window.
Main tasks and assumptions are found in the Procedure document ChallengeProcedure_Cappuccio.pdf.
The zip folder ProcedureSimulation_Cappuccio.zip contains the screen recording of the automation
in progress, as a backup in case of any issue with running the code.*

### Key features
- Operator logs: every action or status update is timestamped to simulate a real operator log  
- Health checks: the code simulates the retrieval of critical information on the safety of selected
subsystems (i.e., battery charge and temperature, TX temperature, mass memory level). The TX temperature
parameter is purposedly off-nominal. This triggers the loop control and demonstrates its logic
- Health corrections: for simplicity, the proposed health corrections are to turn ON/OFF the heater 
associated to a subsystem whose temperature is off-nominal. The mass memory is always emptied (after
a data integrity check)
- Risk mitigation logic: critical operations are aborted in absence of a safe time margin
- Duplex simulation: download and upload are performed simultaneusly, when needed

*The code is organized in helper functions which manage standard print and check sequencies.*

### Prerequisites to run the code
- Python 3.10 or higher
- 'time' library 

### Installation and usage
In command window: 
- cd folder_name        (go to the repository where the file is saved)
- python file_name.py 	(run the file)

*Once started, the simulation does not need manual inputs*
