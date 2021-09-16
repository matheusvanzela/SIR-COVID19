# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 12:32:11 2020

@author: mathe

Modelagem matemática do problema COVID-19

Metodologia SIR - Considera o balanço entre suscetíveis, infectados e removidos
baseado em modelo de taxas diferenciais

Fontes:
A data de estudo é 29 de março de 2020
A fonte de dados sobre o número de infectados é:
https://www.worldometers.info/coronavirus/#countries
Alguns números foram obtidos via IBGE

"""
import matplotlib.pyplot as plt, numpy as np

#condições iniciais
N = 210000000
S = N                       #população brasileira estimada 
I = 1                    #número de infectados 
R = 0                       #número de recuperados
D = 0                     #número inicial de mortos

#Parâmetros do modelo
beta = 0.4/N               #beta = probabilidade de contágio x número de contato per capita por unidade de tempo
gama = 1/10                 #gama = taxa de recuperação por unidade de tempo (aproximadamente 15 dias)

#Adaptações realizadas
FatorReducional = 1         #fator reducional pelo isolamento/medo
Letalidade = 0.025          #fator de letalidade
LetalSemCuidados = 0.04     #fator de letalidade sem cuidados
FatorHospital = 1/3        #fator de hospitalização 
leitos = 200000000000       #capacidade do sistema hospitalar

dias = 200                   #horizonte de projeção

#Inicialização de vetores
Is = np.zeros(dias-1)       #inicializar o vetor de infectados
Rs = np.zeros(dias-1)       #inicializar o vetor de recuperados
ctrle = np.zeros(dias-1)    #vetor de controle dos índices
Hs = np.zeros(dias-1)       #inicializar o vetor dos hospitalizados (Proporcão dos infectados)
Ds = np.zeros(dias-1)       #inicializar o vetor dos mortos
c = np.ones(dias-1)*leitos  #inicializar um vetor com a capacidade dos leitos de acordo com o período

for i in range (1,dias):
    #define qual o beta e qual a letalidade na iteração
    #fr = FatorReducional*0.85 if D/I > 0.05 else FatorReducional
    #beta = beta*fr                                         
    l = Letalidade if FatorHospital * I <= leitos else LetalSemCuidados
    #gama = gama*1.15 if I>500000 else gama
    #print(fr)
    
    #modelagem SIR
    dS = -beta*S*I                      #atualização dos suscetíveis
    dI = beta*S*I - gama*I              #atualização dos infectados
    dR = gama*I - gama*l*I                   #atualização dos recuperados considerando a retirada dos mortos
    dD = gama*l*I
    
    #aplicando as variações (deltas) para suscetíveis, mortos, recuperados e infectados
    S += dS
    I += dI
    R += dR
    D += dD
    
    #atualizando os vetores de S, M, R, I e ctrle
    Is[i-1] = I
    Rs[i-1] = R
    Ds[i-1] = D
    Hs[i-1] = I*FatorHospital
    ctrle[i-1] = i
    #cálculo sem o número de mortes
    print("Dia %i - Infectados: %i Recuperados: %i" % (i, I, R))
    #print("Dia %i - Infectados: %i Mortos: %i" % (i, I, D))

plt.plot(ctrle, Is)
#plt.plot(ds, Hs)
plt.plot(ctrle, Rs)
#plt.plot(ctrle, Ds)
#plt.plot(ds, c)

#cálculo sem o núemro de mortes
plt.legend(("Infectados", "Recuperados"))


#plt.legend(("Infectados", "Recuperados", "Mortes"))

plt.show()



