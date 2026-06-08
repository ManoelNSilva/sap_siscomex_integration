import requests
from app.auth import obter_autenticacao
from app.config import (
    PREFIX_CATP,
    LINK_PROD,
    ROOT_CPF_CNPJ,
    URL_INSERT_PRODUCT,
    INSERT_PRODUCT_FILE,
    DISABLE_PRODUCT_FILE,
)
from app.logger import success, error, info, separator
from app.reporting import gerar_relatorio
from app.utils import load_json_file, response_payload, normalize_json, auth_headers


def consulta_produtos():
    set_token, x_csrf_token = obter_autenticacao()
    url = f"{LINK_PROD}{PREFIX_CATP}/ext/produto"
    print(info, "produtos.consulta_produtos - link: ", url)
    response = requests.get(
        url,
        params={"cpfCnpjRaiz": ROOT_CPF_CNPJ},
        headers=auth_headers(set_token, x_csrf_token),
        timeout=30,
    )
    if response.ok:
        print(success, "Consulta eralizada com sucesso!")
        print(info, "Produtos:\n", normalize_json(response_payload(response)))
        return response_payload(response)

    print(error, "Falha na consulta.")
    print(info, "Info:\n", normalize_json(response_payload(response)))
    return None


def consulta_produto_individual(codigo: str):
    set_token, x_csrf_token = obter_autenticacao()
    url = f"{LINK_PROD}{PREFIX_CATP}/ext/produto"
    response = requests.get(
        url,
        params={"cpfCnpjRaiz": ROOT_CPF_CNPJ, "codigo": codigo},
        headers=auth_headers(set_token, x_csrf_token),
        timeout=30,
    )
    if response.ok:
        print(info, normalize_json(response_payload(response)))
        return response_payload(response)

    print(error, "Falha ao consultar o produto.")
    print(info, normalize_json(response_payload(response)))


def inclui_produto():
    set_token, x_csrf_token = obter_autenticacao()
    body = load_json_file(INSERT_PRODUCT_FILE)
    response = requests.post(
        URL_INSERT_PRODUCT,
        headers=auth_headers(set_token, x_csrf_token, content_type_json=True),
        json=body,
        timeout=30,
    )
    if response.ok:
        print(success, "Produto incluído com sucesso!")
    else:
        print(separator)
        print(error, "Falha ao incluir o produto.")
        print(info, normalize_json(response_payload(response)))
        print(separator)
    return response_payload(response)


def desativa_produto(codigo: str):
    set_token, x_csrf_token = obter_autenticacao()
    url = f"{LINK_PROD}{PREFIX_CATP}/ext/produto/desativar/{ROOT_CPF_CNPJ}/{codigo}"
    response = requests.put(
        url, headers=auth_headers(set_token, x_csrf_token), timeout=30
    )

    if response.ok:
        print(success, "Produto desativado com sucesso!")
    else:
        print(error, "Falha ao desativar o produto.")
        print(info, normalize_json(response_payload(response)))
        print(separator)
    return response_payload(response)


def desativa_produtos_lote():
    set_token, x_csrf_token = obter_autenticacao()
    dados = load_json_file(DISABLE_PRODUCT_FILE)
    codigos = dados if isinstance(dados, list) else dados.get("codigos", [])

    resultados = []
    sucesso = 0
    falha = 0

    for codigo in codigos:
        url = f"{LINK_PROD}{PREFIX_CATP}/ext/produto/desativar/{ROOT_CPF_CNPJ}/{codigo}"
        response = requests.put(
            url, headers=auth_headers(set_token, x_csrf_token), timeout=30
        )

        item = {
            "codigo": codigo,
            "status_code": response.status_code,
            "sucesso": response.ok,
        }
        if response.ok:
            sucesso += 1
            print(success, f"Produto {codigo} desativado com sucesso!")
        else:
            falha += 1
            item["erro"] = response_payload(response)
            print(error, f"Falha ao desativar o produto {codigo}.")
        resultados.append(item)

    relatorio, nome_relatorio = gerar_relatorio(
        nome_base="relatorio_desativacao",
        arquivo_origem=str(DISABLE_PRODUCT_FILE),
        total=len(codigos),
        sucesso=sucesso,
        falha=falha,
        detalhes=resultados,
    )

    print(separator)
    print(success, f"Sucesso: {sucesso} desativado(s), {falha} falha(s).")
    print(info, f"Relatório salvo em: {nome_relatorio}")
    return relatorio
