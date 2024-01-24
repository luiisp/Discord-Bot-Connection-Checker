## Discord Bot Connection Checker 🤖

#### O Discord Bot Connection Chacker é um Bot de Discord criado para verificar quando usuarios entrarem em um servidor, se eles possuem ou não conexão da sua conta do discord com a riot games. O bot foi feito utilizando o framework discord.py integrado com flask para autenticação via OAuth2.

### usability example
https://github.com/luiisp/Discord-Bot-Connection-Checker/assets/115284250/07071010-1ba4-4739-8881-a7ac600dc59c

### Requirements
Certifique-se de ter todas as dependências instaladas. Você pode fazer isso executando
```pip install -r requirements.txt```

Dependências:
* discord.py==2.2.2
* Flask==3.0.1
* httpx==0.26.0
* oauthlib==3.2.2
* python-dotenv==1.0.1

### Configs
#### ⚠️ Attention
para o bot funcionar, deve ter Oauth2 habilidado nas configurações do bot.
Não se esqueça de substituir a url do botao de conexão em: view.add_item > Button > url

#### Substitua os seguintes campos no arquivo configs.env:

- TOKEN=seu token 
- CLIENT_ID=seu client id
- CLIENT_SECRET=sua client secret
- URI=sua uri de redirecionamento (por padrão http://127.0.0.1:5000)

### Execute usando python bot_server.py
