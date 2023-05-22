from controler import Controler
from processo import Processo
# Criação dos processos
print("Cirando processos... \n")
processo1 = Processo(1)
processo2 = Processo(2)
processo3 = Processo(3)
processo4 = Processo(4)
print("Processos criados \n")
# Construindo o anel
processo1.set_proximo_processo(processo2)
processo2.set_proximo_processo(processo3)
processo3.set_proximo_processo(processo4)
processo4.set_proximo_processo(processo1)
print("Anel de processos criado \n")
# Controler/Processo externo
controler = Controler([processo1, processo2, processo3, processo4])
print(f'Processos em controle: {controler.get_ids_processos()}')
# Processo coordenador
id_processo_coord = 2
print(f"O processo coordenador é: P{id_processo_coord}")
for processo in controler.processos:
 processo.set_processo_coord(id_processo_coord)
# Simulação da falha de um processo
faz_falhar = controler.faz_falhar(2)
controler.enviar_mensagem(faz_falhar, None)
# Iniciar a execução dos processos em threads separadas
processo1.start()
processo2.start()
processo3.start()
processo4.start()
# Aguardar a finalização dos processos
processo1.join()
processo2.join()
processo3.join()
processo4.join()