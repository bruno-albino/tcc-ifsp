import pandas as pd

def get_account_value_by_code(df, cd_account):
    value = df[df['CD_CONTA'] == cd_account]['VL_CONTA']
    return value

def get_account_value_by_description(df, ds_account):
  value = df[df['DS_CONTA'] == ds_account]['VL_CONTA']
  return value


# LOAD CSV FILES
file = '../data/processed/01_joined-2020-2020.csv'
file_tickers = '../data/processed/04_tickers-2020-2020.csv'
file_quotes = '../data/processed/05-quotes-2020-2020.csv'
date = '2020-03-31'

df_joined = pd.read_csv(file, sep=',')
df_quotes = pd.read_csv(file_quotes, sep=',')
df_tickers = pd.read_csv(file_tickers, sep=',')

del df_joined['Unnamed: 0']
del df_quotes['Unnamed: 0']
del df_tickers['Unnamed: 0']

cnpj = df_joined['CNPJ_CIA'][60]
df_cnpj = df_joined[df_joined['CNPJ_CIA'] == cnpj]
df_cnpj = df_cnpj[df_cnpj['DT_REFER'] == date]

date_match = df_quotes['Date'] == date
ticker = df_cnpj['TICKER'].unique()[0]
ticker_match = df_quotes['TICKER'] == ticker

acao_valor = float(df_quotes[date_match & ticker_match]['Adj Close'])
acao_volume = int(df_quotes[date_match & ticker_match]['Volume'])

print(f'ticker={ticker}')

def get_dividendo_yield():
  # Dividend Yield (DY) = (Dividendos pagos / Preço da ação_ X 100
  ds_dividendos_pagos = 'Dividendos pagos'

  amount_dividendos_pagos = get_account_value_by_description(df_cnpj, ds_dividendos_pagos)
  vl_dividendos_pagos = sum(amount_dividendos_pagos)
  vl_dividendo_yield = (vl_dividendos_pagos/ float(acao_valor)) * 100

  print(f'Dividendos pagos no período = {vl_dividendos_pagos}')
  print(f'Lucro por ação = {acao_valor}')
  print(f'D.Y = {vl_dividendo_yield} ')
  return vl_dividendo_yield


def get_pl():
  # P/L = Preço atual / Lucro por ação (LPA)
  cd_lucro_por_acao = '3.99'

  vl_lucro_por_acao = float(get_account_value_by_code(df_cnpj, cd_lucro_por_acao))

  vl_pl = acao_valor
  if vl_lucro_por_acao != 0:
      vl_pl = acao_valor / vl_lucro_por_acao
          
  print(f'Preço da ação = {acao_valor}')
  print(f'L.P.A = {vl_lucro_por_acao}')
  print(f'P/L = {vl_pl}')
  return vl_pl

def get_ebit():
  # EBIT (3.05)
  cd_ebit = '3.05'
  vl_ebit = float(get_account_value_by_code(df_cnpj, cd_ebit))
  print(f'EBIT = {vl_ebit}')
  return vl_ebit

def get_ebitda():
  # EBITDA = EBIT + Amortização-Depreciação
  # EBIT (3.05)
  # Depreciação, Amortização e Exaustão (7.04.01)

  cd_depreciacao_amortizacao_e_exaustao = '7.04.01'
  vl_depreciacao_amortizacao_e_exaustao = float(get_account_value_by_code(df_cnpj, cd_depreciacao_amortizacao_e_exaustao))
  vl_ebit = get_ebit()
  
  vl_ebitda = vl_ebit + vl_depreciacao_amortizacao_e_exaustao
  print(f'Depreciacao, Amortização e Exaustão = {vl_depreciacao_amortizacao_e_exaustao}')
  print(f'EBIT = {vl_ebit}')
  print(f'EBITDA = {vl_ebitda}')
  return vl_ebitda

def get_p_ebitda():
  # P/EBITDA = Preço atual / EBITDA
  vl_ebitda = get_ebitda()
  vl_p_ebitda = acao_valor / vl_ebitda
  print(f'Preço da ação = {acao_valor}')
  print(f'EBITDA = {vl_ebitda}\n')
  print(f'P/EBITDA = {vl_p_ebitda}')
  return vl_p_ebitda

def get_p_ebit():
  ## P/EBIT = Preço atual / EBIT
  vl_ebit = get_ebit()
  vl_p_ebit = acao_valor / vl_ebit

  print(f'Preço da ação = {acao_valor}')
  print(f'EBIT = {vl_ebit}\n')
  print(f'P/EBITDA = {vl_p_ebit}')
  return vl_p_ebit

