import hashlib
import json


def isValidHash(hash):
    return hash[0:4] == "0000"


# док-во работы, это число нужно подобрать так, чтобы хэш начинался с нулей
def isValidProof(block, proof):  # подходит ли это число в качетсво док-ва работы
    block_copy = block.copy()
    block_copy["proof"] = proof
    hash = dataToHash(block_copy)  # считаем новый хэш
    is_valid_hash = isValidHash(hash)
    return is_valid_hash  # начинается ли хэш с двух нулей


def mineProofOfWork(block):
    # майним число, чтобы, добавив его к блоку, хэш начинался с двух нулей
    # это делается для того, чтобы сделать новую запись в блокчнйне с нужным хэшем
    # (например, начинающимся с 0000, иначе остальные участники сети не примкт эту запись)
    proof = 0
    while not isValidProof(block, proof):
        proof += 1
    return proof


def dataToHash(data):  # написали функцию, которая возвращает хэш каких-либо данных
    json_Data = json.dumps(data)
    binary_Data = json_Data.encode()
    return hashlib.sha256(binary_Data).hexdigest()[:10]


genesis_block = {
    "from": "",  # кто отправил
    "to": "",  # кому отправил(а)
    "amount": 0.0  # сколько отправили
}

genesis_block["proof"] = mineProofOfWork(genesis_block)
blockchain = [  # в нашем случае это список транзакций
    # нужен первый пустой блок из-за особенности блокчейна
    # (всегда считать хэш предлыдущего блока)
    genesis_block

]


def addNewBlock(account_from, account_to, amount):  # добавить запись/блок в блокчейн
    previous_block = blockchain[-1]  # последний блок в блокчейне
    previous_hash = dataToHash(previous_block)

    block = {
        "from": account_from,
        "to": account_to,
        "amount": amount,
        "previous_hash": previous_hash

    }  # создаем блок

    proof = mineProofOfWork(block)
    block["proof"] = proof
    blockchain.append(block)


addNewBlock("Satoshi", "Vasya", 2000)
addNewBlock("Satoshi", "Petya", 14)
addNewBlock("Satoshi", "Kolya", 88)
addNewBlock("Satoshi", "Nastya", 69420)

addNewBlock("Vasya", "Petya", 1000)
addNewBlock("Petya", "Nastya", 500)
addNewBlock("Petya", "Kolya", 500)


def calcBalances():
    balances = {}
    balances_list = []
    for block in blockchain:
        if block["from"] in balances:  # если есть запись о балансе отправителя, то положим ее в переменную
            balance_from = balances[block["from"]]
        else:
            balance_from = 0

        if block["to"] in balances:  # если есть запись о балансе получателся, то положим ее в переменную
            balance_to = balances[block["to"]]
        else:
            balance_to = 0

        balance_from -= block["amount"]  # проверить разницу (> 0?)
        balance_to += block["amount"]

        balances[block["from"]] = balance_from
        balances[block["to"]] = balance_to

    for value in balances.values():
        balances_list.append(value)

    return balances, balances_list


def validBlockchain():
    prev_block = None
    balances, b_list = calcBalances()  # посчитали балансы, теперь нужно проверить все ли > 0
    for item in b_list:    # проверка баланс (создал список балансов, если в нем есть отрицательные значения,
                           # то блокчейн не валидный)
        if item < 0:
            print("invalid")

    print("\n", balances, "\n")
    for block in blockchain:
        if prev_block:
            # сверить хэши, начиная со второго
            actual_prev_hash = dataToHash(prev_block)  # считаем хэш предыдущего блока
            recorded_prev_hash = block["previous_hash"]  # хэш записанный в блокчейне
            if not isValidHash(actual_prev_hash):
                print("blockchain is invalid, proof of work is wrong")
            if actual_prev_hash != recorded_prev_hash:
                print("Blockchain is invalid")
            else:
                print(f"valid {actual_prev_hash}")

        prev_block = block


for i in range(len(blockchain)):
    print(blockchain[i])

validBlockchain()

# blockchain[5]["amount"] = 9993021  проверка (работает ли защищенность блокчейна)
# вместо обычной dataToHash начнем использовать ф-цию майнинга mineProofOfWork, тогда все хэши будут начинаться с 0000

# 1. переписать ф-цию addNewBlock, чтобы она использовала ф-цию майнинга (done)
# 2. переписать ф-цию validBlockchain, чтобы она проверяла, что ъэш начинается с нужного кол-ва 0 (done)

# 3. посчитать балансы всех участников

print("\nbalances \n")
print(calcBalances())  # дз - проверять возможна ли транзакция validBlockchain (кол-во денег)
