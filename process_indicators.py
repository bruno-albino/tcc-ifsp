from utils import get_indicators_path, get_processed_path, get_quotes_path
import pandas as pd
import yfinance as yf

def get_quotes_quantity(df):
  vl_quotes_quantity = df['QUOTES_QUANTITY'].unique()[0]

  if vl_quotes_quantity == None:
    vl_quotes_quantity = 0

  return vl_quotes_quantity

def get_book_value(df):
  vl_book_value = df['BOOK_VALUE'].unique()[0]
  return vl_book_value

def get_account_value_by_code(df, cd_account):
  try:
    result = float(df.loc[cd_account]['VL_CONTA'])
    if result < 0:
      result = result * -1

    return result
  except KeyError:
    print(f'Account not found: {cd_account}')
    return 0

def get_quote_value_by_defer_date(df):
  df_quotes = pd.read_csv(get_quotes_path())
  date = df['DT_REFER'].max()
  ticker = list(df['TICKER'])[0]
  selecao_ticker = df_quotes['TICKER'] == ticker
  selecao_date = df_quotes['Date'] == date
  df_quotes_ticker_date = df_quotes[selecao_ticker & selecao_date].reset_index()

  acao_valor = 0.0

  if not df_quotes_ticker_date.empty:
    acao = df_quotes_ticker_date.iloc[0]
    acao_valor = float(acao['Adj Close'])
  return acao_valor

def get_dividendo_yield(df):
  vl_dividendo_yield = df['DY'].unique()[0]
  return vl_dividendo_yield
  # cd_dividendos_pagos = '6.01.02.11'
  # # Dividend Yield (DY) = (Dividendos pagos / Preço da ação) X 100
  # # ds_dividendos_pagos = 'Dividendos pagos'
  # acao_valor = get_quote_value_by_defer_date(df)
  # vl_dividendos_pagos = get_account_value_by_code(df, cd_dividendos_pagos)

  # if vl_dividendos_pagos == 0 or acao_valor == 0:
  #   return 0

  # vl_dividendo_yield = ( vl_dividendos_pagos / acao_valor) * 100
  # return vl_dividendo_yield

def get_pl(df):
  # P/L = Preço atual / Lucro por ação (LPA)
  cd_lucro_por_acao = '3.99'

  vl_lucro_por_acao = get_account_value_by_code(df, cd_lucro_por_acao)
  acao_valor = get_quote_value_by_defer_date(df)

  if vl_lucro_por_acao <= 0.0:
    return vl_lucro_por_acao

  vl_pl = acao_valor / vl_lucro_por_acao
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
  acao_valor = get_quote_value_by_defer_date(df)

  if vl_ebitda == 0:
    return vl_ebitda

  vl_p_ebitda = acao_valor / vl_ebitda
  return vl_p_ebitda

def get_p_ebit(df):
  ## P/EBIT = Preço atual / EBIT
  vl_ebit = get_ebit(df)
  acao_valor = get_quote_value_by_defer_date(df)

  if vl_ebit == 0:
    return vl_ebit

  vl_p_ebit = acao_valor / vl_ebit
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
  acao_valor = get_quote_value_by_defer_date(df)
  vl_quotes_quantity = get_quotes_quantity(df)

  if vl_quotes_quantity == 0:
    return vl_quotes_quantity

  vl_cap_giro_por_acao = (vl_ativo_circulante - vl_passivo_circulante) / vl_quotes_quantity

  vl_p_cap_giro = acao_valor / vl_cap_giro_por_acao
  return vl_p_cap_giro

def get_p_ativo_circulante_liquido(df):
  # P/ACL = Preço da Ação / Ativos Circulantes Líquidos por ação
  # Ativos Circulantes Líquidos por ação = Ativos circulantes / quantidade de ações
  vl_ativo_circulante = get_ativo_circulante(df)
  acao_valor = get_quote_value_by_defer_date(df)
  vl_quotes_quantity = get_quotes_quantity(df)

  if vl_quotes_quantity == 0:
    return vl_quotes_quantity
    
  vl_ativos_circulantes_liq_por_acao = vl_ativo_circulante / vl_quotes_quantity

  vl_p_ativos_circulantes_liq = acao_valor / vl_ativos_circulantes_liq_por_acao
  return vl_p_ativos_circulantes_liq