def get_ativo_circulante():
  cd_ativo_circulante = '1.01'
  vl_ativo_circulante = float(get_account_value_by_code(df_cnpj, cd_ativo_circulante))
  return vl_ativo_circulante

def get_passivo_circulante():
  cd_passivo_circulante = '2.01'
  vl_passivo_circulante = float(get_account_value_by_code(df_cnpj, cd_passivo_circulante))
  return vl_passivo_circulante

def get_p_cap_giro():
  # P/Capital de Giro = Preço da Ação / Capital de Giro por ação
  # Para encontrar o capital de giro por ação, basta encontrar o valor do ativo circulante,
  # subtrair o valor do passivo circulante e dividir o resultado pelo número total de ações emitidas.
  vl_ativo_circulante = get_ativo_circulante()
  vl_passivo_circulante = get_passivo_circulante()

  vl_cap_giro_por_acao = (vl_ativo_circulante - vl_passivo_circulante) / acao_volume

  vl_p_cap_giro = acao_valor / vl_cap_giro_por_acao

  print(f'Preço da ação = {acao_valor}')
  print(f'Volume da ação = {acao_volume}')

  print(f'Ativo circulante = {vl_ativo_circulante}')
  print(f'Passivo circulante = {vl_passivo_circulante}')
  print(f'Capitao de Giro por ação = {vl_cap_giro_por_acao}\n')

  print(f'P/CAP. GIRO = {vl_p_cap_giro}')
  return vl_p_cap_giro

def get_p_ativo_circulante_liquido():
  # P/ACL = Preço da Ação / Ativos Circulantes Líquidos por ação
  # Ativos Circulantes Líquidos por ação = Ativos circulantes / quantidade de ações
  vl_ativo_circulante = get_ativo_circulante()
  vl_ativos_circulantes_liq_por_acao = vl_ativo_circulante / acao_volume

  vl_p_ativos_circulantes_liq = acao_valor / vl_ativos_circulantes_liq_por_acao

  print(f'Preço da ação = {acao_valor}')
  print(f'Volume da ação = {acao_volume}')

  print(f'Ativo circulante = {vl_ativo_circulante}')
  print(f'Ativos circulantes líquidos por ação = {vl_ativos_circulantes_liq_por_acao}\n')

  print(f'P/ATIV. CIRC. LIQ = {vl_p_ativos_circulantes_liq}')
  return vl_p_ativos_circulantes_liq

def get_patrimonio_liquido():
  cd_patrimonio_liquido = '2.03'
  vl_patrimonio_liquido = float(get_account_value_by_code(df_cnpj, cd_patrimonio_liquido))
  return vl_patrimonio_liquido

def get_vpa():
  # VPA = Patrimônio líquido / Nº de ações
  vl_patrimonio_liquido = get_patrimonio_liquido()
  vl_vpa = vl_patrimonio_liquido / acao_volume

  print(f'Patrimônio líquido = {vl_patrimonio_liquido}')
  print(f'Quantidade de ações = {acao_volume}\n')

  print(f'VPA = {vl_vpa}')
  return vl_vpa

def get_pvp():
  # P/VP = Preço atual / VPA
  vl_vpa = get_vpa()
  vl_p_vp = acao_valor / vl_vpa
  print(f'Preço ação = {acao_valor}')
  print(f'VPA = {vl_vpa}\n')

  print(f'P/VP = {vl_p_vp}')

def get_p_ativo():
  # P/Ativo = Preço da ação / Valor Contábil por ação
  # TODO: Valor contábil da empresa
  # Valor contábil por ação = Valor contábil da empresa / Total de ações em circulação

  vl_contabil_da_empresa = 1000000000
  vl_contabil_por_acao = vl_contabil_da_empresa / acao_volume

  vl_p_ativo = acao_valor / vl_contabil_por_acao

  print(f'Valor contábil da empresa = {vl_contabil_da_empresa}')
  print(f'Volume de ações = {acao_volume}')
  print(f'Valor da ação = {acao_valor}\n')

  print(f'P/Ativo = {vl_p_ativo}')

