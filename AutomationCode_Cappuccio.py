# Manuel Cappuccio, April 2026
# OpenCosmos Challenge

# Import the time, datetime libraries
import time 
import datetime # it will not be used

# Helper functions
def log_action(t, mex):     
    # log_action prints the requested message in the form of an operator log,
    # opened by the input timestamp - which is ficticious for the purpose of this simulation
    
    # time = datetime.now().strftime("%H:%M:%S"), this would be the way to get the actual timestamp
    print(f"[{t}] [OPERATOR_LOG]: {mex}\n")
    time.sleep(2) # The waiting time is accessory to the simulation 

def send_command(comm):
    # send_command notifies the user that the requested command has been sent and,
    # after a latency, acknowledges the correct reception by the spacecraft 
    window = 0 # seconds, acquisition window after which contact is cancelled
    while True: 
        print(f" > SENDING COMMAND: {comm}")
        latency = 3 # seconds, back-and-forth latency. In real scenario this would be measured by the ground station
        time.sleep(latency)
        window = window + latency
        if latency < 15: # seconds, parameter defined in the procedure manual 
            print(f" < ACK RECEPTION for {comm}\n")
            break
        else: # Unexpected LOS procedure
            # time = datetime.now().strftime("%H:%M:%S")
            log_action("time", "STATUS: Temporary loss of signal.")
            # Procedure: change carrier frequency or antenna orientation around the expected coordinates, then retry.
            if window > 60: # seconds, re-acquisition window threshold after which contact is cancelled 
                log_action("time", "STATUS: Loss of signal. Cancel activity.")
                # sys.exit(1), interrupts the simulation
            
    time.sleep(2) 

def display(mex):
    # display prints the input messages, mostly notifications of running processes. Accepts multiple messages
    for n_mex in mex:
        print(f"{n_mex}...\n")
        time.sleep(2)

def health_checks(data):
    # health_checks simulates the health checks performed while reviewing the logs of the spacecraft. 
    # For simplicity, this simulation only checks battery charge and temperature, transmitter temperature, 
    # mass memory occupation. Nominal ranges are known to the computer:
    battery_charge_range = [20, 100] # %
    battery_temp_range = [253, 313] # K
    TX_temp_range = [263, 303] # K
    memory_range = [0, 80] # %
    # Every critical variable has its own check algorithm. Every one of them fully checks the nominality of the data
    if data[0]>battery_charge_range[0]:
        print(f"Battery level: {data[0]:.1f} % NOMINAL")
        time.sleep(3)
    else:
        print(f"Battery level: {data[0]:.1f} % OFF-NOMINAL")
        # send_command(SAFEMODE)
        log_action("STATUS: SAFEMODE Activated. Aborting contact")
        # end of simulation
   
    while data[1]<battery_temp_range[0] or data[1]>battery_temp_range[1]:   #...while TX temperature is out of range... 
        if data[1]<battery_temp_range[0]: #too cold
            print(f"Battery temperature: {(data[1]-273.15):.2f}°C OFF-NOMINAL")
            # Example of standard procedure: turn on heaters
            send_command("BATT_HEATER_ON")
            # wait 30 seconds and check again
            display({"Waiting 30 seconds"})
        elif data[2]>battery_temp_range[1]:
            print(f"Battery temperature: {(data[1]-273.15):.2f}°C OFF-NOMINAL")
            # Emergency procedure: turn on heaters
            send_command("BATT_HEATER_OFF")
            # wait 30 seconds and check again  
            display({"Waiting 30 seconds"})
    # If out of the while cycle, the temperature is nominal          
    print(f"Battery temperature: {(data[1]-273.15):.2f}°C NOMINAL")
    time.sleep(3)

    while data[2]<TX_temp_range[0] or data[2]>TX_temp_range[1]:   #...while TX temperature is out of range... 
        if data[2]<TX_temp_range[0]: #too cold
            print(f"TX temperature: {(data[2]-273.15):.2f}°C OFF-NOMINAL")
            # Emergency procedure: turn on heaters
            send_command("TX_HEATER_ON")
            # wait 30 seconds and check again
            display({"Waiting 30 seconds"})
        elif data[2]>TX_temp_range[1]:
            print(f"TX temperature: {(data[2]-273.15):.2f}°C OFF-NOMINAL")
            # Emergency procedure: turn on heaters
            send_command("TX_HEATER_OFF")
            # wait 30 seconds and check again  
            display({"Waiting 30 seconds"})
            # SIMULATION: now the temperature is down to 300 K 
            data[2] = 300

    # If out of the while cycle, the temperature is nominal          
    print(f"TX temperature: {(data[2]-273.15):.2f}°C NOMINAL")
    time.sleep(3)

    if data[3]<memory_range[1]:
        print(f"Mass memory level: {data[3]:.1f} % NOMINAL")
        time.sleep(3)
    else:
        print(f"Mass memory level: {data[3]:.1f} % OFF-NOMINAL")
        # Emergency procedure: check the integrity of the received data and delete it
        # Procedure already implemented later