def get_patrimonio_liquido(df):
  cd_patrimonio_liquido = '2.03'
  vl_patrimonio_liquido = get_account_value_by_code(df, cd_patrimonio_liquido)
  return vl_patrimonio_liquido

def get_vpa(df):
  # VPA = Patrimônio líquido / Nº de ações
  vl_patrimonio_liquido = get_patrimonio_liquido(df)
  vl_quotes_quantity = get_quotes_quantity(df)

  if vl_quotes_quantity == 0:
    return vl_quotes_quantity

  vl_vpa = vl_patrimonio_liquido / vl_quotes_quantity
  return vl_vpa

def get_pvp(df):
  # P/VP = Preço atual / VPA
  vl_vpa = get_vpa(df)
  acao_valor = get_quote_value_by_defer_date(df)

  if vl_vpa == 0:
    return vl_vpa

  vl_p_vp = acao_valor / vl_vpa
  return vl_p_vp

def get_p_ativo(df):
  # P/Ativo = Preço da ação / Valor Contábil por ação
  # Valor contábil por ação = Valor contábil da empresa / Total de ações em circulação
  acao_valor = get_quote_value_by_defer_date(df)
  vl_quotes_quantity = get_quotes_quantity(df)
  vl_book_value = get_book_value(df)

  if vl_quotes_quantity == 0:
    return vl_quotes_quantity

  vl_contabil_por_acao = vl_book_value / vl_quotes_quantity

  vl_p_ativo = acao_valor / vl_contabil_por_acao
  return vl_p_ativo

def get_ev(df):
  vl_ev = df['EV'].unique()[0]
  return vl_ev
  # Ativos Não-Operacionais = "Outros Ativos Não Operacionais"
  ### Caixa e equivalente de caixa (1.01.01)
  # Capitalização = Valor do mercado = Valor de uma ação x Número de ações existentes
  # Dívida = Balanço patrimonial = Passivo + Patrimônio líquido
  # EV = Capitalização + Dívida – Caixa e Equivalentes – Ativos Não-Operacionais

  # cd_caixa_e_equivalente = '1.01.01'
  # cd_ativos_nao_operacionais = '1.02.01.10.04'
  # # ds_ativos_nao_operacionais = 'Outros Ativos Não Operacionais'

  # vl_ativos_nao_operacionais = get_account_value_by_code(df, cd_ativos_nao_operacionais)
  # vl_caixa_e_equivalente = get_account_value_by_code(df, cd_caixa_e_equivalente)
  # acao_valor = get_quote_value_by_defer_date(df)
  # vl_patrimonio_liquido = get_patrimonio_liquido(df)
  # vl_passivo_total = get_passivo_total(df)
                                
  # vl_capitalizacao = acao_valor * get_quotes_quantity(df)
  # vl_divida = vl_passivo_total + vl_patrimonio_liquido

  # vl_ev = vl_capitalizacao + vl_divida - vl_caixa_e_equivalente - vl_ativos_nao_operacionais
  # return vl_ev

def get_ev_ebitda(df):
  # EV/EBITDA = EV / EBITDA

  vl_ebitda = get_ebitda(df)
  vl_ev = get_ev(df)

  if vl_ev == 0:
    return vl_ev

  vl_ev_ebitda = vl_ev / vl_ebitda
  return vl_ev_ebitda

def get_ev_ebit(df):
  # EV/EBIT = EV / EBIT
  vl_ev = get_ev(df)
  vl_ebit = get_ebit(df)

  if vl_ebit == 0:
    return vl_ebit

  vl_ev_ebit = vl_ev / vl_ebit
  return vl_ev_ebit

def get_lucro_liquido(df):
  cd_lucro_liquido = '3.11'
  vl_lucro_liquido = get_account_value_by_code(df, cd_lucro_liquido)
  return vl_lucro_liquido

def get_lpa(df):
  # LPA  = Lucro líquido / Nº de ações
  vl_lucro_liquido = get_lucro_liquido(df)
  vl_quotes_quantity = get_quotes_quantity(df)

  if vl_quotes_quantity == 0:
    return vl_quotes_quantity

  vl_lpa = vl_lucro_liquido / vl_quotes_quantity
  return vl_lpa

def get_receita_liquida(df):
  cd_receita_liquida = '3.01'
  vl_receita_liquida = get_account_value_by_code(df, cd_receita_liquida)
  return vl_receita_liquida