def get_ev():
  # Ativos Não-Operacionais = "Outros Ativos Não Operacionais"
  ### Caixa e equivalente de caixa (1.01.01)
  # Capitalização = Valor do mercado = Valor de uma ação x Número de ações existentes
  # Dívida = Balanço patrimonial = Passivo + Patrimônio líquido
  # EV = Capitalização + Dívida – Caixa e Equivalentes – Ativos Não-Operacionais

  cd_caixa_e_equivalente = '1.01.01'
  ds_ativos_nao_operacionais = 'Outros Ativos Não Operacionais'

  vl_ativos_nao_operacionais = sum(get_account_value_by_description(df_cnpj, ds_ativos_nao_operacionais))
  vl_caixa_e_equivalente = float(get_account_value_by_code(df_cnpj, cd_caixa_e_equivalente))
                                
  vl_capitalizacao = acao_valor * acao_volume
  vl_divida = vl_passivo_total + get_patrimonio_liquido()


  vl_ev = vl_capitalizacao + vl_divida - vl_caixa_e_equivalente - vl_ativos_nao_operacionais

  print(f'Capitalização = {vl_capitalizacao}')
  print(f'Dívidas = {vl_divida}')
  print(f'Caixa = {vl_caixa_e_equivalente}')
  print(f'Ativos não operacionais = {vl_ativos_nao_operacionais}\n')

  print(f'Enterprise value (EV) = {vl_ev}')
  return vl_ev

def get_ev_ebitda():
  # EV/EBITDA = EV / EBITDA

  vl_ev_ebitda = get_ev() / get_ebitda()
  print(f'EV/EBITDA = {vl_ev_ebitda}')
  return vl_ev_ebitda

def get_ev_ebit():
  # EV/EBIT = EV / EBIT
  vl_ev_ebit = get_ev() / get_ebit()
  print(f'EV/EBIT = {vl_ev_ebit}')
  return vl_ev_ebit

def get_lucro_liquido():
  cd_lucro_liquido = '3.11'
  vl_lucro_liquido = float(get_account_value_by_code(df_cnpj, cd_lucro_liquido))
  return vl_lucro_liquido

def get_lpa():
  # LPA  = Lucro líquido / Nº de ações

  vl_lpa = get_lucro_liquido() / acao_volume
  return vl_lpa

def get_receita_liquida():
  cd_receita_liquida = '3.01'
  vl_receita_liquida = float(get_account_value_by_code(df_cnpj, cd_receita_liquida))
  return vl_receita_liquida

def get_psr():
  # PSR = Preço da Ação / Receita Líquida por Ação
  acao_valor_total = acao_valor * acao_volume

  vl_psr = acao_valor_total / get_receita_liquida()
  print(f'P/SR = {vl_psr}')
  return vl_psr

def get_pvp():
  ## P/VP = Preço atual / VPA
  vl_p_vp = acao_valor / get_vpa()
  return vl_p_vp

def get_roe():
  #ROE = Lucro Líquido (3.11) / Patrimônio Líquido (2.03)
  vl_roe = get_lucro_liquido() / get_patrimonio_liquido()
  return vl_roe

def get_ativo_total():
  cd_ativo_total = '1'
  vl_ativo_total = float(get_account_value_by_code(df_cnpj, cd_ativo_total))
  return vl_ativo_total

def get_roa():
  #ROA = Lucro Líquido (3.11) / Ativo Total (1) 
  vl_roa = get_lucro_liquido() / get_ativo_total()
  return vl_roa

def get_divida_bruta():
  cd_emprestimos = '2.01.04'
  cd_financiamentos = '2.02.01'
  vl_emprestimos = float(get_account_value_by_code(df_cnpj, cd_emprestimos))
  vl_financiamentos = float(get_account_value_by_code(df_cnpj, cd_financiamentos))

  vl_endividamento = vl_financiamentos + vl_emprestimos
  vl_endividamento
  return vl_endividamento

def get_roic():
  #ROIC = (EBIT - Impostos) / (Patrimônio Líquido + Endividamento)
  #Imposto de Renda e Contribuição Social sobre o Lucro (3.08) = Impostos
  #Dívida Bruta = Empréstimos e Financiamentos (2.01.04 + 2.02.01) = Endividamento

  cd_imposto = '3.08'
  vl_imposto = float(get_account_value_by_code(df_cnpj, cd_imposto)) * -1
  vl_roic = (get_ebit() - vl_imposto) / (get_patrimonio_liquido() + get_divida_bruta())
  return vl_roic

def get_lucro_bruto():
  cd_lucro_bruto = '3.03'
  vl_lucro_bruto = float(get_account_value_by_code(df_cnpj, cd_lucro_bruto))
  return vl_lucro_bruto

def get_m_bruta():
  #Margem Bruta = Lucro Bruto / Receita Líquida
  vl_margem_bruta = (get_lucro_bruto() / get_receita_liquida())
  return vl_margem_bruta

def get_m_liquida():
  #Margem Líquida = Lucro Líquido / Receita Líquida
  vl_margem_liquida = (get_lucro_liquido() / get_receita_liquida())
  return vl_margem_liquida

