from customer import snl
from customer import l3
from customer import ga


def detect_item_base_contract(contract, path):


    if contract == "SNL":
        data = snl.find_q_clause(path)
        print(data)
        return

    if contract == "L3":
        data = l3.find_q_clause(path)
        print(data)
        return

    if contract == "GA":
        data = ga.find_q_clause(path)
        print(data)
        return