# --- Main ---
# Simulation of automated procedure
# Begin procedure - establish contact with s/c
print("\n---Start of contact sequence simulation---\n")
aos_mexs = {"Importing TLEs", "Pointing antenna"}
display(aos_mexs)
send_command("TX_MOD_ON") # Commands Tx and Tx modulation to turn ON

# T=0: contact phase
# - [00:00 - 02:00] health and platform checks
time0 = "10:15:20"
log_action(time0, "Link established, starting contact phase")


send_command("REQ_HEALTH")
display({"Downloading health data"})
send_command("REQ_LOGS")
display({"Downloading logs"})
display({"Performing health checks"})

# Critical health data are saved locally. Each variable is checked to find any off-nominals
# Hypothesis: data coming from satellite
battery_charge = 92
battery_temp = 289
TX_temp = 316 # Off-nominal
memory = 78 

health_checks([battery_charge, battery_temp, TX_temp, memory])
log_action("10:17:00","STATUS: All subsystems NOMINAL.")
display({"Checking data integrity"})
log_action("10:17:10","STATUS: All data downloaded correctly.")
send_command("DEL_LOGS")

# - [02:00 - 07:00] payload operations and command uplink
time1 = "10:17:20"
Dtime = 8 # minutes, simulated
print("Remaining time: ",Dtime, " minutes")

if Dtime>4: # time to upload and restart TMTC
    log_action(time1, "Starting payload data download and command upload") 
    send_command("REQ_PL_DATA")
    send_command("UPLOAD_FILE[new_comms_config.txt]")
    display({"Downloading data"})
    display({"Uploading file"})
    time.sleep(5) 
    log_action("10:21:00", "Payload data download completed") 
    time.sleep(2)
    log_action("10:21:30", "Configuration file upload completed") 
    display({"Checking data integrity"})
    log_action("10:22:00","STATUS: All data downloaded correctly.")
    send_command("DEL_PL_DATA")
else:
    log_action(time1,"WARNING: Insufficient time. Aborting task.")

# - [07:00 - 10:00] platform activity
time2 = "10:22:20"
Dtime = 3 # minutes, simulated
print("Remaining time: ",Dtime, " minutes")
if Dtime > 2:
    log_action(time2,"Starting platform activity")
    send_command("RESTART_TMTC")
    log_action("10:23:00", "STATUS: Loss of signal.") # Expected
    display({"Waiting for link re-establishment"})
    # TX is off by default
    send_command("TX_MOD_ON")
    time3 = "10:23:30"
    log_action(time3, "Link established, starting configuration checks.")
    send_command("REQ_TMTC_HEALTH")
    display({"Downloading TMTC health data"})
    log_action("10:24:00","STATUS: TMTC subsystem NOMINAL")
    display({"Verifying new file configuration"})
    log_action("10:24:30","CONFIRMATION: New configuration applied successfully.")
else:
    log_action(time2,"WARNING: Insufficient time. Aborting task.")

log_action("10:25:20", "STATUS: Loss of signal.")
print("---End of contact sequence simulation---\n")