def get_psr(df):
  # PSR = Preço da Ação / Receita Líquida por Ação
  acao_valor = get_quote_value_by_defer_date(df)
  acao_valor_total = acao_valor * get_quotes_quantity(df)
  vl_receita_liquida = get_receita_liquida(df)

  if vl_receita_liquida == 0:
    return vl_receita_liquida

  vl_psr = acao_valor_total / vl_receita_liquida
  return vl_psr

def get_roe(df):
  #ROE = Lucro Líquido (3.11) / Patrimônio Líquido (2.03)
  vl_lucro_liquido = get_lucro_liquido(df)
  vl_patrimonio_liquido = get_patrimonio_liquido(df)

  if vl_patrimonio_liquido == 0:
    return vl_patrimonio_liquido

  vl_roe = vl_lucro_liquido / vl_patrimonio_liquido
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
  vl_ebit = get_ebit(df)
  vl_patrimonio_liquido = get_patrimonio_liquido(df)
  vl_divida_bruta = get_divida_bruta(df)

  vl_ebit_imposto = vl_ebit - vl_imposto
  vl_patrimonio_liquido_divida_bruta = vl_patrimonio_liquido + vl_divida_bruta

  if vl_patrimonio_liquido_divida_bruta == 0:
    return vl_patrimonio_liquido_divida_bruta

  vl_roic = vl_ebit_imposto / vl_patrimonio_liquido_divida_bruta
  return vl_roic

def get_lucro_bruto(df):
  cd_lucro_bruto = '3.03'
  vl_lucro_bruto = get_account_value_by_code(df, cd_lucro_bruto)
  return vl_lucro_bruto

def get_m_bruta(df):
  #Margem Bruta = Lucro Bruto / Receita Líquida
  vl_lucro_bruto = get_lucro_bruto(df)
  vl_receita_liquida = get_receita_liquida(df)

  if vl_receita_liquida == 0.0:
    return vl_receita_liquida

  vl_margem_bruta = vl_lucro_bruto / vl_receita_liquida
  return vl_margem_bruta

def get_m_liquida(df):
  #Margem Líquida = Lucro Líquido / Receita Líquida
  vl_lucro_liquido = get_lucro_liquido(df)
  vl_receita_liquida = get_receita_liquida(df)
  
  if vl_receita_liquida == 0:
    return vl_receita_liquida
  
  vl_margem_liquida = vl_lucro_liquido / vl_receita_liquida
  return vl_margem_liquida

def get_m_ebit(df):
  #Margem EBIT = EBIT / Receita Líquida
  vl_ebit = get_ebit(df)
  vl_receita_liquida = get_receita_liquida(df)

  if vl_receita_liquida == 0:
    return vl_receita_liquida

  vl_margem_ebit = vl_ebit / vl_receita_liquida
  return vl_margem_ebit

def get_m_ebitda(df):
  #Margem EBITDA = EBITDA / Receita Líquida
  vl_ebitda = get_ebitda(df)
  vl_receita_liquida = get_receita_liquida(df)

  if vl_receita_liquida == 0:
    return vl_receita_liquida

  vl_margem_ebitda = vl_ebitda / vl_receita_liquida
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
  vl_divida_liquida = get_divida_liquida(df)
  vl_patrimonio_liquido = get_patrimonio_liquido(df)

  vl_divida_liquida_por_pl = vl_divida_liquida / vl_patrimonio_liquido
  return vl_divida_liquida_por_pl

def get_div_liquida_ebit(df):
  # Dív. Líquida/EBIT = Dívida Líquida/EBIT
  vl_divida_liquida = get_divida_liquida(df)
  vl_ebit = get_ebit(df)

  if vl_ebit == 0:
    return vl_ebit

  vl_divida_liquida_por_ebit = vl_divida_liquida / vl_ebit
  return vl_divida_liquida_por_ebit

def get_div_liquida_ebitda(df):
  # Dív. Líquida/EBIT = Dívida Líquida/EBIT
  vl_divida_liquida = get_divida_liquida(df)
  vl_ebitda = get_ebitda(df)

  if vl_ebitda == 0:
    return vl_ebitda

  vl_divida_liquida_por_ebitda = vl_divida_liquida / vl_ebitda
  return vl_divida_liquida_por_ebitda

def get_liq_corrente(df):
  ## 4. LIQ. CORRENTE = Ativo Circulante / Passivo Circulante
  vl_ativo_circulante = get_ativo_circulante(df)
  vl_passivo_circulante = get_passivo_circulante(df)

  if vl_passivo_circulante == 0:
    return vl_passivo_circulante

  vl_liquido_corrente =  vl_ativo_circulante / vl_passivo_circulante
  return vl_liquido_corrente

