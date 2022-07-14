# Calunga

<p align="center">
  <img src="https://raw.githubusercontent.com/sistematico/calunga/main/assets/img/calunga.jpg" alt="Calunga" /><br />
  <em>Meia noite patrão!</em>
</p>

Um bot simples para o Telegram para baixar vídeos do Youtube e outros sites.

Demo: [@calungabot](https://t.me/calungabot) on Telegram.

## Funções

* Baixar qualquer vídeo do Youtube rapidamente e facilmente
* Envia os vídeos direto do Telegram
* Fácil de usar, só enviar o link no privado do bot

## Instalação & Configuração

Este projeto usa as bibliotecas [python-telegram-bot](https://python-telegram-bot.org/) e [yt_dlp](https://github.com/yt-dlp/yt-dlp) para interagir com o Telegram e baixar os vídeos.

Você pode instalar todas as bibliotecas necessárias com o comando:

```
pip install python-telegram-bot yt-dlp
```
ou

```
pip install -r requirements.txt
```

Adicionar o usuário e criar a unidade SystemD com o comando(como root):

```bash
bash install.sh

```

## Uso

1. Crie um bot no Telegram através do [@BotFather](https://t.me/botfather)
2. Copie o Token API
3. Crie um arquivo ```.env``` no mesmo diretório do arquivo ```calunga.py``` dentro deste arquivo crie uma variável ```TOKEN``` e cole sua api. Ex.: ```TOKEN = TOKEN_QUE_O_BOTFATHER_TE_FORNECEU```
4. Rode o bot `python3 calunga.py` para testar ou `systemctl --now enable kalunga` para deixa-lo permanente.
5. Envie um link do Youtube para ele: [@calungabot](https://t.me/calungabot)


## Bibliotecas usadas

* https://github.com/python-telegram-bot/python-telegram-bot
* https://pypi.org/project/yt-dlp


## Ajude

Se o meu trabalho foi útil de qualquer maneira, considere doar qualquer valor através do das seguintes plataformas:

[![LiberaPay](https://img.shields.io/badge/LiberaPay-gray?logo=liberapay&logoColor=white&style=flat-square)](https://liberapay.com/sistematico/donate) [![PagSeguro](https://img.shields.io/badge/PagSeguro-gray?logo=pagseguro&logoColor=white&style=flat-square)](https://pag.ae/bfxkQW) [![ko-fi](https://img.shields.io/badge/ko--fi-gray?logo=ko-fi&logoColor=white&style=flat-square)](https://ko-fi.com/K3K32RES9) [![Buy Me a Coffee](https://img.shields.io/badge/Buy_Me_a_Coffee-gray?logo=buy-me-a-coffee&logoColor=white&style=flat-square)](https://www.buymeacoffee.com/sistematico) [![Open Collective](https://img.shields.io/badge/Open_Collective-gray?logo=opencollective&logoColor=white&style=flat-square)](https://opencollective.com/sistematico) [![Patreon](https://img.shields.io/badge/Patreon-gray?logo=patreon&logoColor=white&style=flat-square)](https://patreon.com/sistematico)

![GitHub Sponsors](https://img.shields.io/github/sponsors/sistematico?label=Github%20Sponsors)
