import pandas as pd

def get_account_value_by_code(df, cd_account):
  return float(df.loc[cd_account]['VL_CONTA']) * -1

# def get_account_value_by_description(df, ds_account):
#   value = df[df['DS_CONTA'] == ds_account]['VL_CONTA']
#   return value


# # LOAD CSV FILES
# file = '../data/processed/01_joined-2020-2020.csv'
# file_tickers = '../data/processed/04_tickers-2020-2020.csv'
# file_quotes = '../data/processed/05-quotes-2020-2020.csv'
# date = '2020-03-31'

# df_joined = pd.read_csv(file, sep=',')
# df_quotes = pd.read_csv(file_quotes, sep=',')
# df_tickers = pd.read_csv(file_tickers, sep=',')

# del df_joined['Unnamed: 0']
# del df_quotes['Unnamed: 0']
# del df_tickers['Unnamed: 0']

# cnpj = df_joined['CNPJ_CIA'][60]
# df_cnpj = df_joined[df_joined['CNPJ_CIA'] == cnpj]
# df_cnpj = df_cnpj[df_cnpj['DT_REFER'] == date]

# date_match = df_quotes['Date'] == date
# ticker = df_cnpj['TICKER'].unique()[0]
# ticker_match = df_quotes['TICKER'] == ticker

# acao_valor = float(df_quotes[date_match & ticker_match]['Adj Close'])
# acao_volume = int(df_quotes[date_match & ticker_match]['Volume'])

# print(f'ticker={ticker}')

def get_dividendo_yield(df):
  cd_dividendos_pagos = '6.01.02.11'
  # Dividend Yield (DY) = (Dividendos pagos / Preço da ação) X 100
  # ds_dividendos_pagos = 'Dividendos pagos'
  vl_dividendos_pagos = get_account_value_by_code(df, cd_dividendos_pagos)
  vl_dividendo_yield = (vl_dividendos_pagos/ float(1000)) * 100
  return vl_dividendo_yield


def get_pl(df):
  # P/L = Preço atual / Lucro por ação (LPA)
  cd_lucro_por_acao = '3.99'

  vl_lucro_por_acao = get_account_value_by_code(df, cd_lucro_por_acao)

  vl_pl = 10000 / vl_lucro_por_acao
  return vl_pl

def get_ebit(df):
  # EBIT (3.05)
  cd_ebit = '3.05'
  vl_ebit = get_account_value_by_code(df, cd_ebit)
  return vl_ebit

def get_ebitda(df):
  # EBITDA = EBIT + Amortização-Depreciação
  # EBIT (3.05)
  # Depreciação, Amortização e Exaustão (7.04.01)

  cd_depreciacao_amortizacao_e_exaustao = '7.04.01'
  vl_depreciacao_amortizacao_e_exaustao = get_account_value_by_code(df, cd_depreciacao_amortizacao_e_exaustao)
  vl_ebit = get_ebit(df)
  
  vl_ebitda = vl_ebit + vl_depreciacao_amortizacao_e_exaustao
  return vl_ebitda

def get_p_ebitda(df):
  # P/EBITDA = Preço atual / EBITDA
  vl_ebitda = get_ebitda(df)
  vl_p_ebitda = 10000 / vl_ebitda
  return vl_p_ebitda

def get_p_ebit(df):
  ## P/EBIT = Preço atual / EBIT
  vl_ebit = get_ebit(df)
  vl_p_ebit = 10000 / vl_ebit
  return vl_p_ebit

def get_ativo_circulante(df):
  cd_ativo_circulante = '1.01'
  vl_ativo_circulante = get_account_value_by_code(df, cd_ativo_circulante)
  return vl_ativo_circulante

def get_passivo_circulante(df):
  cd_passivo_circulante = '2.01'
  vl_passivo_circulante = get_account_value_by_code(df, cd_passivo_circulante)
  return vl_passivo_circulante

