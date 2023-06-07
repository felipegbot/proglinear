from pymprog import * # importando a biblioteca
import sys

# Dados de entrada
Max = 0 # número máximo de entradas de funcionários
M = [] # número mínimo de funcionários por hora (24 horas separados em 6 períodos)

# Abrindo o arquivo indicado
with open(sys.argv[1], 'r') as f:
  # Lendo o arquivo
  data = f.readlines()

  # Pegando o número máximo de entradas de funcionários
  Max = int(data[0].strip())

  # Preenchendo o vetor que contém o mínimo de funcionários por hora
  for i in range(1,len(data)):
    # Insere o mínimo de funcionários 4 vezes por período, pois o vetor foi separado em horas
    for j in range(4):
      M.append(int(data[i].strip()))
  f.close()

N = [ # fator multiplicativo do custo por hora a ser pago (24 horas)
  1.2, 1.2, 1.2, 1.2,   # 0h-4h
  1.2, 1, 1, 1,         # 4h-8h
  1, 1, 1, 1,           # 8h-12h
  1, 1, 1, 1,           # 12h-16h
  1, 1, 1, 1,           # 16h-20h
  1, 1, 1.2, 1.2,       # 20h-24h
]

n = 24 # número de horas

horas_trabalhadas_diurno = 0
horas_trabalhadas_noturno = 0

begin('trabalho final item b') # inicia o modelo

# Variáveis de decisão
y = var('y', n) # número de funcionários que estão trabalhando na hora i
x = var('x', n) # número de funcionários que entraram na hora i
e = var('e', n, bool) # variável de controle que diz se houve entrada de funcionários ou não na hora i


# Função objetivo
minimize(
  sum(y[i] * N[i] for i in range(n)) # custo total
)

# Restrições
for i in range(n):
  # número de funcionários que estão trabalhando
  y[i] == sum(x[a] for a in range(i-5,i+1))

  sum(e[i] for i in range(n)) <= Max # número máximo de entradas de funcionários (Max)

  x[i] <= e[i] * (sum(M[a % n] for a in range(i, i+6)))

  # número mínimo de funcionários
  y[i] >= M[i]

solve()

for i in range(n):
  print("Hora %d: %d funcionários entraram e %d funcionários estão trabalhando" % (i, x[i].primal, y[i].primal))
  if(i >= 22 or i < 5):
    horas_trabalhadas_noturno += y[i].primal
  else:
    horas_trabalhadas_diurno += y[i].primal
print('\n')
print("solucao otima", round(vobj()))
print("horas trabalhadas durante o período diurno: ", round(horas_trabalhadas_diurno))
print("horas trabalhadas durante o período noturno: ", round(horas_trabalhadas_noturno))
print("horas trabalhadas totais: ", round(sum(y[i].primal for i in range(n))))
print('\n')
print("valor do período diurno: ", round(horas_trabalhadas_diurno * 1))
print("valor do período noturno: ", round(horas_trabalhadas_noturno * 1.2))
print("valor total: ", round((horas_trabalhadas_diurno * 1) + (horas_trabalhadas_noturno * 1.2)))
print('\n')
end() # finaliza o modelo