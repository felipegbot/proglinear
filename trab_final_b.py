from pymprog import * # importando a biblioteca

# Dados de entrada

Min = [ # número mínimo de funcionários por hora (24 horas separados em 6 períodos)
  20, 20, 20, 20,  # 0h-4h
  30, 30, 30, 30,  # 4h-8h
  50, 50, 50, 50,  # 8h-12h
  45, 45, 45, 45,  # 12h-16h
  60, 60, 60, 60,  # 16h-20h
  40, 40, 40, 40,  # 20h-24h
]

N = [ # fator multiplicativo do custo por hora a ser pago (24 horas)
  1.2, 1.2, 1.2, 1.2,   # 0h-4h
  1.2, 1, 1, 1,         # 4h-8h
  1, 1, 1, 1,           # 8h-12h
  1, 1, 1, 1,           # 12h-16h
  1, 1, 1, 1,           # 16h-20h
  1, 1, 1.2, 1.2,       # 20h-24h
]

Max = 5 # número máximo de entradas de funcionários

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
  y[i] == sum(x[a] for a in range(i-5,i))

  sum(e[i] for i in range(n)) <= Max # número máximo de entradas de funcionários (Max)

  x[i] <= e[i] * (sum(Min[a % n] for a in range(i, i+5)))

  # número mínimo de funcionários
  y[i] >= Min[i]

solve()

for i in range(n):
  print("Hora %d: %d funcionários entraram e %d funcionários estão trabalhando" % (i, x[i].primal, y[i].primal))
  if(i > 22 or i < 5):
    horas_trabalhadas_noturno += y[i].primal
  else:
    horas_trabalhadas_diurno += y[i].primal
print('\n')
print("horas trabalhadas durante o período diurno: ", horas_trabalhadas_diurno)
print("horas trabalhadas durante o período noturno: ", horas_trabalhadas_noturno)

print('\n')
print("valor do período diurno: ", (horas_trabalhadas_diurno * 1))
print("valor do período noturno: ", (horas_trabalhadas_noturno * 1.2))
print('\n')

end() # finaliza o modelo