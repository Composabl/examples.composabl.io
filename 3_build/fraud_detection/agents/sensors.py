from composabl import Sensor

step = Sensor("step", "", lambda obs: obs[0])
amount = Sensor("amount", "", lambda obs: obs[1])
oldbalanceOrg = Sensor("oldbalanceOrg", "", lambda obs: obs[2])
newbalanceOrig = Sensor("newbalanceOrig", "", lambda obs: obs[3])
oldbalanceDEst = Sensor("oldbalanceDEst", "", lambda obs: obs[4])
newbalanceDest = Sensor("newbalanceDest", "", lambda obs: obs[5])

sensors = [step, amount, oldbalanceOrg, newbalanceOrig, oldbalanceDEst, newbalanceDest]