def get_p_cap_giro(df):
  # P/Capital de Giro = Preço da Ação / Capital de Giro por ação
  # Para encontrar o capital de giro por ação, basta encontrar o valor do ativo circulante,
  # subtrair o valor do passivo circulante e dividir o resultado pelo número total de ações emitidas.
  vl_ativo_circulante = get_ativo_circulante(df)
  vl_passivo_circulante = get_passivo_circulante(df)

  vl_cap_giro_por_acao = (vl_ativo_circulante - vl_passivo_circulante) / 1000000

  vl_p_cap_giro = acao_valor / vl_cap_giro_por_acao
  return vl_p_cap_giro

def get_p_ativo_circulante_liquido(df):
  # P/ACL = Preço da Ação / Ativos Circulantes Líquidos por ação
  # Ativos Circulantes Líquidos por ação = Ativos circulantes / quantidade de ações
  vl_ativo_circulante = get_ativo_circulante(df)
  vl_ativos_circulantes_liq_por_acao = vl_ativo_circulante / 10000000

  vl_p_ativos_circulantes_liq = 10000 / vl_ativos_circulantes_liq_por_acao
  return vl_p_ativos_circulantes_liq

def get_patrimonio_liquido(df):
  cd_patrimonio_liquido = '2.03'
  vl_patrimonio_liquido = get_account_value_by_code(df, cd_patrimonio_liquido)
  return vl_patrimonio_liquido

def get_vpa(df):
  # VPA = Patrimônio líquido / Nº de ações
  vl_patrimonio_liquido = get_patrimonio_liquido(df)
  vl_vpa = vl_patrimonio_liquido / 100000
  return vl_vpa

def get_pvp():
  # P/VP = Preço atual / VPA
  vl_vpa = get_vpa()
  vl_p_vp = 10000 / vl_vpa
  return vl_p_vp

def get_p_ativo(df):
  # P/Ativo = Preço da ação / Valor Contábil por ação
  # TODO: Valor contábil da empresa
  # Valor contábil por ação = Valor contábil da empresa / Total de ações em circulação

  vl_contabil_da_empresa = 1000000000
  vl_contabil_por_acao = vl_contabil_da_empresa / 10000

  vl_p_ativo = 10000 / vl_contabil_por_acao
  return vl_p_ativo

def get_ev(df):
  # Ativos Não-Operacionais = "Outros Ativos Não Operacionais"
  ### Caixa e equivalente de caixa (1.01.01)
  # Capitalização = Valor do mercado = Valor de uma ação x Número de ações existentes
  # Dívida = Balanço patrimonial = Passivo + Patrimônio líquido
  # EV = Capitalização + Dívida – Caixa e Equivalentes – Ativos Não-Operacionais

  cd_caixa_e_equivalente = '1.01.01'
  cd_ativos_nao_operacionais = '1.02.01.10.04'
  # ds_ativos_nao_operacionais = 'Outros Ativos Não Operacionais'

  vl_ativos_nao_operacionais = get_account_value_by_code(df, cd_ativos_nao_operacionais)
  vl_caixa_e_equivalente = get_account_value_by_code(df, cd_caixa_e_equivalente)
                                
  vl_capitalizacao = 10000 * 100000
  # vl_divida = vl_passivo_total + get_patrimonio_liquido()
  vl_divida = get_patrimonio_liquido()

  vl_ev = vl_capitalizacao + vl_divida - vl_caixa_e_equivalente - vl_ativos_nao_operacionais
  return vl_ev

def get_ev_ebitda(df):
  # EV/EBITDA = EV / EBITDA

  vl_ev_ebitda = get_ev(df) / get_ebitda(df)
  return vl_ev_ebitda

def get_ev_ebit(df):
  # EV/EBIT = EV / EBIT
  vl_ev_ebit = get_ev(df) / get_ebit(df)
  return vl_ev_ebit

def get_lucro_liquido(df):
  cd_lucro_liquido = '3.11'
  vl_lucro_liquido = get_account_value_by_code(df, cd_lucro_liquido)
  return vl_lucro_liquido

def get_lpa(df):
  # LPA  = Lucro líquido / Nº de ações

  vl_lpa = get_lucro_liquido(df) / 10000
  return vl_lpa

def get_receita_liquida(df):
  cd_receita_liquida = '3.01'
  vl_receita_liquida = get_account_value_by_code(df, cd_receita_liquida)
  return vl_receita_liquida

