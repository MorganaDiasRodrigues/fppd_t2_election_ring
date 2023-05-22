import threading

class Processo(threading.Thread):
    def __init__(self, processo_id):
        super(Processo, self).__init__()
        self.processo_id = processo_id
        self.coordenador_id = None
        self.ativo = True
        self.proximo_processo = None
        self.recebendo_mensagem = threading.Event()

    def enviar_mensagem(self, mensagem, proximo_processo):
        if self.processo_id == None:
            print(f"[Enviar mensagem] Mensagem do Controler")
            self.receber_mensagem(mensagem)
        else:
            if self.proximo_processo.ativo == False:
                print(f'[Enviar mensagem] Processo atual P{self.processo_id} tem seu próximo como falho. Pulando...')
                proximo_processo.proximo_processo.receber_mensagem(mensagem)
                print(f'[Enviar mensagem] Processo atual P{self.processo_id} enviará para P{proximo_processo.proximo_processo.processo_id}')
            else:
                proximo_processo.receber_mensagem(mensagem)
                print(f'[Enviar mensagem] Processo atual P{self.processo_id} enviará para P{proximo_processo.processo_id}')


    def receber_mensagem(self, mensagem):
        print(f'[Receber mensagem] Lendo mensagem...')
        self.recebendo_mensagem.set()
        if mensagem['tipo'] == 'eleicao':
            print(f'[Receber mensagem] A mensagem recebida de P{self.processo_id} é eleição')
            self.processar_mensagem_eleicao(mensagem)

        elif mensagem['tipo'] == 'coordenador':
            print(f'[Receber mensagem] A mensagem recebida de P{self.processo_id} é sobre o novo coordenador')
            self.processar_mensagem_coordenador(mensagem)

        elif mensagem['tipo'] == 'falhar':
            print(f'[Receber mensagem] A mensagem recebida é do Controler e é sobre uma falha')
            for processo in mensagem['processos']:
                if processo.processo_id == mensagem['id']:
                    processo.ativo = False
                    print(f'O processo P{processo.processo_id} agora está falho (Ativo = {processo.ativo})')
                if processo.processo_id == mensagem['id'] == processo.coordenador_id:
                    print("O coordenador está falho.")
                    for processo in mensagem['processos']:
                        if processo.processo_id != processo.coordenador_id:
                            print(f"Processo que vai chamar a eleição: {processo.processo_id}")
                            processo.iniciar_eleicao()
                            break

    def processar_mensagem_eleicao(self, mensagem):
        if len(mensagem["caminho"]) <= 3:
            if self.ativo == False:
                mensagem['caminho'].append(self.processo_id)
                self.enviar_mensagem(mensagem, self.proximo_processo)
            else:
                mensagem['caminho'].append(self.processo_id)
                mensagem['ids'].append(self.processo_id)
                self.enviar_mensagem(mensagem, self.proximo_processo)
        
        else:
            if max(mensagem["ids"]) == self.processo_id:
                print(f'O maior ID entre os processos ativos é {max(mensagem["ids"])}')
                self.tornar_coordenador(max(mensagem["ids"]))

    def processar_mensagem_coordenador(self, mensagem):
        if self.ativo == False:
            ...
        else:
            self.coordenador_id = mensagem['id']
            print("[Mensagem coordenador] Processo P{} recebeu mensagem do novo coordenador: {}".format(self.processo_id, self.coordenador_id))
            if self.processo_id in mensagem["caminho"]:
                ...
            else:
                if self.proximo_processo.proximo_processo.ativo == True:
                    mensagem["caminho"].append(self.processo_id)
                    self.enviar_mensagem(mensagem, self.proximo_processo)
                else:
                    mensagem["caminho"].append(self.processo_id)

    def iniciar_eleicao(self):
        mensagem = {'tipo': 'eleicao', 'id': self.processo_id, 'caminho': [], "ids":[]}
        self.enviar_mensagem(mensagem, self.proximo_processo)

    def tornar_coordenador(self, max_processo_id):
        self.coordenador_id = max_processo_id
        mensagem = {'tipo': 'coordenador', 'id': self.coordenador_id, "caminho":[self.processo_id]}
        self.enviar_mensagem(mensagem, self.proximo_processo)
        print(f"Novo coordenador é P{self.coordenador_id}")

    def set_proximo_processo(self, proximo_processo):
        self.proximo_processo = proximo_processo

    def set_processo_coord(self, id_processo_coord:int):
        self.coordenador_id = id_processo_coord
        
    def get_processo_id(self):
        return self.processo_id
    
    def get_coordenador_id(self):
        return self.coordenador_id
