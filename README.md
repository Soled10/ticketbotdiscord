# 🎫 Bot de Tickets Discord com IA 🤖

Um bot de tickets completo e totalmente configurável via Discord usando Slash Commands. Sistema inteligente com **IA integrada**, **painel visual interativo**, **estatísticas avançadas** e muito mais!

> ⚡ **NOVO:** Configure tudo com apenas `/painel` - Interface visual completa!  
> 🤖 **NOVO:** IA integrada para sugestões automáticas e análise de sentimento!  
> 📊 **NOVO:** Sistema completo de estatísticas e avaliações!

---

## ✨ Características Principais

### 🎯 Sistema de Painel Visual (**NOVO!**)
- 📋 **Configuração completa com `/painel`** - Uma interface visual para TUDO
- 🎨 **Modals e Botões Interativos** - Sem necessidade de decorar comandos
- ⚡ **Configure visualmente** - Canais, mensagens, categorias, automação, FAQ
- 🚀 **Setup em 3 cliques** - A forma mais fácil de configurar um bot

### 🤖 IA Integrada (**NOVO!** - Opcional)
- 💡 **Sugestões Automáticas** - IA sugere respostas profissionais baseadas em FAQs
- 😊 **Análise de Sentimento** - Detecta tickets urgentes/negativos automaticamente
- 🎯 **Auto-resposta Inteligente** - Responde com FAQs enquanto equipe está offline
- 📝 **Resumos Automáticos** - Gera resumo completo de tickets
- 🌐 **Multi-Provider** - OpenAI (GPT), Anthropic (Claude), Groq (LLaMA/Mixtral)
- 🆓 **Groq Gratuito** - Use LLaMA/Mixtral gratuitamente!

### 📊 Estatísticas Avançadas (**NOVO!**)
- 📈 **Métricas Detalhadas** - Total de tickets, tempos médios, categorias
- 🏆 **Ranking da Equipe** - Veja quem mais resolve tickets (gamificação!)
- 📊 **Gráficos Visuais** - Gráficos ASCII para categorias, horários e mensal
- ⭐ **Sistema de Avaliação** - Usuários avaliam o atendimento (1-5 estrelas)
- 📅 **Estatísticas Mensais** - Acompanhe evolução ao longo do tempo

### 🎫 Sistema de Tickets Completo
- 🎯 **Criação Inteligente** - Select menu com categorias personalizáveis
- 😄 **Emojis Personalizados** - Use emojis do seu servidor nas categorias
- 📋 **Categorias Ilimitadas** - Crie quantas categorias precisar
- 📄 **Transcrições HTML** - Histórico completo e bonito de cada ticket
- 🤖 **Auto-deleção Configurável** - Delete tickets fechados automaticamente
- ✋ **Sistema de Reivindicação** - Equipe pode reivindicar tickets
- 👥 **Gerenciamento de Usuários** - Adicione/remova pessoas dos tickets
- 📊 **Logs Completos** - Acompanhe todas as ações em tempo real
- 🔔 **Notificações** - Configure cargo para receber notificações