def get_psr(df):
  # PSR = Preço da Ação / Receita Líquida por Ação
  acao_valor_total = 10000 * 100000

  vl_psr = acao_valor_total / get_receita_liquida(df)
  return vl_psr

# def get_pvp():
#   ## P/VP = Preço atual / VPA
#   vl_p_vp = acao_valor / get_vpa()
#   return vl_p_vp

def get_roe(df):
  #ROE = Lucro Líquido (3.11) / Patrimônio Líquido (2.03)
  vl_roe = get_lucro_liquido(df) / get_patrimonio_liquido(df)
  return vl_roe

def get_ativo_total(df):
  cd_ativo_total = '1'
  vl_ativo_total = get_account_value_by_code(df, cd_ativo_total)
  return vl_ativo_total

def get_roa(df):
  #ROA = Lucro Líquido (3.11) / Ativo Total (1) 
  vl_roa = get_lucro_liquido(df) / get_ativo_total(df)
  return vl_roa

def get_divida_bruta(df):
  cd_emprestimos = '2.01.04'
  cd_financiamentos = '2.02.01'
  vl_emprestimos = get_account_value_by_code(df, cd_emprestimos)
  vl_financiamentos = get_account_value_by_code(df, cd_financiamentos)

  vl_endividamento = vl_financiamentos + vl_emprestimos
  vl_endividamento
  return vl_endividamento

def get_roic(df):
  #ROIC = (EBIT - Impostos) / (Patrimônio Líquido + Endividamento)
  #Imposto de Renda e Contribuição Social sobre o Lucro (3.08) = Impostos
  #Dívida Bruta = Empréstimos e Financiamentos (2.01.04 + 2.02.01) = Endividamento

  cd_imposto = '3.08'
  vl_imposto = get_account_value_by_code(df, cd_imposto)
  vl_roic = (get_ebit(df) - vl_imposto) / (get_patrimonio_liquido(df) + get_divida_bruta(df))
  return vl_roic

def get_lucro_bruto(df):
  cd_lucro_bruto = '3.03'
  vl_lucro_bruto = get_account_value_by_code(df, cd_lucro_bruto)
  return vl_lucro_bruto

def get_m_bruta(df):
  #Margem Bruta = Lucro Bruto / Receita Líquida
  vl_margem_bruta = (get_lucro_bruto(df) / get_receita_liquida(df))
  return vl_margem_bruta

def get_m_liquida(df):
  #Margem Líquida = Lucro Líquido / Receita Líquida
  vl_margem_liquida = (get_lucro_liquido(df) / get_receita_liquida(df))
  return vl_margem_liquida

def get_m_ebit(df):
  #Margem EBIT = EBIT / Receita Líquida
  vl_margem_ebit = get_ebit(df) / get_receita_liquida(df)
  return vl_margem_ebit

def get_m_ebitda(df):
  #Margem EBITDA = EBITDA / Receita Líquida
  vl_margem_ebitda = get_ebitda(df) / get_receita_liquida(df)
  return vl_margem_ebitda

def get_divida_liquida(df):
  # Caixa e Equivalente de Caixa (1.01.01)
  # Aplicações Finaceiras (1.01.02)
  # Aplicações Financeiras Avaliadas a Valor Justo através do Resultado (1.02.01.01)
  # Dívida Líquida = Dívida Bruta - (Caixa e Equivalente de Caixa + Aplicações Finaceiras + 1.02.01.01)
  cd_caixa_e_equivalente_de_caixa = '1.01.01'
  cd_aplicacoes_financeiras = '1.01.01'
  cd_aplicacoes_financeiras_avaliadas_a_valor_justo = '1.02.01.01'

  vl_caixa_e_equivalente_de_caixa = get_account_value_by_code(df, cd_caixa_e_equivalente_de_caixa)
  vl_aplicacoes_financeiras = get_account_value_by_code(df, cd_aplicacoes_financeiras)
  vl_aplicacoes_financeiras_avaliadas_a_valor_justo = get_account_value_by_code(df, cd_aplicacoes_financeiras_avaliadas_a_valor_justo)

  vl_divida_liquida = get_divida_bruta(df) - (vl_caixa_e_equivalente_de_caixa + vl_aplicacoes_financeiras + vl_aplicacoes_financeiras_avaliadas_a_valor_justo)
  return vl_divida_liquida

