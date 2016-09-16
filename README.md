# Índice

1. [Ambiente de desenvolvimento](#ambiente-de-desenvolvimento)
  - [Instalar git](#Instalar-git)
  - [Instalar Python](#Instalar-Python)
  - [Instalar dependências](#Instalar-dependencias)
  - [Instalar MongoDB](#Instalar-mongodb)
2. [Modelo de produto - MongoDB](#modelo-de-produto)
3. [Arquitetura do projeto](#Arquitetura-do-projeto)
4. [Como rodar extração de links](#Extracao-de-links)
5. [Como rodar extração de dados](#Extracao-de-dados)
6. [OFF-Topic](#OFF-TOPIC)

***
# <a id="ambiente-de-desenvolvimento">Ambiente de desenvolvimento</a>

## <a id="Instalar-git">Instalar git: </a>
  - `sudo apt-get install git`

## <a id="Instalar-Python">Instalar Python: </a>
  - `sudo apt-get install build-essential checkinstall`
  - `sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev`
  - `cd ~/Downloads`
  - `wget http://python.org/ftp/python/2.7.12/Python-2.7.12.tgz`
  - `tar -xvf Python-2.7.12.tgz`
  - `cd Python-2.7.5`
  - `./configure`
  - `make`
  - `sudo checkinstall`

## <a id="Instalar-dependencias">Instalar dependências:</a>
  - `pip install -r requirements.txt`

## <a id="Instalar-mongodb">Instalar MongoDB: </a>
  - `sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927`
  - Ubuntu 16.04
    + `echo "deb http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list`
  - `sudo apt-get update`
  - `sudo apt-get install -y mongodb-org`
  - Confira se o arquivo existe: `sudo ls /lib/systemd/system/mongod.service`
  - Senão, crie um:
    + `sudo vi /lib/systemd/system/mongod.service`
    + Pressione a tecla 'i'
    + Cole o seguinte texto dentro do arquivo:
    [Unit]
    Description=High-performance, schema-free document-oriented database
    After=network.target
    Documentation=https://docs.mongodb.org/manual

    [Service]
    User=mongodb
    Group=mongodb
    ExecStart=/usr/bin/mongod --quiet --config /etc/mongod.conf

    [Install]
    WantedBy=multi-user.target

  - Rode o banco: `sudo service mongod start`
  - Importe o arquivo mongo.json que está na pasta principal do projeto:
    + `mongoimport --db price_watch --collection products --file mongo.json`

***

# <a id="modelo-de-produto">Modelo de produto - MongoDB</a>
```
{
  _id: (BSON object) número de identificação criado pelo próprio mongo,
  available: (true/false) disponibilidade do produto,
  brand: (String) marca do produto,
  color: (String) cor majoritária do produto
  display_feature: (Array de Strings) tipos de tela (LCD/LED, Touch, 3D, etc),
  display_size: (String) tamanho de tela,
  graphics_processor_name: (String) nome da placa de vídeo,
  graphics_processor: (String) capacidade da placa de vídeo com indicação de unidade(GB, MB, etc),
  name: (String) título do produto,
  operating_system: (String) _Windows/MacOS/Linux com a versão e distribuição caso aplicável,
  price: (Float) preço do produto,
  processor: (String) processador,
  ram_memory: (String) memória ram com indicação de unidade (GB, MB etc),
  screen_resolution: (String) 1366x768 por exemplo,
  storage: (String) HD com indicação de unidade (TB, GB, MB, etc),
  storage_type: (String) HD/SSD se disponível,
  url: (String) url para a página do produto,
  image_url: (String) url para a imagem principal do produto
}
```

***

# <a id="Arquitetura-do-projeto">Arquitetura do projeto</a>
  - App: contém projeto em si
    + models: diretório contendo as classes do projeto
      * cada loja possui uma pasta com seu nome contendo um arquivo de scraper para obter os links dos produtos e um para extrair os dados
  - log: arquivos de log gerados, caso necessários
  - settings: arquivos de configuração
  - tests: arquivos de testes

***

# <a id="Extracao-de-links">Como rodar extração de links?</a>
 * Entre na pasta da loja desejada
 * No terminal digite `scrapy runspider <nome_loja>.py -t json -o - > links_list.json`
 * A lista de links será gerada dentro do arquivo links_list.json na mesma pasta da loja
 * Faça as devidas validações para guardar somente links válidos (notebooks disponíveis ou não)

***

# <a id="Extracao-de-dados">Como rodar extração de dados?</a>

### A ser definido

***
# <a id="OFF-TOPIC">OFF-TOPIC</a>

Sugestão de editor te textos:
  - https://www.sublimetext.com/3 (o que eu uso, opção pessoal)
  - http://limetext.org/
  - https://www.geany.org/Download/Releases
  - http://bluefish.openoffice.nl/download.html
  - gedit
