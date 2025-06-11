class Chain: # Classe 
    def __init__(self,name):
        self.chain = [] # Lista armazenando operacoes do ativo
        self.name = name # Parametro de criacao do objeto - codigo boi (a ser usado posteriormente)
        self.first_block()
    
    def create_block(self,previous_hash):
        block = { # dicionario com as carac que queremos para cada bloco DA CHAIN/LISTA 
            'index':len(self.chain) + 1, # Guardar posicao 
            'name': self.name, # Nome do bloco
            'timestamp': str(datetime.datetime.now()), # Hora Bloco
            'previous_hash': previous_hash # Hash do bloco anterior 
            }
        block['hash'] = self.hashId(block)  # Gera o hash com as informacoes do bloco todo (+ seguro)
        self.chain.append(block)
        return block
    
    def first_block(self,previous_hash='00000'):
        block = self.create_block(previous_hash)
        return block

    # def new_block(self,name):
        self.name = name
        previous_block = self.previous_block()
        previous_hash = previous_block['hash']
        self.create_block(previous_hash)
    
    def new_block(self, process):
        previous_block = self.previous_block()
        previous_hash = previous_block['hash']
        self.name = process
        block = self.create_block(previous_hash)

    # def hashId(self,string): # Criamos o codigo para Hash 
        # encoded_str = string.encode() # Transformamos em Bytes
        # return hashlib.sha256(encoded_str).hexdigest() # Entendendo melhor sobre hexdigest apenas sei que e necessario
    
    def hashId(self, block_data):
        encoded_str = json.dumps(block_data, sort_keys=True).encode()
        return hashlib.sha256(encoded_str).hexdigest()   
    
    def previous_block(self):
        return self.chain[-1] # Retornamos o ultimo bloco da lista 
    
    def show_chain(self):
        response ={
            'tamanho': len(self.chain), # Lemos o tamanho da lista e retornamos 
            'cadeia': self.chain # Printamos a lista 
        }
        return response
    
    def search_hash(self,hash):
        for block in self.chain:
            try:
                if block['hash'] == hash:
                    return self.show_chain()
            except Exception as e:
                continue 
    
        return "O registro nao existe"