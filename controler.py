import threading
from processo import Processo

class Controler(Processo):
    def __init__(self, processos:list):
        self.processo_id = None
        self.processos = processos
        self.recebendo_mensagem = threading.Event()

    def faz_falhar(self, id:int):
        print(f"Processo para falhar: P{id}")
        faz_falhar = {'tipo':'falhar', 'id': id, "ativo": False, 'processos': self.processos}
        return faz_falhar

    def get_ids_processos(self):
        ids = []
        for processo in self.processos:
            ids.append(processo.get_processo_id())
        return ids