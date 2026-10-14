from flask import Flask, render_template, request

app = Flask(__name__)

# Rota raiz da aplicação, renderiza o formulário para o usuário inserir os dados.
@app.route('/')
def index():
    return render_template('form.html')
# Rota que executa o cálculo com base nos dados inseridos pelo usuário.
@app.route('/resultado', methods=['POST'])

# Função que retorna o resultado do cálculo de sálario para o usuário pela rota "/resultado".
def resultado():

    # Tratamento de erro, caso o usuário digite dados inválidos.
    try:
        salario = float(request.form['salario'].replace(',','.'))
        dependentes = int(request.form['dependentes'])
    except ValueError:
        return "Erro: Insira valores válidos. Ex: Salário = 1000,00 | Dependentes = 1"

    # Calculo salário liquido

    #Valores constantes usados para os cálculos.
    INSS = 0.08
    IR = 0.15
    VALOR_POR_DEPENDENTE = 200.00
    SALARIO_ISENTO_IR = 2500.00

    # Descontos no salário.
    desc_INSS = salario * INSS
    desc_IR = salario * IR
    
    # Valor dedutivel para salários acima do limite de Isenção do Imposto de Renda
    deducao_por_dependente = dependentes * VALOR_POR_DEPENDENTE

    # Válidações feitas para evitar valores negativos.
    if salario < 0 :
        return "Erro: O salário bruto não pode ser negativo. Ex.: 2500.00"
    elif dependentes < 0 :
        return "Erro: O número de dependentes não pode ser negativo. Ex.: 2"

    # Cálculo para salários isentos.
    resultado = salario - desc_INSS + deducao_por_dependente

    # Cálculos para salários acima do limite de isenção.
    if salario > SALARIO_ISENTO_IR :
        resultado = resultado - desc_IR

    return f"Salário liquido: R$ {resultado:.2f}".replace('.',',')

if __name__ == '__main__':
    app.run(debug=True)
