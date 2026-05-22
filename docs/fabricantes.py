import requests
from app.auth import obter_autenticacao
from app.config import (
    DISENGAGEMENT_FILE,
    LINK_FILE,
    LINK_PROD,
    PREFIX_CATP,
    ROOT_CPF_CNPJ,
    URL_MANUFACTURER_LINK,
)
from app.logger import error, info, separator, success
from app.reporting import gerar_relatorio
from app.utils import auth_headers, load_json_file, normalize_json, response_payload


def vincula_fabricante():
    set_token, x_csrf_token = obter_autenticacao()
    dados = load_json_file(LINK_FILE)
    fabricantes = dados if isinstance(dados, list) else [dados]

    resultados, sucesso, falha = [], 0, 0
    total = len(fabricantes)

    for i, fabricante in enumerate(fabricantes, start=1):
        codigo_produto = fabricante.get("codigoProduto")
        codigo_operador = fabricante.get("codigoOperadorEstrangeiro")
        print(
            info,
            f"{i} de {total} - Enviando vínculo: produto={codigo_produto}, operador={codigo_operador}",
        )

        try:
            response = requests.post(
                URL_MANUFACTURER_LINK,
                headers=auth_headers(set_token, x_csrf_token, content_type_json=True),
                json=fabricante,
                timeout=30,
            )
            item = {
                "indice": i,
                "codigoProduto": codigo_produto,
                "codigoOperadorEstrangeiro": codigo_operador,
                "status_code": response.status_code,
                "sucesso": response.ok,
            }

            if response.ok:
                sucesso += 1
                item["erro"] = response_payload(response)
                print(error, f"{i} de {total} - Falha ao vincular.")
                print(info, normalize_json(item["erro"]))

            resultados.append(item)
        except requests.RequestException as ex:
            falha += 1
            resultados.append(
                {
                    "indice": i,
                    "codigoProduto": codigo_produto,
                    "codigoOperadorEstrangeiro": codigo_operador,
                    "status_code": None,
                    "sucesso": False,
                    "erro": str(ex),
                }
            )
            print(error, f"{i} de {total} - Erro na requisição: {ex}")
    relatorio, nome_relatorio = gerar_relatorio(
        nome_base="relatorio_vinculos",
        arquivo_origem=str(LINK_FILE),
        total=total,
        sucesso=sucesso,
        falha=falha,
        detalhes=resultados,
    )

    print(separator)
    print(info, f"Processados: {total}")
    print(success, f"Sucesso: {sucesso}")
    print(error, f"Falha: {falha}")
    print(info, f"Relatório salvo em: {nome_relatorio}")

    return relatorio


def desvincula_fabricante_produto():
    set_token, x_csrf_token = obter_autenticacao()
    dados = load_json_file(DISENGAGEMENT_FILE)

    resultados, sucesso, falha = [], 0, 0
    total = len(dados)
    url = f"{LINK_PROD}{PREFIX_CATP}/ext/fabricante/{ROOT_CPF_CNPJ}"

    for i, item in enumerate(dados, start=1):
        codigo_produto = item.get("codigoProduto")
        codigo_operador = item.get("codigoOperadorEstrangeiro")
        print(
            info,
            f"{i} de {total} - Desvinculando: produto={codigo_produto}, operador={codigo_operador}",
        )

        try:
            response = requests.put(
                url,
                headers=auth_headers(set_token, x_csrf_token, content_type_json=True),
                json=item,
                timeout=30,
            )

            item_resultado = {
                "indice": i,
                "codigoProduto": codigo_produto,
                "codigoOperadorEstrangeiro": codigo_operador,
                "status_code": response.status_code,
                "sucesso": response.ok,
            }

            if response.ok:
                sucesso += 1
                print(success, f"{i} de {total} - Fabricante desvinculado com sucesso!")
                maybe_json = response_payload(response)
                if maybe_json:
                    item_resultado["resposta"] = maybe_json
                else:
                    falha += 1
                    item_resultado["erro"] = response_payload(response)
                    print(error, f"{i} de {total} - Falha ao desvincular.")
                    print(info, normalize_json(item_resultado["erro"]))

                resultados.append(item_resultado)
        except requests.RequestException as ex:
            falha += 1
            resultados.append(
                {
                    "indice": i,
                    "codigoProduto": codigo_produto,
                    "codigoOperadorEstrangeiro": codigo_operador,
                    "status_code": None,
                    "sucesso": False,
                    "erro": str(ex),
                }
            )
            print(error, f"{i} de {total} - Erro na requisição: {ex}")

    relatorio, nome_relatorio = gerar_relatorio(
        nome_base="relatorio_desvinculo",
        arquivo_origem=str(DISENGAGEMENT_FILE),
        total=total,
        sucesso=sucesso,
        falha=falha,
        detalhes=resultados,
    )

    print(separator)
    print(info, f"Total: {total}")
    print(success, f"Desvinculado(s): {sucesso}")
    print(error, f"Falha: {falha}")
    print(info, f"Relatório salvo em: {nome_relatorio}")
    return relatorio


def exporta_vinculos_fabricante_produtos():
    set_token, x_csrf_token = obter_autenticacao()
    url = f"{LINK_PROD}{PREFIX_CATP}/ext/fabricante/exportar/{ROOT_CPF_CNPJ}"
    response = requests.get(
        url, headers=auth_headers(set_token, x_csrf_token), timeout=30
    )

    if response.ok:
        print(success, "Consulta realizada com sucesso!")
        print(info, normalize_json(response_payload(response)))
        return response_payload(response)

    print(error, "Falha na consulta.")
    print(info, normalize_json(response_payload(response)))

    return None
