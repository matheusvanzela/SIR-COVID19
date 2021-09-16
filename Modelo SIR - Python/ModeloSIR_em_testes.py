# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 22:01:52 2020

@author: mathe
"""

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
beta = 0.2/N               #beta = probabilidade de contágio x número de contato per capita por unidade de tempo
gama = 1/10                 #gama = taxa de recuperação por unidade de tempo (aproximadamente 15 dias)

#Adaptações realizadas
Letalidade = 0.005           #fator de letalidade
LetalSemCuidados = 0.021      #fator de letalidade sem cuidados

dias = 200                   #horizonte de projeção

#Inicialização de vetores
Is = np.zeros(dias-1)       #inicializar o vetor de infectados
Rs = np.zeros(dias-1)       #inicializar o vetor de recuperados
ctrle = np.zeros(dias-1)    #vetor de controle dos índices
Ds = np.zeros(dias-1)       #inicializar o vetor dos mortos
c = np.ones(dias-1)*leitos  #inicializar um vetor com a capacidade dos leitos de acordo com o período

for i in range (1,dias):
    #define qual o beta e qual a letalidade na iteração
    l = Letalidade 
        
    #modelagem SIR
    dS = -beta*S*I                      #atualização dos suscetíveis
    dI = beta*S*I - gama*I              #atualização dos infectados
    dR = gama*I - gama*l*I          #atualização dos recuperados considerando a retirada dos mortos
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
    ctrle[i-1] = i
    
    print("Dia %i - Infectados: %i Mortos: %i" % (i, I, D))
    

plt.plot(ctrle, Is)
#plt.plot(ds, Hs)
plt.plot(ctrle, Rs)
plt.plot(ctrle, Ds)
#plt.plot(ds, c)
plt.legend(("Infectados", "Recuperados", "Mortes"))

plt.show()