def get_m_ebit():
  #Margem EBIT = EBIT / Receita Líquida
  vl_margem_ebit = get_ebit() / get_receita_liquida()
  return vl_margem_ebit

def get_m_ebitda():
  #Margem EBITDA = EBITDA / Receita Líquida
  vl_margem_ebitda = get_ebitda() / get_receita_liquida()
  return vl_margem_ebitda

def get_divida_liquida():
  # Caixa e Equivalente de Caixa (1.01.01)
  # Aplicações Finaceiras (1.01.02)
  # Aplicações Financeiras Avaliadas a Valor Justo através do Resultado (1.02.01.01)
  # Dívida Líquida = Dívida Bruta - (Caixa e Equivalente de Caixa + Aplicações Finaceiras + 1.02.01.01)
  cd_caixa_e_equivalente_de_caixa = '1.01.01'
  cd_aplicacoes_financeiras = '1.01.01'
  cd_aplicacoes_financeiras_avaliadas_a_valor_justo = '1.02.01.01'

  vl_caixa_e_equivalente_de_caixa = float(get_account_value_by_code(df_cnpj, cd_caixa_e_equivalente_de_caixa))
  vl_aplicacoes_financeiras = float(get_account_value_by_code(df_cnpj, cd_aplicacoes_financeiras))
  vl_aplicacoes_financeiras_avaliadas_a_valor_justo = float(get_account_value_by_code(df_cnpj, cd_aplicacoes_financeiras_avaliadas_a_valor_justo)) 

  vl_divida_liquida = get_divida_bruta() - (vl_caixa_e_equivalente_de_caixa + vl_aplicacoes_financeiras + vl_aplicacoes_financeiras_avaliadas_a_valor_justo)
  return vl_divida_liquida

def get_div_liquida_pl():
  # Dív. Líquida/PL = Dívida Líquida/Patrimônio Líquido
  vl_divida_liquida_por_pl = get_divida_liquida() / get_patrimonio_liquido()
  return vl_divida_liquida_por_pl

def get_div_liquida_ebit():
  # Dív. Líquida/EBIT = Dívida Líquida/EBIT
  vl_divida_liquida_por_ebit = get_divida_liquida() / get_ebit()
  return vl_divida_liquida_por_ebit

def get_div_liquida_ebitda():
  # Dív. Líquida/EBIT = Dívida Líquida/EBIT
  vl_divida_liquida_por_ebitda = get_divida_liquida() / get_ebitda()
  return vl_divida_liquida_por_ebitda

def get_liq_corrente():
  ## 4. LIQ. CORRENTE = Ativo Circulante / Passivo Circulante
  vl_liquido_corrente = get_ativo_circulante() / get_passivo_circulante()
  return vl_liquido_corrente

def get_pl_ativos():
  # PL/ATIVOS = Patrimônio Líquido / Ativos
  vl_pl_ativos = get_patrimonio_liquido() / get_ativo_total()
  return vl_pl_ativos

def get_passivo_total():
  cd_passivo_total = '2'
  vl_passivo_total = float(get_account_value_by_code(df_cnpj, cd_passivo_total))
  return vl_passivo_total

def get_passivos_ativos():
  ## PASSIVOS/ATIVOS = Passivos / Ativos
  vl_passivos_ativos = get_passivo_total() / get_ativo_total()
  return vl_passivos_ativos


row = {
    'cnpj': cnpj,
    'date': date,
    'dy': get_dividendo_yield(),
    'pl': get_pl(),
    'pvp': get_pvp(),
    'evebitda': get_ev_ebitda(),
    'evebit': get_ev_ebit(),
    'pebitda': get_p_ebitda(),
    'pebit': get_p_ebit(),
    'vpa': get_vpa(),
    'pativo': get_p_ativo(),
    'lpa': get_lpa(),
    'psr': get_psr(),
    'pcapgiro': get_p_cap_giro(),
    'pativcirqliq': get_p_ativo_circulante_liquido(),
    'dlpl': get_div_liquida_pl(),
    'dlebit': get_div_liquida_ebit(),
    'dlebitda': get_div_liquida_ebitda(),
    'plativos': get_pl_ativos(),
    'passivosativos': get_passivos_ativos(),
    'liqcorrente': get_liq_corrente(),
    'mbruta': get_m_bruta(),
    'mebit': get_m_ebit(),
    'mebitda': get_m_ebitda(),
    'mliquida': get_m_liquida(),
    'roe': get_roe(),
    'roa': get_roa(),
    'roic': get_roic(),
}

df = pd.DataFrame()
df = df.append(row, ignore_index=True)
df.to_csv('./data/teste.csv')