---

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Conta Discord Developer
- Bot Discord criado no [Discord Developer Portal](https://discord.com/developers/applications)
- (Opcional) API Key de IA: [Groq](https://console.groq.com/) (grátis!), [OpenAI](https://platform.openai.com/), ou [Anthropic](https://console.anthropic.com/)

---

## 🚀 Instalação Rápida

### 1. Clone o repositório

```bash
git clone <seu-repositorio>
cd workspace
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt

# Se quiser usar IA (opcional):
pip install openai  # Para GPT
# OU
pip install anthropic  # Para Claude
# OU
pip install groq  # Para LLaMA/Mixtral (GRÁTIS!)
```

### 3. Configure o bot

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite e adicione seu token
nano .env  # ou use seu editor preferido
```

No arquivo `.env`:
```env
# Obrigatório
DISCORD_TOKEN=seu_token_aqui

# Opcional - IA (recomendado!)
AI_ENABLED=true
AI_PROVIDER=groq  # groq é GRÁTIS!
AI_API_KEY=sua_chave_groq
AI_MODEL=mixtral-8x7b-32768
```

### 4. Inicie o bot

```bash
python bot.py
```

Você verá:
```
✅ Cog carregada: cogs.painel_config
✅ Cog carregada: cogs.ticket_system
✅ Cog carregada: cogs.ticket_management
✅ Cog carregada: cogs.ai_assistant
✅ Cog carregada: cogs.statistics
✅ Cog carregada: cogs.utilidades
✅ X comandos slash sincronizados
╔═══════════════════════════════════════╗
║  🎫 Bot de Tickets Online
║  Nome: SeuBot
║  ID: 123456789
║  Servidores: 1
║  🤖 IA: Ativada (groq)
╚═══════════════════════════════════════╝
```

---

## 🎮 Setup no Discord (3 PASSOS SIMPLES!)

### Passo 1: Convide o bot

Use este link (substitua CLIENT_ID pelo ID do seu bot):
```
https://discord.com/api/oauth2/authorize?client_id=CLIENT_ID&permissions=8&scope=bot%20applications.commands
```

### Passo 2: Configuração Básica (30 segundos)

```bash
/config-rapida categoria canal:#categoria-tickets
/config-rapida logs canal:#logs-tickets
/config-rapida suporte cargo:@Suporte
```

### Passo 3: Configure e Crie Painel

```bash
/painel
```

Na interface visual:
1. ✅ Clique em "Mensagens" para personalizar
2. ✅ Clique em "Categorias" para adicionar categorias personalizadas
3. ✅ Clique em "Automação" para configurar IA e auto-delete
4. ✅ Clique em "FAQ" para adicionar perguntas frequentes
5. ✅ Clique em "Criar Painel" para finalizar

**PRONTO! Seu sistema está funcionando!** 🎉

---

## 📚 Comandos

### 🎯 Comando Principal

```bash
/painel
```
Abre uma interface visual completa com botões para:
- 📋 Canais & Cargos
- 💬 Mensagens (modals interativos)
- 🎫 Categorias (adicionar/listar)
- 🤖 Automação (IA, auto-delete, etc)
- ❓ FAQ (para IA usar)
- 📊 Estatísticas
- 🎯 Criar Painel de Tickets

### ⚡ Configuração Rápida

| Comando | Descrição |
|---------|-----------|
| `/config-rapida categoria` | Define categoria dos tickets |
| `/config-rapida logs` | Define canal de logs |
| `/config-rapida suporte` | Define cargo de suporte |
| `/config-rapida notificacao` | Define cargo para notificações |

### 🤖 Automação

| Comando | Descrição |
|---------|-----------|
| `/automacao auto_delete ativar:True valor:10` | Auto-deletar após 10min |
| `/automacao transcript ativar:True` | Ativar transcrições |
| `/automacao ia_enabled ativar:True` | Ativar IA |
| `/automacao ai_auto ativar:True` | Auto-resposta da IA |
| `/automacao limit valor:3` | Máx 3 tickets por usuário |

### 🎫 Tickets

| Comando | Descrição |
|---------|-----------|
| `/criar-painel-ticket` | Cria painel customizado |
| `/fechar [motivo]` | Fecha ticket |
| `/adicionar [usuário]` | Adiciona ao ticket |
| `/remover [usuário]` | Remove do ticket |
| `/tickets [status]` | Lista tickets |
| `/avaliar [1-5]` | Avaliar atendimento ⭐ |

### 🤖 IA (requer configuração)

| Comando | Descrição |
|---------|-----------|
| `/ia-sugerir` | IA sugere resposta |
| `/ia-analisar` | Analisa sentimento |
| `/ia-resumo` | Resumo do ticket |

### 📊 Estatísticas

| Comando | Descrição |
|---------|-----------|
| `/estatisticas [periodo]` | Ver estatísticas detalhadas |
| `/ranking-staff` | Ranking da equipe 🏆 |
| `/grafico [tipo]` | Gráficos ASCII |

### 🔧 Utilidades

| Comando | Descrição |
|---------|-----------|
| `/ajuda` | Lista todos os comandos |
| `/botinfo` | Info do bot |
| `/ping` | Latência |
| `/emoji-list` | Lista emojis do servidor |

---

## 🤖 Configuração da IA (Opcional)

### Por Que Usar IA?

- ⚡ **Resposta Instantânea** - Usuários não ficam esperando
- 🎯 **Respostas Consistentes** - Baseadas em suas FAQs
- 😊 **Detecção de Urgência** - Prioriza casos críticos
- 📝 **Resumos Automáticos** - Para passar tickets entre atendentes
- 💡 **Ajuda a Equipe** - Sugestões de resposta profissionais

### Providers e Custos

| Provider | Modelo Recomendado | Custo | Qualidade | Velocidade |
|----------|-------------------|-------|-----------|------------|
| **Groq** 🆓 | mixtral-8x7b | **GRÁTIS** | ⭐⭐⭐⭐ | ⚡⚡⚡⚡⚡ |
| **OpenAI** | gpt-3.5-turbo | $0.002/1K | ⭐⭐⭐⭐⭐ | ⚡⚡⚡⚡ |
| **Anthropic** | claude-3-haiku | $0.25/1M | ⭐⭐⭐⭐⭐ | ⚡⚡⚡⚡ |

**Recomendação:** Comece com **Groq** (é grátis e rápido!)

### Setup da IA

#### 1. Obtenha API Key

- **Groq (GRÁTIS!):** https://console.groq.com/keys
- **OpenAI:** https://platform.openai.com/api-keys
- **Anthropic:** https://console.anthropic.com/

#### 2. Configure no `.env`

```env
AI_ENABLED=true
AI_PROVIDER=groq  # ou openai, ou anthropic
AI_API_KEY=sua_chave_aqui
AI_MODEL=mixtral-8x7b-32768  # ou gpt-3.5-turbo, ou claude-3-haiku
```

#### 3. Ative no Discord

```bash
/automacao ia_enabled ativar:True
/automacao ai_auto ativar:True  # Auto-resposta
```

#### 4. Adicione FAQs

```bash
/painel
# Clique em "FAQ"
# Adicione perguntas e respostas frequentes
```

#### 5. Teste!

```bash
# Em um ticket, use:
/ia-sugerir  # IA sugere resposta
/ia-analisar  # Analisa sentimento
/ia-resumo  # Gera resumo
```

### Recursos da IA

✅ **Sugestões de Resposta**
- Analisa mensagem do usuário
- Busca em FAQs relevantes
- Gera resposta profissional
- Staff revisa e envia

✅ **Análise de Sentimento**
- Detecta: positivo, neutro, negativo, urgente
- Notifica staff em casos urgentes automaticamente
- Prioriza tickets críticos

✅ **Auto-resposta (Opcional)**
- Responde automaticamente com base em FAQs
- Funciona 24/7
- Reduz tempo de primeira resposta
- Staff complementa quando necessário

✅ **Resumos Inteligentes**
- Gera resumo de todo o ticket
- Ideal para handoff entre atendentes
- Exporta contexto completo

---

## 📊 Sistema de Estatísticas

### Ver Estatísticas

```bash
/estatisticas
```

Mostra:
- 🎫 Total de tickets (abertos e histórico)
- ⭐ Avaliação média (de usuários)
- ⏱️ Tempo médio de resposta
- ⏱️ Tempo médio de resolução
- 📋 Top 5 categorias mais usadas
- 🕐 Horários de pico
- 👥 Top 5 staff que mais ajudou

### Ranking da Equipe

```bash
/ranking-staff
```

Mostra:
- 🥇 1º lugar
- 🥈 2º lugar
- 🥉 3º lugar
- Demais posições
- Gamificação para a equipe!

### Gráficos

```bash
/grafico tipo:categorias  # Gráfico de categorias
/grafico tipo:horarios    # Gráfico de horários
/grafico tipo:mensal      # Gráfico mensal
```

Exemplo:
```
Categorias:
suporte        ████████████ 45
duvida         ████████ 32
bug            ████ 18
parceria       ██ 8
```

### Sistema de Avaliação

Usuários podem avaliar:
```bash
/avaliar nota:5  # 5 estrelas
```

Opções:
- ⭐ 1 - Muito Ruim
- ⭐⭐ 2 - Ruim
- ⭐⭐⭐ 3 - Regular
- ⭐⭐⭐⭐ 4 - Bom
- ⭐⭐⭐⭐⭐ 5 - Excelente

Feedback automático para cada nota!

---

## 🔧 Estrutura do Projeto

```
workspace/
├── bot.py                      # Bot principal com suporte a IA
├── requirements.txt            # Dependências
├── .env.example               # Exemplo de configuração
├── .env                       # Suas configurações (NÃO commitar!)
├── .gitignore                 # Git ignore
│
├── README.md                  # Documentação principal
├── NOVIDADES.md               # Recursos novos detalhados
├── GUIA_RAPIDO.md             # Setup em 5 minutos
├── EXEMPLOS.md                # Exemplos práticos
│
├── config/                    # Auto-gerado
│   ├── guild_configs.json     # Configurações por servidor
│   ├── tickets_data.json      # Dados dos tickets
│   ├── statistics.json        # Estatísticas
│   └── faq_data.json          # FAQs para IA
│
└── cogs/                      # Módulos
    ├── painel_config.py       # [NOVO] Painel interativo
    ├── ai_assistant.py        # [NOVO] Sistema de IA
    ├── statistics.py          # [NOVO] Estatísticas
    ├── ticket_system.py       # Sistema de tickets
    ├── ticket_management.py   # Gerenciamento
    └── utilidades.py          # Utilitários
```

---

## 🎯 Casos de Uso

### 1. Servidor de Jogos 🎮
```
Categorias:
🔧 Suporte Técnico
🐛 Report de Bug
🎁 Recompensas
🚨 Denúncias

IA ativa: Responde FAQs sobre bugs conhecidos
```

### 2. E-commerce 🛍️
```
Categorias:
💰 Compras
📦 Rastreamento
🔄 Trocas/Devoluções
💳 Pagamento

IA ativa: Informa status de pedidos automaticamente
```

### 3. Suporte SaaS 💼
```
Categorias:
🆘 Suporte Urgente
❓ Dúvidas
💡 Feature Request
🐛 Bugs

IA ativa: Triagem automática, detecta urgência
Estatísticas: Monitora SLA e satisfação
```

### 4. Comunidade/Discord 🎭
```
Categorias:
🎫 Suporte Geral
🚨 Denúncias
🤝 Parcerias
👔 Candidatura Staff

IA ativa: Auto-resposta com regras do servidor
```

---

## ❓ FAQ

### O bot funciona sem IA?
**Sim!** IA é totalmente opcional. O bot funciona perfeitamente sem ela.

### Qual provider de IA usar?
- **Iniciante:** Groq (grátis e rápido)
- **Produção pequena:** OpenAI GPT-3.5 (barato)
- **Produção grande:** Anthropic Claude (melhor qualidade)

### Quanto custa?
- **Bot:** Grátis e open source
- **IA Groq:** Grátis (tier generoso)
- **IA OpenAI:** ~$0.002 por 1000 tokens (muito barato)
- **IA Anthropic:** ~$0.25 por 1M tokens

### A IA vai responder errado?
A IA é baseada em suas FAQs. Quanto melhores suas FAQs, melhores as respostas. Staff sempre pode revisar e complementar.

### Como desativar IA depois?
```bash
/automacao ia_enabled ativar:False
```

### Posso ter múltiplos painéis?
Sim! Use `/criar-painel-ticket` em qualquer canal.

---

## 🔒 Segurança

- ⚠️ **NUNCA** compartilhe seu `.env` ou tokens
- ✅ `.env` já está no `.gitignore`
- ✅ Use permissões apropriadas no Discord
- ✅ Mantenha dependências atualizadas
- ✅ API Keys de IA são criptografadas em trânsito

---

## 🐛 Problemas Conhecidos

- Limite de 50 canais por categoria (Discord)
- Select menu máx 25 opções (Discord)
- Transcrições não incluem imagens inline (apenas links)

---

## 🚀 Roadmap

- [ ] Dashboard web
- [ ] Sistema de tags/prioridades
- [ ] Integração com webhooks
- [ ] Backup automático
- [ ] Mais providers de IA
- [ ] Transcrição com imagens

---

## 💬 Suporte

Documentação completa:
- `README.md` - Este arquivo
- `NOVIDADES.md` - Detalhes das novas funcionalidades
- `GUIA_RAPIDO.md` - Setup rápido
- `EXEMPLOS.md` - Exemplos práticos

No Discord:
- `/ajuda` - Lista de comandos
- `/botinfo` - Info do bot

---

## 📜 Licença

Este projeto é open source e está disponível para uso livre.

---

## 🙏 Contribuindo

Contribuições são bem-vindas!

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/MinhaFeature`)
3. Commit (`git commit -m 'Add MinhaFeature'`)
4. Push (`git push origin feature/MinhaFeature`)
5. Pull Request

---

## ⭐ Agradecimentos

Obrigado por usar este bot! Se gostou, deixe uma ⭐ no repositório!

---

**🎫 Bot de Tickets com IA • Configurável • Open Source • Feito com ❤️**
