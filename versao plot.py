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
    def minutos_operando(self,tipo):
        if(tipo==0):
            return [dt.strftime('%Y-%m-%d %H:%M') for dt in datetime_range(self.start, self.finish)]
        elif(tipo==1 and int(self.situacao)==2):
            return [dt.strftime('%Y-%m-%d %H:%M') for dt in datetime_range(self.start, self.finish)]
        elif(tipo==2 and int(self.situacao)!=2):
            return [dt.strftime('%Y-%m-%d %H:%M') for dt in datetime_range(self.start, self.finish)]
        else:
            return []

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
        return str(timedelta(seconds=retorno))
    
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
    def minutos_operando(self,tipo):
        retorno = []
        for i in self.Todas:
            retorno = retorno + i.minutos_operando(tipo)
        return retorno


PUCRS = Faculdade()

with open('Lote (mvu).csv',newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
    for row in spamreader:
        if(row[0]=='codigo'):
            print("pulando primeira linha")
        else:
            PUCRS.add_ocorrencia(Ocorrencia(row))


###########################
########CONSULTAS##########
###########################
print("Tc = " + PUCRS.todos_ciclos())
print("Atendidas = " + str(PUCRS.atendidas()))
print("-------------------------------------")



MinutosON = []
MinutosRUIM = []
for i in range(1,4):
    maquina = Faculdade()
    maquina.add_tudo(PUCRS.retorna_maquina(i))
    print(f'Maquina {i} = {maquina.todos_ciclos()}')
    print(f'Atendidas = {maquina.atendidas()}')
    print(f'Erro = {maquina.defeituosas()}')
    MinutosON.append(maquina.minutos_operando(0))
    MinutosRUIM.append(maquina.minutos_operando(2))
    print("--------------------------------")

InicioLote = datetime.datetime.strptime("2022-05-12 00:00", '%Y-%m-%d %H:%M')
FinalLote = datetime.datetime.strptime("2022-06-07 23:59", '%Y-%m-%d %H:%M')

T = [dt.strftime('%Y-%m-%d %H:%M') for dt in datetime_range(InicioLote, FinalLote)]
AA=[]
BB=[]
CC=[]

AA2=[]
BB2=[]
CC2=[]



for i in T:
    if(i in MinutosON[0]):
        AA.append(1)
    else:
        AA.append(0)
    if(i in MinutosON[1]):
        BB.append(1)
    else:
        BB.append(0)
    if(i in MinutosON[2]):
        CC.append(1)
    else:
        CC.append(0)
    if(i in MinutosRUIM[0]):
        AA2.append(1)
    else:
        AA2.append(0)
    if(i in MinutosRUIM[1]):
        BB2.append(1)
    else:
        BB2.append(0)
    if(i in MinutosRUIM[2]):
        CC2.append(1)
    else:
        CC2.append(0)
    
import plotly.express as px

fig = px.imshow([AA,BB,CC],y=['Maquina 1','Maquina 2','Maquina 3'],height=500)
fig.show()

fig2 = px.imshow([[ (a + b) for a, b in zip(AA, AA2) ],[ (a + b) for a, b in zip(BB, BB2) ],[ (a + b) for a, b in zip(CC, CC2) ]],y=['Maquina 1','Maquina 2','Maquina 3'],color_continuous_scale=[[0, 'rgb(13, 8, 135)'], [0.5, 'rgb(240,249,33)'], [1.0, 'red']],height=500)
fig2.show()