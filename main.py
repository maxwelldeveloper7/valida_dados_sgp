import pandas as pd
import re
from datetime import datetime

def validar_cpf(cpf):
    cpf_str = str(cpf).strip()
    if not cpf_str.isdigit():
        return False, "CPF contém caracteres inválidos (apenas números são permitidos)"
    if len(cpf_str) != 11:
        return False, "CPF deve conter exatamente 11 dígitos numéricos"
    return True, None

def validar_nis(nis):
    nis_str = str(nis).strip()
    if not nis_str.isdigit():
        return False, "NIS contém caracteres inválidos (apenas números são permitidos)"
    if len(nis_str) != 11:
        return False, "NIS deve conter exatamente 11 dígitos numéricos"
    return True, None

def validar_data(data_str):
    try:
        datetime.strptime(str(data_str), "%d/%m/%Y")
        return True
    except:
        return False

def validar_ano(ano):
    return bool(re.fullmatch(r'\d{4}', str(ano)))

def validar_codigo(codigo, tamanho):
    return bool(re.fullmatch(r'\d{' + str(tamanho) + '}', str(codigo)))

def validar_planilha_sgp(path_arquivo):
    df = pd.read_csv(path_arquivo)
    erros = []

    for i, row in df.iterrows():
        linha = i + 2  # considerando cabeçalho na linha 1

        # CPF ou NIS obrigatórios
        cpf_valido, cpf_erro = validar_cpf(row['ESTUDANTE_CPF'])
        nis_valido, nis_erro = validar_nis(row['ESTUDANTE_NU_NIS'])

        if not (cpf_valido):
            erros.append(f"Linha {linha}: CPF inválido. Motivos: "
                         f"{cpf_erro if not cpf_valido else ''} ".strip())
            
        if not (nis_valido):
            erros.append(f"Linha {linha}: NIS inválido. Motivos: "
                        f"{nis_erro if not nis_valido else ''}".strip())

        if not isinstance(row['ESTUDANTE_NOME'], str) or not row['ESTUDANTE_NOME'].strip():
            erros.append(f"Linha {linha}: Nome do estudante obrigatório.")

        if not validar_data(row['ESTUDANTE_DT_NASCIMENTO']):
            erros.append(f"Linha {linha}: Data de nascimento inválida.")

        if not isinstance(row['ESTUDANTE_MAE_NOME'], str) or not row['ESTUDANTE_MAE_NOME'].strip():
            erros.append(f"Linha {linha}: Nome da mãe obrigatório.")

        if not (validar_codigo(row['CO_ENTIDADE'], 8) or (isinstance(row['NO_ENTIDADE'], str) and row['NO_ENTIDADE'].strip())):
            erros.append(f"Linha {linha}: Código INEP ou Nome da escola é obrigatório.")

        if not validar_data(row['DATA_INICIO_PERIODO_LETIVO']):
            erros.append(f"Linha {linha}: Data início do período letivo inválida.")
        if not validar_data(row['DATA_INICIO_MATRICULA']):
            erros.append(f"Linha {linha}: Data início da matrícula inválida.")

        if not validar_ano(row['NU_ANO_MATRICULA']):
            erros.append(f"Linha {linha}: Ano da matrícula inválido.")

        if not str(row['ESTUDANTE_ETAPA_DE_ENSINO']).isdigit():
            erros.append(f"Linha {linha}: Etapa de ensino inválida (deve ser número inteiro).")

        if row['TURMA_FORMA_ORGANIZACAO'] not in [1, 2, 3, 4, 5, 6]:
            erros.append(f"Linha {linha}: Forma de organização da turma inválida.")

        if not str(row['TURMA_ORGANIZACAO_QUANTIDADE_TOTAL']).isdigit():
            erros.append(f"Linha {linha}: Quantidade total da organização da turma inválida.")

    if erros:
        print("\nErros encontrados:")
        for erro in erros:
            print(erro)
    else:
        print("Planilha validada com sucesso, sem erros.")

# Exemplo de uso:
validar_planilha_sgp('planilha.csv')
