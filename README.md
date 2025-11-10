# 🎫 Bot de Tickets Discord

Um bot de tickets completo e totalmente configurável via Discord usando Slash Commands. Suporte a emojis personalizados, múltiplas categorias de tickets, transcrições automáticas e muito mais!

## ✨ Características

- 🎯 **100% Configurável via Discord** - Sem necessidade de editar código
- 🎫 **Sistema Completo de Tickets** - Criação, gerenciamento e fechamento
- 😄 **Emojis Personalizados** - Use emojis do seu servidor nas categorias
- 📋 **Categorias Customizáveis** - Crie quantas categorias quiser
- 📄 **Transcrições HTML** - Salve todo o histórico dos tickets
- 🤖 **Auto-deleção** - Delete tickets fechados automaticamente
- ✋ **Sistema de Reivindicação** - Equipe pode reivindicar tickets
- 📊 **Logs Completos** - Acompanhe todas as ações em tempo real
- 🔧 **Painel Interativo** - Select menu para escolher tipo de ticket
- 🛡️ **Sistema de Permissões** - Controle total sobre quem pode fazer o quê

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Conta Discord Developer
- Bot Discord criado no [Discord Developer Portal](https://discord.com/developers/applications)

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone <seu-repositorio>
cd workspace
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure o bot

1. Copie o arquivo `.env.example` para `.env`:
```bash
cp .env.example .env
```

2. Edite o arquivo `.env` e adicione seu token:
```
DISCORD_TOKEN=seu_token_aqui
```

### 4. Inicie o bot

```bash
python bot.py
```

## 🎮 Configuração Inicial

### 1. Convide o bot para seu servidor

Use este link (substitua CLIENT_ID pelo ID do seu bot):
```
https://discord.com/api/oauth2/authorize?client_id=CLIENT_ID&permissions=8&scope=bot%20applications.commands
```

### 2. Configure as permissões necessárias

O bot precisa das seguintes permissões:
- ✅ Gerenciar Canais
- ✅ Gerenciar Cargos
- ✅ Ver Canais
- ✅ Enviar Mensagens
- ✅ Gerenciar Mensagens
- ✅ Incorporar Links
- ✅ Anexar Arquivos
- ✅ Ler Histórico de Mensagens

### 3. Configure o sistema de tickets

Execute os seguintes comandos no Discord (requer permissão de Administrador):

```
1. /ticket-config categoria [categoria]
   Define onde os tickets serão criados

2. /ticket-config logs [canal]
   Define onde os logs serão enviados

3. /ticket-config cargo-suporte [cargo]
   Define qual cargo terá acesso aos tickets

4. /painel
   Cria o painel para abertura de tickets
```

## 📚 Comandos

### ⚙️ Configuração (`/ticket-config`)

| Comando | Descrição |
|---------|-----------|
| `/ticket-config categoria` | Define a categoria onde tickets serão criados |
| `/ticket-config logs` | Define o canal de logs |
| `/ticket-config cargo-suporte` | Define o cargo da equipe de suporte |
| `/ticket-config mensagem-abertura` | Personaliza mensagem ao abrir ticket |
| `/ticket-config mensagem-fechamento` | Personaliza mensagem ao fechar ticket |
| `/ticket-config limite-tickets` | Define limite de tickets por usuário (1-10) |
| `/ticket-config auto-deletar` | Configura deleção automática de tickets fechados |
| `/ticket-config transcrição` | Ativa/desativa transcrições |
| `/ticket-config categoria-ticket` | Cria/edita categoria de ticket personalizada |
| `/ticket-config remover-categoria` | Remove uma categoria de ticket |
| `/ticket-config ver` | Visualiza todas as configurações |

### 🎫 Sistema de Tickets

| Comando | Descrição |
|---------|-----------|
| `/painel` | Cria um painel interativo para abertura de tickets |
| `/fechar [motivo]` | Fecha o ticket atual |
| `/adicionar [usuário]` | Adiciona um usuário ao ticket |
| `/remover [usuário]` | Remove um usuário do ticket |
| `/tickets [status]` | Lista tickets (abertos/fechados/meus) |

### 🔧 Utilidades

| Comando | Descrição |
|---------|-----------|
| `/ajuda` | Mostra todos os comandos disponíveis |
| `/botinfo` | Informações sobre o bot |
| `/ping` | Verifica a latência do bot |
| `/emoji-list` | Lista emojis personalizados do servidor |

## 🎨 Categorias de Tickets Personalizadas

Você pode criar categorias completamente personalizadas:

```
/ticket-config categoria-ticket 
    id_categoria: suporte
    nome: Suporte Técnico
    emoji: 🔧
    descricao: Preciso de ajuda técnica
    ativar: True
```

### Categorias Padrão

O bot vem com 4 categorias pré-configuradas:

- 🎫 **Suporte Geral** - Preciso de ajuda com algo
- ❓ **Dúvidas** - Tenho uma dúvida
- 🚨 **Denúncia** - Reportar um problema
- 🤝 **Parcerias** - Proposta de parceria

## 😄 Usando Emojis Personalizados

### Ver emojis disponíveis
```
/emoji-list
```

### Usar em categorias
Ao criar/editar uma categoria, você pode usar:
- Emojis Unicode: ✅ ❌ 🎫 🔧
- Emojis personalizados: Copie e cole do servidor

### Usar em mensagens
Use placeholders nas mensagens personalizadas:
- `{user}` - Menção do usuário
- `{username}` - Nome do usuário
- Emojis personalizados: `:nome_do_emoji:`

## 🎛️ Painel de Controle de Tickets

Quando um ticket é criado, aparece um painel com botões:

- 🔒 **Fechar** - Fecha o ticket
- ✋ **Reivindicar** - Reivindica o ticket para você
- 📄 **Transcrição** - Gera transcrição HTML do ticket

## 📊 Sistema de Logs

Todos os eventos são registrados no canal de logs configurado:

- ✅ Abertura de tickets
- 🔒 Fechamento de tickets
- ✋ Reivindicação de tickets
- 👥 Adição/remoção de usuários
- 📄 Transcrições anexadas automaticamente

## 📄 Transcrições

As transcrições são geradas em formato HTML com:
- ✅ Todas as mensagens do ticket
- ✅ Timestamps formatados
- ✅ Informações dos usuários
- ✅ Embeds preservados
- ✅ Links para anexos
- ✅ Design responsivo e bonito

## 🔧 Estrutura de Arquivos

```
workspace/
├── bot.py                      # Arquivo principal do bot
├── requirements.txt            # Dependências Python
├── .env.example               # Exemplo de configuração
├── .env                       # Suas configurações (não commitar!)
├── .gitignore                 # Arquivos ignorados pelo Git
├── README.md                  # Este arquivo
├── config/                    # Pasta de configurações (auto-gerada)
│   ├── guild_configs.json     # Configurações dos servidores
│   └── tickets_data.json      # Dados dos tickets
└── cogs/                      # Módulos do bot
    ├── ticket_config.py       # Comandos de configuração
    ├── ticket_system.py       # Sistema de criação de tickets
    ├── ticket_management.py   # Gerenciamento de tickets
    └── utilidades.py          # Comandos utilitários
```

## 🛠️ Desenvolvimento

### Adicionar nova funcionalidade

1. Crie um novo arquivo em `cogs/`
2. Implemente sua cog:

```python
from discord.ext import commands

class MinhaFuncionalidade(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Seus comandos aqui

async def setup(bot):
    await bot.add_cog(MinhaFuncionalidade(bot))
```

3. Carregue a cog em `bot.py`:
```python
cogs_to_load = [
    # ... outras cogs
    "cogs.minha_funcionalidade"
]
```

### Customizar mensagens

Edite as mensagens padrão em `bot.py` na função `get_guild_config()`.

## ❓ FAQ

### O bot não responde aos comandos
- Verifique se o bot está online
- Confirme que os comandos foram sincronizados (aparece no console)
- Verifique as permissões do bot no servidor

### Os tickets não são criados
- Configure a categoria com `/ticket-config categoria`
- Verifique se o bot tem permissão de criar canais
- Confirme que há espaço na categoria (máx 50 canais)

### Emojis personalizados não aparecem
- Use `/emoji-list` para ver emojis disponíveis
- Copie e cole o emoji exatamente como aparece
- Certifique-se de que o bot está no mesmo servidor do emoji

### Como resetar as configurações?
Delete os arquivos em `config/` e reinicie o bot.

## 📝 Variáveis de Placeholder

Use estas variáveis nas mensagens personalizadas:

- `{user}` - Menção do usuário (@usuário)
- `{username}` - Nome do usuário (sem @)
- `{server}` - Nome do servidor
- `{member_count}` - Total de membros

## 🔒 Segurança

- ⚠️ **NUNCA** compartilhe seu arquivo `.env` ou token
- ✅ Sempre adicione `.env` ao `.gitignore`
- ✅ Use permissões apropriadas no Discord
- ✅ Mantenha as dependências atualizadas

## 🐛 Problemas Conhecidos

- Limite de 50 canais por categoria (limitação do Discord)
- Select menu só pode ter até 25 opções (limitação do Discord)
- Transcrições não incluem imagens diretamente (apenas links)

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se livre para:

1. Fazer fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abrir um Pull Request

## 📜 Licença

Este projeto é de código aberto e está disponível para uso livre.

## 💬 Suporte

Se tiver problemas ou dúvidas:

1. Verifique o FAQ acima
2. Leia a documentação do Discord.py
3. Use `/ajuda` no bot para ver os comandos

## 🎯 Roadmap

Funcionalidades planejadas:

- [ ] Sistema de avaliação de tickets
- [ ] Estatísticas detalhadas
- [ ] Backup automático de transcrições
- [ ] Sistema de tags/prioridades
- [ ] Integração com webhooks
- [ ] Dashboard web (futuro)

## 📸 Screenshots

### Painel de Tickets
O painel interativo com select menu para escolher o tipo de ticket.

### Canal de Ticket
Canal privado criado automaticamente com botões de controle.

### Transcrição HTML
Transcrição completa e formatada de todo o ticket.

---

**Feito com ❤️ para a comunidade Discord**

🎫 Bot de Tickets • Configurável • Open Source