def get_div_liquida_pl(df):
  # Dív. Líquida/PL = Dívida Líquida/Patrimônio Líquido
  vl_divida_liquida_por_pl = get_divida_liquida(df) / get_patrimonio_liquido(df)
  return vl_divida_liquida_por_pl

def get_div_liquida_ebit(df):
  # Dív. Líquida/EBIT = Dívida Líquida/EBIT
  vl_divida_liquida_por_ebit = get_divida_liquida(df) / get_ebit(df)
  return vl_divida_liquida_por_ebit

def get_div_liquida_ebitda(df):
  # Dív. Líquida/EBIT = Dívida Líquida/EBIT
  vl_divida_liquida_por_ebitda = get_divida_liquida(df) / get_ebitda(df)
  return vl_divida_liquida_por_ebitda

def get_liq_corrente(df):
  ## 4. LIQ. CORRENTE = Ativo Circulante / Passivo Circulante
  vl_liquido_corrente = get_ativo_circulante(df) / get_passivo_circulante(df)
  return vl_liquido_corrente

def get_pl_ativos(df):
  # PL/ATIVOS = Patrimônio Líquido / Ativos
  vl_pl_ativos = get_patrimonio_liquido(df) / get_ativo_total(df)
  return vl_pl_ativos

def get_passivo_total(df):
  cd_passivo_total = '2'
  vl_passivo_total = get_account_value_by_code(df, cd_passivo_total)
  return vl_passivo_total

def get_passivos_ativos(df):
  ## PASSIVOS/ATIVOS = Passivos / Ativos
  vl_passivos_ativos = get_passivo_total(df) / get_ativo_total(df)
  return vl_passivos_ativos


def process_indicators(df):
  date = df['DT_REFER'].max()
  # df.set_index('CD_CONTA', inplace=True)

  for cnpj in df['CNPJ_CIA'].unique():
    selecao_cnpj = df['CNPJ_CIA'] == cnpj
    selecao_data = df['DT_REFER'] == date
    cnpj_df = df[selecao_cnpj & selecao_data]

    row = {
        'cnpj': cnpj,
        'date': date,
        'dy': get_dividendo_yield(cnpj_df),
        'pl': get_pl(cnpj_df),
        'pvp': get_pvp(cnpj_df),
        'evebitda': get_ev_ebitda(cnpj_df),
        'evebit': get_ev_ebit(cnpj_df),
        'pebitda': get_p_ebitda(cnpj_df),
        'pebit': get_p_ebit(cnpj_df),
        'vpa': get_vpa(cnpj_df),
        'pativo': get_p_ativo(cnpj_df),
        'lpa': get_lpa(cnpj_df),
        'psr': get_psr(cnpj_df),
        'pcapgiro': get_p_cap_giro(cnpj_df),
        'pativcirqliq': get_p_ativo_circulante_liquido(cnpj_df),
        'dlpl': get_div_liquida_pl(cnpj_df),
        'dlebit': get_div_liquida_ebit(cnpj_df),
        'dlebitda': get_div_liquida_ebitda(cnpj_df),
        'plativos': get_pl_ativos(cnpj_df),
        'passivosativos': get_passivos_ativos(cnpj_df),
        'liqcorrente': get_liq_corrente(cnpj_df),
        'mbruta': get_m_bruta(cnpj_df),
        'mebit': get_m_ebit(cnpj_df),
        'mebitda': get_m_ebitda(cnpj_df),
        'mliquida': get_m_liquida(cnpj_df),
        'roe': get_roe(cnpj_df),
        'roa': get_roa(cnpj_df),
        'roic': get_roic(cnpj_df),
    }
    print(row)
    # for i, row in cnpj_df.iterrows():
    #   value = get_account_value_by_code(cnpj_df, i)
    #   print(f'type={type(value)} value={value}')



# df = pd.DataFrame()
# df = df.append(row, ignore_index=True)
# df.to_csv('./data/teste.csv')

# if __name__ == '__main__':
#     process()
