import requests
from app.auth import obter_autenticacao
from app.config import (
    LINK_PROD,
    PREFIX_CATP,
    ROOT_CPF_CNPJ,
    OPERATOR_FILE,
    URL_FOREIGN_OPERATOR_CONSULTATION,
)
from app.logger import success, error, info, separator
from app.utils import load_json_file, response_payload, normalize_json, auth_headers


def inclui_operador_estrangeiro():
    set_token, x_csrf_token = obter_autenticacao()
    body = load_json_file(OPERATOR_FILE)
    operadores = body if isinstance(body, list) else [body]

    base = f"{LINK_PROD}{PREFIX_CATP}".rstrip("/")
    url = f"{base}/ext/operador-estrangeiro/{ROOT_CPF_CNPJ}/"

    last_payload = None
    for operador in operadores:
        nome = operador.get("nome", "N/A")
        response = requests.post(
            url,
            headers=auth_headers(set_token, x_csrf_token, content_type_json=True),
            json=operador,
            timeout=30,
        )

        if response.ok:
            print(separator)
            print(success, f"Operador {nome} incluído com sucesso!")
            print(success, normalize_json(response_payload(response)))
        else:
            print(separator)
            print(error, f"Falha ao incluir o operador {nome}.")
            print(error, normalize_json(response_payload(response)))

        last_payload = response_payload(response)
    return last_payload


def consulta_operador_estrangeiro():
    set_token, x_csrf_token = obter_autenticacao()
    response = requests.get(
        URL_FOREIGN_OPERATOR_CONSULTATION,
        params={"cpfCnpjRaiz": ROOT_CPF_CNPJ},
        headers=auth_headers(set_token, x_csrf_token),
        timeout=30,
    )

    if response.ok:
        print(success, "Consulta realizada com sucesso!")
        data = response_payload(response)
        print(success, normalize_json(data))
        return data

    print(error, "Falha ao na consulta.")
    print(error, normalize_json(response_payload(response)))
    return None


def desativa_operador_estrangeiro(codigo: str, codigo_pais: str, versao: str):
    set_token, x_csrf_token = obter_autenticacao()
    url = f"{LINK_PROD}{PREFIX_CATP}/ext/operador-estrangeiro/desativar/{ROOT_CPF_CNPJ}/{codigo_pais}/{codigo}/{versao}"

    response = requests.put(
        url, headers=auth_headers(set_token, x_csrf_token), timeout=30
    )

    if response.ok:
        print(success, "Operador estrangeiro desativado com sucesso!")
    else:
        print(error, "Falha ao desativar o operador estrangeiro.")
        print(info, normalize_json(response_payload(response)))
    return response_payload(response)
