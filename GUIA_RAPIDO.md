# 🚀 Guia Rápido - Bot de Tickets

## ⚡ Começando em 5 Minutos

### 1. Instalação Rápida

```bash
# Instalar dependências
pip install -r requirements.txt

# Copiar arquivo de configuração
cp .env.example .env

# Editar .env e adicionar seu token
nano .env  # ou use qualquer editor
```

### 2. Iniciar o Bot

```bash
python bot.py
```

Você verá:
```
✅ Cog carregada: cogs.ticket_config
✅ Cog carregada: cogs.ticket_system
✅ Cog carregada: cogs.ticket_management
✅ Cog carregada: cogs.utilidades
✅ X comandos slash sincronizados
╔═══════════════════════════════════════╗
║  🎫 Bot de Tickets Online
║  Nome: SeuBot
║  ID: 123456789
║  Servidores: 1
╚═══════════════════════════════════════╝
```

### 3. Configuração no Discord (5 comandos)

Execute estes comandos em ordem:

#### Passo 1: Crie uma categoria para tickets
```
/ticket-config categoria [selecione a categoria]
```

#### Passo 2: Configure o canal de logs
```
/ticket-config logs [selecione o canal]
```

#### Passo 3: Configure o cargo de suporte
```
/ticket-config cargo-suporte [selecione o cargo]
```

#### Passo 4: Veja as configurações
```
/ticket-config ver
```

#### Passo 5: Crie o painel
```
/painel
```

**Pronto! Seu sistema de tickets está funcionando! 🎉**

## 🎨 Personalização Rápida

### Adicionar Categoria Personalizada

```
/ticket-config categoria-ticket
    id_categoria: vendas
    nome: Vendas
    emoji: 💰
    descricao: Quero comprar algo
    ativar: True
```

### Personalizar Mensagens

```
/ticket-config mensagem-abertura 
mensagem: Olá {user}! 👋 Obrigado por abrir um ticket. Nossa equipe responderá em breve!
```

```
/ticket-config mensagem-fechamento
mensagem: Ticket fechado por {user}. Obrigado por entrar em contato! 🎫
```

### Configurar Auto-deleção

```
/ticket-config auto-deletar
    ativar: True
    minutos: 10
```

## 💡 Dicas Rápidas

### Para Administradores

1. **Organize suas categorias**: Use emojis diferentes para cada tipo
2. **Configure limites**: `/ticket-config limite-tickets 3`
3. **Ative transcrições**: Sempre úteis para revisão
4. **Configure logs**: Monitore tudo que acontece

### Para Equipe de Suporte

1. **Reivindique tickets**: Clique no botão ✋
2. **Adicione membros**: `/adicionar @usuario`
3. **Gere transcrição**: Clique no botão 📄
4. **Feche com motivo**: `/fechar [motivo]`

### Para Usuários

1. Clique no painel para abrir ticket
2. Selecione a categoria adequada
3. Aguarde resposta da equipe
4. Você pode fechar seu próprio ticket

## 🎯 Casos de Uso

### Servidor de Jogos
```
Categorias sugeridas:
🎮 Suporte Técnico
🐛 Report de Bug
💡 Sugestões
🎁 Reclamar Recompensas
```

### Servidor de Vendas
```
Categorias sugeridas:
💰 Compras
📦 Rastreamento
🔄 Trocas e Devoluções
❓ Dúvidas Gerais
```

### Servidor de Comunidade
```
Categorias sugeridas:
🎫 Suporte Geral
🚨 Denúncias
🤝 Parcerias
✨ Sugestões
```

## 🔧 Solução Rápida de Problemas

### Bot não responde
```bash
# Verifique se está rodando
python bot.py

# Veja os logs no console
```

### Comandos não aparecem
- Aguarde 1-2 minutos (sincronização)
- Reinstale o bot com novas permissões
- Verifique se tem permissão de Administrador

### Tickets não são criados
- Verifique se configurou a categoria
- Confirme permissões do bot
- Categoria não pode estar cheia (max 50 canais)

## 📋 Checklist de Configuração

- [ ] Bot instalado e rodando
- [ ] Token configurado no .env
- [ ] Bot adicionado ao servidor
- [ ] `/ticket-config categoria` configurado
- [ ] `/ticket-config logs` configurado  
- [ ] `/ticket-config cargo-suporte` configurado
- [ ] Categorias de ticket criadas/editadas
- [ ] Painel criado com `/painel`
- [ ] Teste: criar um ticket
- [ ] Teste: fechar um ticket
- [ ] Verificar log no canal de logs

## 🎓 Comandos Essenciais

| O Que Fazer | Comando |
|-------------|---------|
| Ver ajuda | `/ajuda` |
| Ver configurações | `/ticket-config ver` |
| Criar painel | `/painel` |
| Fechar ticket | `/fechar` |
| Ver tickets abertos | `/tickets abertos` |
| Ver meus tickets | `/tickets meus` |
| Ver emojis | `/emoji-list` |
| Info do bot | `/botinfo` |

## 🚀 Próximos Passos

1. ✅ Configure as mensagens personalizadas
2. ✅ Adicione emojis personalizados às categorias
3. ✅ Configure limites de tickets por usuário
4. ✅ Ative auto-deleção se desejar
5. ✅ Treine sua equipe nos comandos
6. ✅ Monitore os logs regularmente

## 💬 Mensagens de Exemplo

### Mensagem de Abertura Profissional
```
Olá {user}! 👋

Obrigado por abrir um ticket. Nossa equipe de suporte foi notificada e responderá o mais breve possível.

⏰ Tempo médio de resposta: 2-4 horas
📋 ID do Ticket: #{ticket_id}

Por favor, descreva seu problema com detalhes.
```

### Mensagem de Fechamento
```
✅ Ticket fechado por {user}

Obrigado por entrar em contato! Se precisar de mais ajuda, não hesite em abrir um novo ticket.

⭐ Avalie nosso atendimento em #feedback
```

## 🎨 Emojis Recomendados

Para categorias:
- 🎫 Suporte Geral
- 🐛 Bugs
- 💡 Sugestões
- 🚨 Denúncias
- 💰 Vendas
- 🎁 Recompensas
- ❓ Dúvidas
- 🤝 Parcerias
- 📦 Entregas
- 🔧 Técnico

---

**🎉 Agora você está pronto para usar o Bot de Tickets!**

Para mais detalhes, veja o `README.md` completo.