def get_pl_ativos(df):
  # PL/ATIVOS = Patrimônio Líquido / Ativos
  vl_ativos = get_ativo_total(df)
  vl_patrimonio_liquido = get_patrimonio_liquido(df)

  if vl_ativos == 0:
    return vl_ativos

  vl_pl_ativos = vl_patrimonio_liquido / vl_ativos
  return vl_pl_ativos

def get_passivo_total(df):
  cd_passivo_total = '2'
  vl_passivo_total = get_account_value_by_code(df, cd_passivo_total)
  return vl_passivo_total

def get_passivos_ativos(df):
  ## PASSIVOS/ATIVOS = Passivos / Ativos
  vl_ativos = get_ativo_total(df)
  vl_passivos = get_passivo_total(df)

  if vl_ativos == 0:
    return vl_ativos

  vl_passivos_ativos = vl_passivos / vl_ativos
  return vl_passivos_ativos


def download_remaining_data(df):
  ticker = df.iloc[0].TICKER
  result = yf.Ticker(f'{ticker}.SA')

  try:
    df['EV'] = result.info['enterpriseValue']
  except KeyError:
    df['EV'] = 0

  try:
    df['QUOTES_QUANTITY'] = result.info['sharesOutstanding']
  except KeyError:
    df['QUOTES_QUANTITY'] = 0

  try:
    df['DY'] = result.info['dividendYield']
  except KeyError:
    df['DY'] = 0
  
  try:
    df['BOOK_VALUE'] = result.info['bookValue']
  except KeyError:
    df['BOOK_VALUE'] = 0

  return df

def process_indicators():
  print('Start process indicators')
  path = get_processed_path()
  df = pd.read_csv(path)
  df.dropna(inplace=True)
  date = df['DT_REFER'].max()

  df_indicators = pd.DataFrame()

  for cnpj in df['CNPJ_CIA'].unique()[:20]:
    selecao_cnpj = df['CNPJ_CIA'] == cnpj
    df_cnpj = df[selecao_cnpj]
    selecao_data = df_cnpj['DT_REFER'] == date
    df_cnpj = df_cnpj[selecao_data].reset_index()

    if not df_cnpj.empty:
      df_cnpj = download_remaining_data(df_cnpj)
      companyName = df_cnpj['DENOM_CIA'].unique()[0]
      df_cnpj.set_index('CD_CONTA', inplace=True)

      row = {
          'cnpj': cnpj,
          'company': companyName,
          'date': date,
          'dy': get_dividendo_yield(df_cnpj),
          'pl': get_pl(df_cnpj),
          'pvp': get_pvp(df_cnpj),
          'evebitda': get_ev_ebitda(df_cnpj),
          'evebit': get_ev_ebit(df_cnpj),
          'pebitda': get_p_ebitda(df_cnpj),
          'pebit': get_p_ebit(df_cnpj),
          'vpa': get_vpa(df_cnpj),
          'pativo': get_p_ativo(df_cnpj),
          'lpa': get_lpa(df_cnpj),
          'psr': get_psr(df_cnpj),
          'pcapgiro': get_p_cap_giro(df_cnpj),
          'pativcirqliq': get_p_ativo_circulante_liquido(df_cnpj),
          'dlpl': get_div_liquida_pl(df_cnpj),
          'dlebit': get_div_liquida_ebit(df_cnpj),
          'dlebitda': get_div_liquida_ebitda(df_cnpj),
          'plativos': get_pl_ativos(df_cnpj),
          'passivosativos': get_passivos_ativos(df_cnpj),
          'liqcorrente': get_liq_corrente(df_cnpj),
          'mbruta': get_m_bruta(df_cnpj),
          'mebit': get_m_ebit(df_cnpj),
          'mebitda': get_m_ebitda(df_cnpj),
          'mliquida': get_m_liquida(df_cnpj),
          'roe': get_roe(df_cnpj),
          'roa': get_roa(df_cnpj),
          'roic': get_roic(df_cnpj),
      }
      print(f'Empresa {cnpj} carregada')
      df_indicators = df_indicators.append(row, ignore_index=True)

  df_indicators.to_csv(get_indicators_path())

if __name__ == "__main__":
  process_indicators()
