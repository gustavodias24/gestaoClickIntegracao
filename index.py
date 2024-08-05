"""
    {
        "id": "93642",
        "nome": "Matriz"
    },
    {
        "id": "439109",
        "nome": "MRN"
    }

"""

import requests
import json
from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "allow_headers": "access-token, secret-access-token"}})


@app.route("/")
def index():
    return render_template("index.html")


def pegarProdutosAtualizado(idLoja):
    produtosAtualizados = []

    paginaAtual = 1
    while True:
        print(f"LOG: Pegando Produtos na Página: {paginaAtual}")
        url = f"https://api.gestaoclick.com/produtos?loja_id={idLoja}&pagina={paginaAtual}"

        headers = {
            'access-token': '3076727a4d1aa63c37dad01d898cbd5e76be736c',
            'secret-access-token': '78431bbea7a34f085aca7e8d0352628148145947'
        }

        response = requests.request("GET", url, headers=headers)

        if response.status_code == 200:

            for data in response.json().get('data'):
                produtosAtualizados.append(data)

            paginaAtual += 1

            if paginaAtual > response.json().get('meta').get('total_paginas'):
                break

    return produtosAtualizados


def atualizarProduto(idLoja, produtoPayLoad):
    url = f"https://api.gestaoclick.com/produtos/{produtoPayLoad.get('id')}?loja_id={idLoja}"
    payload = json.dumps(produtoPayLoad)

    headers = {
        'access-token': '3076727a4d1aa63c37dad01d898cbd5e76be736c',
        'secret-access-token': '78431bbea7a34f085aca7e8d0352628148145947',
        'Content-Type': 'application/json'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)

    print(f"LOG: Status-Code: {response.status_code} / Produto - {produtoPayLoad.get('nome')} ")


if __name__ == "__main__":
    app.run()

    # print("Escolha uma Opção")
    # opc2 = input("( 1 ) Matriz para MRN\n( 2 ) MRN para Matriz\n")
    #
    # if opc2 == '1':
    #     lojaOrigem = "93642"
    #     lojaDestino = "439109"
    # elif opc2 == '2':
    #     lojaOrigem = "439109"
    #     lojaDestino = "93642"
    # else:
    #     print("Opção inválida")
    #
    # produtosParaAtualizar = pegarProdutosAtualizado(lojaOrigem)
    #
    # for produto in produtosParaAtualizar:
    #     atualizarProduto(lojaDestino, produto)
    #
    # print(f'Total de Produtos Atualizados: {len(produtosParaAtualizar)}')
