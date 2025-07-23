import random 
import string
from blockchain import Chain

def randomLote():
    letters = ''.join(random.choices(string.ascii_uppercase, k=4))  # Gera 4 letras maiúsculas
    numbers = ''.join(random.choices(string.digits, k=3))  # Gera 3 números
    return f"boi_{letters}_{numbers}"  # Formato boi_LLLL_NNN

def randomAnimal(name): 
    process = str((random.randint(1,20))) # Gera os possiveis processos que o boi pode passar (1-20)
    return f"{name}-{process}" # Formato requerido 


def criar_teste(animal):
    obj_animal = Chain(animal) 
    for i in range(5):  
        processo_animal = randomAnimal(animal)
        obj_animal.new_block(processo_animal)
    return obj_animal  # Agora retorna o objeto criado
