import hashlib
import json

income = [100, 200, 3000, 1000]
balance = sum(income)

bank_account = {
    "name": "Tim",
    "balance": balance,
    "date": "27-01-2004"

}

print(bank_account["balance"])

text = "hello"
binary = text.encode()  # преобразуем к бинарным данным
print(binary)
print(hashlib.sha256(binary))  # считаем хэш
print(hashlib.sha256(binary).hexdigest())

print(bank_account)

json_data = json.dumps(bank_account)  # приводим словарь к строке в формате json
print(json_data)
binary_data = json_data.encode()  # приводим строку к бинарным данным
print(hashlib.sha256(binary_data).hexdigest())  # хэш словаря


def dataToHash(data):  # написали функцию, которая возвращает хэш каких-либо данных
    json_Data = json.dumps(data)
    binary_Data = json_Data.encode()
    return hashlib.sha256(binary_Data).hexdigest()


print(dataToHash(bank_account))

# BLOCKCHAIN

blockchain = [  # в нашем случае это список транзакций
                # нужен первый пустой блок из-за особенности блокчейна
                # (всегда считать хэш предлыдущего блока)
    {
        "from": "",  # кто отправил
        "to": "",  # кому отправил(а)
        "amount": 0.0  # сколько отправили
    }
]


def addNewBlock(account_from, account_to, amount):  # добавить запись/блок в блокчейн
    block = {
        "from": account_from,
        "to": account_to,
        "amount": amount
    }
    blockchain.append(block)

addNewBlock("Vasya", "Kolya", 1000)

print(blockchain)