from pgmpy.models import BayesianNetwork
from pgmpy.inference import VariableElimination

car_model = BayesianNetwork(
    [
        ("Battery", "Radio"),
        ("Battery", "Ignition"),
        ("Ignition","Starts"),
        ("Gas","Starts"),
        ("Starts","Moves"),
        ("keyPresent", "Starts")
    ]
)

# Defining the parameters using CPT
from pgmpy.factors.discrete import TabularCPD

cpd_battery = TabularCPD(
    variable="Battery", variable_card=2, values=[[0.70], [0.30]],
    state_names={"Battery":['Works',"Doesn't work"]},
)

cpd_gas = TabularCPD(
    variable="Gas", variable_card=2, values=[[0.40], [0.60]],
    state_names={"Gas":['Full',"Empty"]},
)

cpd_radio = TabularCPD(
    variable=  "Radio", variable_card=2,
    values=[[0.75, 0.01],[0.25, 0.99]],
    evidence=["Battery"],
    evidence_card=[2],
    state_names={"Radio": ["turns on", "Doesn't turn on"],
                 "Battery": ['Works',"Doesn't work"]}
)

cpd_ignition = TabularCPD(
    variable=  "Ignition", variable_card=2,
    values=[[0.75, 0.01],[0.25, 0.99]],
    evidence=["Battery"],
    evidence_card=[2],
    state_names={"Ignition": ["Works", "Doesn't work"],
                 "Battery": ['Works',"Doesn't work"]}
)

cpd_starts = TabularCPD(
    variable="Starts",
    variable_card=2,
    values=[[0.99, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01], [0.01, 0.99, 0.99, 0.99, 0.99, 0.99, 0.99, 0.99]],
    evidence=["Ignition", "Gas", "keyPresent"],
    evidence_card=[2, 2, 2],
    state_names={"Starts":['yes','no'], "Ignition":["Works", "Doesn't work"], "Gas":['Full',"Empty"], "keyPresent":['yes','no']}
)

cpd_moves = TabularCPD(
    variable="Moves", variable_card=2,
    values=[[0.8, 0.01],[0.2, 0.99]],
    evidence=["Starts"],
    evidence_card=[2],
    state_names={"Moves": ["yes", "no"],
                 "Starts": ['yes', 'no']}
)

cpd_keyPresent = TabularCPD(
    variable="keyPresent", variable_card=2,
    values=[[0.70], [0.30]],
    state_names={"keyPresent": ['yes','no']}
)

# Associating the parameters with the model structure
car_model.add_cpds( cpd_starts, cpd_ignition, cpd_gas, cpd_radio, cpd_battery, cpd_moves, cpd_keyPresent)

car_infer = VariableElimination(car_model)


def question3p2():
    print("\nGiven that the car will not move, what is the probability that the battery is not working?")
    print(car_infer.query(variables=["Battery"], evidence={"Moves":"no"}))
    print("35.90% chance that the battery is not working.")
    print("\nGiven that the radio is not working, what is the probability that the car will not start?")
    print(car_infer.query(variables=["Starts"], evidence={"Radio":"Doesn't turn on"}))
    print("86.87% chance that the car will not start.")
    print("\nGiven that the battery is working, does the probability of the radio working change if we discover that the car has gas in it?")
    print("Without knowing about gas:")
    print(car_infer.query(variables=["Radio"], evidence={"Battery":"Works"}))
    print("Knowing the gas tank is full:")
    print(car_infer.query(variables=["Radio"], evidence={"Battery":"Works", "Gas":"Full"}))
    print("No, it does not change the probability of the radio working if we know that there is gas in the car.")
    print("\nGiven that the car doesn't move, how does the probability of the ignition failing change if we observe that the car does not have gas in it?")
    print("Not knowing about gas:")
    print(car_infer.query(variables=["Ignition"], evidence={"Moves":"no"}))
    print("Knowing that the gas is empty:")
    print(car_infer.query(variables=["Ignition"], evidence={"Moves":"no", "Gas":"Empty"}))
    print("The chance of the ignition failing drops from 56.66% to 48.22%.")
    print("\nWhat is the probability that the car starts if the radio works and it has gas in it?")
    print(car_infer.query(variables=["Starts"], evidence={"Radio":"turns on", "Gas":"Full"}))
    print("72.12% chance of the car starting if the radio works and it has gas in it.")

def question3p3():
    print("\nKeyPresent:")
    print("\nP(starts | gas, ignition, keyPresent):")
    print(car_infer.query(variables=["Starts"], evidence={"Gas":"Full", "Ignition":"Works", "keyPresent":"yes"}))
    print("\nP(starts | gas, !ignition, keyPresent):")
    print(car_infer.query(variables=["Starts"], evidence={"Gas": "Full", "Ignition": "Doesn't work", "keyPresent": "yes"}))
    print("Same for rest of possible combinations.")
