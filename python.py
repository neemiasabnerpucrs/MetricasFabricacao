import datetime
from datetime import timedelta
import csv

def datetime_range(start, end):
    current = start
    while current < end:
        yield current
        current += timedelta(minutes=1)

class Ocorrencia:
    def __init__(self,dados):
        self.codigo = dados[0]
        
        self.chegada = datetime.datetime.strptime(dados[1].replace(',','.'), '%Y-%m-%d %H:%M:%S.%f')
        self.start = datetime.datetime.strptime(dados[2].replace(',','.'), '%Y-%m-%d %H:%M:%S.%f')
        self.finish = datetime.datetime.strptime(dados[4].replace(',','.'), '%Y-%m-%d %H:%M:%S.%f')
        self.cor = dados[6]
        self.situacao = dados[8]
        self.maquina = dados[9]

    def espera(self):
        return (self.start - self.chegada).total_seconds()
    def tempo_ciclo(self):
        return (self.finish - self.start).total_seconds()
    def minutos_operando(self):
        return [dt.strftime('%Y-%m-%d %H:%M') for dt in datetime_range(self.start, self.finish)]


class Faculdade:
    def __init__(self):
        self.Todas = []

    def add_tudo(self,maquina):
        self.Todas = maquina

    def add_ocorrencia(self,ocorrido):
        self.Todas.append(ocorrido)
    
    def retorna_maquina(self,numero):
        retorno = []
        for evento in self.Todas:
            if(int(evento.maquina) == numero):
                retorno.append(evento)
        return retorno
    def todos_ciclos(self):
        retorno = 0
        for evento in self.Todas:
            retorno = retorno + evento.tempo_ciclo()
        return timedelta(seconds=retorno)
    
    def atendidas(self):
        retorno = 0;
        for evento in self.Todas:
            if(int(evento.situacao) == 2):
                retorno = retorno + 1
        return retorno

    def defeituosas(self):
        retorno = 0;
        for evento in self.Todas:
            if(not int(evento.situacao) == 2):
                retorno = retorno + 1
        return retorno
    
    def media_espera(self):
        retorno = 0
        for i in self.Todas:
            retorno = retorno + i.espera()
        return (retorno/len(self.Todas))


PUCRS = Faculdade()

with open('Lote (mvu).csv',newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
    for row in spamreader:
        if(row[0]=='codigo'):
            #print("pulando primeira linha")
            pass
        else:
            PUCRS.add_ocorrencia(Ocorrencia(row))



###########################
########CONSULTAS##########
###########################

print("MLT = " + str(PUCRS.todos_ciclos()))
print(f'Atendidas = {PUCRS.atendidas()} e Não Atendidas = {PUCRS.defeituosas()} Eficiencia = {round(PUCRS.atendidas()*100/(PUCRS.defeituosas()+PUCRS.atendidas()),2)}')
print("Tc médio = " + str(PUCRS.todos_ciclos()/PUCRS.atendidas()))
print(f"Media Espera = {round(PUCRS.media_espera()/3600,2)} horas")
print("----------------------------------")




for i in range(1,4):
    maquina = Faculdade()
    maquina.add_tudo(PUCRS.retorna_maquina(i))
    print(f"Maquina {i}")
    print(f'MLT = {maquina.todos_ciclos()}')
    print(f'Atendidas = {maquina.atendidas()} e Não Atendidas = {maquina.defeituosas()} Eficiencia = {round(maquina.atendidas()*100/(maquina.defeituosas()+maquina.atendidas()),2)}')
    print("Tc médio = " + str(maquina.todos_ciclos()/maquina.atendidas()))
    print(f"Media Espera = {round(maquina.media_espera()/3600,2)} horas")
    print("--------------------------------")