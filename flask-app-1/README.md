# Flask App

Este projeto é uma aplicação web simples desenvolvida com Flask. A aplicação permite buscar e visualizar informações de clientes.

## Estrutura do Projeto

```
flask-app
├── src
│   ├── app.py                # Ponto de entrada da aplicação Flask
│   ├── templates
│   │   ├── index.html        # Template da página inicial
│   │   └── details.html      # Template da página de detalhes do cliente
├── requirements.txt          # Dependências do projeto
└── README.md                 # Documentação do projeto
```

## Pré-requisitos

Antes de executar a aplicação, certifique-se de ter o Python e o pip instalados em sua máquina.

## Instalação

1. Clone o repositório ou baixe os arquivos do projeto.
2. Navegue até o diretório do projeto.
3. Instale as dependências necessárias com o seguinte comando:

```
pip install -r requirements.txt
```

## Execução

Para executar a aplicação, utilize o seguinte comando:

```
python src/app.py
```

A aplicação estará disponível em `http://127.0.0.1:5000/`.

## Funcionalidades

- **Página Inicial**: Permite buscar clientes por CNPJ, Código do Cliente ou Nome do Cliente.
- **Página de Detalhes**: Exibe informações detalhadas sobre um cliente específico.

## Observações

Este projeto utiliza dados fictícios e não está conectado a um banco de dados real. As consultas são feitas em uma tabela fictícia.