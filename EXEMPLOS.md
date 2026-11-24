# 📚 Exemplos de Uso - Bot de Tickets

Este arquivo contém exemplos práticos de como configurar e usar o bot para diferentes cenários.

## 🎮 Exemplo 1: Servidor de Jogos

### Configuração Inicial

```bash
# 1. Configurar categoria
/ticket-config categoria [categoria: TICKETS]

# 2. Configurar logs
/ticket-config logs [canal: #logs-tickets]

# 3. Configurar cargo
/ticket-config cargo-suporte [cargo: @Moderador]

# 4. Configurar limite
/ticket-config limite-tickets limite:2
```

### Criar Categorias Personalizadas

```bash
# Suporte Técnico
/ticket-config categoria-ticket
    id_categoria: suporte-tecnico
    nome: Suporte Técnico
    emoji: 🔧
    descricao: Problemas técnicos com o servidor
    ativar: True

# Report de Bug
/ticket-config categoria-ticket
    id_categoria: bug-report
    nome: Report de Bug
    emoji: 🐛
    descricao: Reportar um bug encontrado
    ativar: True

# Denúncia de Jogador
/ticket-config categoria-ticket
    id_categoria: denuncia
    nome: Denúncia
    emoji: 🚨
    descricao: Denunciar comportamento inadequado
    ativar: True

# Reclamar Recompensas
/ticket-config categoria-ticket
    id_categoria: recompensas
    nome: Recompensas
    emoji: 🎁
    descricao: Reclamar suas recompensas
    ativar: True
```

### Mensagens Personalizadas

```bash
# Mensagem de Abertura
/ticket-config mensagem-abertura
mensagem: 🎮 Olá {user}! Bem-vindo ao suporte do servidor.

Nossa equipe de moderação responderá em breve!

⏰ Tempo médio: 30 minutos
📝 Descreva seu problema com detalhes.

# Mensagem de Fechamento
/ticket-config mensagem-fechamento
mensagem: ✅ Ticket fechado por {user}

Obrigado por jogar conosco! 🎮
```

### Criar Painel

```bash
/painel
    titulo: 🎮 Suporte do Servidor
    descricao: Precisa de ajuda? Abra um ticket selecionando a categoria apropriada abaixo!
    
    🔧 **Suporte Técnico** - Problemas com lag, conexão, etc
    🐛 **Bug Report** - Encontrou um bug? Reporte aqui
    🚨 **Denúncia** - Reporte jogadores infratores
    🎁 **Recompensas** - Reclame suas recompensas e prêmios
    cor: #FF6B6B
```

---

## 💼 Exemplo 2: Servidor de Vendas/E-commerce

### Configuração Inicial

```bash
/ticket-config categoria [categoria: ATENDIMENTO]
/ticket-config logs [canal: #vendas-logs]
/ticket-config cargo-suporte [cargo: @Vendedor]
/ticket-config limite-tickets limite:3
/ticket-config auto-deletar ativar:True minutos:15
```

### Categorias de Vendas

```bash
# Compras
/ticket-config categoria-ticket
    id_categoria: compras
    nome: Realizar Compra
    emoji: 💰
    descricao: Quero comprar um produto
    ativar: True

# Pagamento
/ticket-config categoria-ticket
    id_categoria: pagamento
    nome: Problemas com Pagamento
    emoji: 💳
    descricao: Problemas com pagamento ou checkout
    ativar: True

# Rastreamento
/ticket-config categoria-ticket
    id_categoria: rastreamento
    nome: Rastrear Pedido
    emoji: 📦
    descricao: Rastrear meu pedido
    ativar: True

# Trocas e Devoluções
/ticket-config categoria-ticket
    id_categoria: trocas
    nome: Trocas/Devoluções
    emoji: 🔄
    descricao: Solicitar troca ou devolução
    ativar: True

# Suporte Pós-Venda
/ticket-config categoria-ticket
    id_categoria: pos-venda
    nome: Suporte Pós-Venda
    emoji: 🛠️
    descricao: Suporte após a compra
    ativar: True
```

### Mensagens para E-commerce

```bash
/ticket-config mensagem-abertura
mensagem: 💼 Olá {user}! Obrigado por entrar em contato.

🛍️ Nossa equipe de vendas está pronta para ajudar!

⏰ Horário de atendimento: 9h às 18h
📱 Atendimento via ticket 24/7

Descreva como podemos ajudá-lo:

/ticket-config mensagem-fechamento
mensagem: ✅ Atendimento finalizado por {user}

Obrigado pela preferência! 💚
⭐ Avalie nosso atendimento em #avaliações
🛍️ Volte sempre!
```

---

## 🏫 Exemplo 3: Servidor Educacional

### Configuração

```bash
/ticket-config categoria [categoria: SUPORTE-ALUNOS]
/ticket-config logs [canal: #admin-logs]
/ticket-config cargo-suporte [cargo: @Professor]
/ticket-config limite-tickets limite:5
```

### Categorias Educacionais

```bash
# Dúvidas de Matéria
/ticket-config categoria-ticket
    id_categoria: duvidas
    nome: Dúvidas sobre Matéria
    emoji: 📚
    descricao: Tire suas dúvidas sobre o conteúdo
    ativar: True

# Problemas Técnicos
/ticket-config categoria-ticket
    id_categoria: tecnico
    nome: Suporte Técnico
    emoji: 💻
    descricao: Problemas com acesso ou plataforma
    ativar: True

# Solicitações
/ticket-config categoria-ticket
    id_categoria: solicitacoes
    nome: Solicitações
    emoji: 📝
    descricao: Solicitar certificados, declarações, etc
    ativar: True

# Feedback
/ticket-config categoria-ticket
    id_categoria: feedback
    nome: Feedback
    emoji: 💭
    descricao: Dar feedback sobre aulas ou conteúdo
    ativar: True
```

---

## 🎭 Exemplo 4: Servidor de Comunidade

### Configuração Básica

```bash
/ticket-config categoria [categoria: TICKETS]
/ticket-config logs [canal: #staff-logs]
/ticket-config cargo-suporte [cargo: @Staff]
/ticket-config transcrição ativar:True
```

### Categorias Comunitárias

```bash
# Suporte Geral
/ticket-config categoria-ticket
    id_categoria: suporte
    nome: Suporte Geral
    emoji: 🎫
    descricao: Preciso de ajuda geral
    ativar: True

# Denúncias
/ticket-config categoria-ticket
    id_categoria: report
    nome: Denúncias
    emoji: 🚨
    descricao: Reportar usuário ou conteúdo
    ativar: True

# Parcerias
/ticket-config categoria-ticket
    id_categoria: parceria
    nome: Parcerias
    emoji: 🤝
    descricao: Proposta de parceria
    ativar: True

# Sugestões
/ticket-config categoria-ticket
    id_categoria: sugestao
    nome: Sugestões
    emoji: 💡
    descricao: Dar sugestões para o servidor
    ativar: True

# Candidatura Staff
/ticket-config categoria-ticket
    id_categoria: candidatura
    nome: Candidatura Staff
    emoji: 👔
    descricao: Candidatar-se para a equipe
    ativar: True
```

---

## 🎪 Exemplo 5: Usando Emojis Personalizados

### Descobrir Emojis do Servidor

```bash
/emoji-list
```

Resultado:
```
😄 Emojis de MeuServidor

Estáticos (15)
:logo: :checkmark: :xmark: :ticket_icon: :staff_badge: ...

Animados (8)
:loading: :party: :celebrate: ...
```

### Usar Emojis Personalizados nas Categorias

```bash
# Copie o emoji da lista e use na criação
/ticket-config categoria-ticket
    id_categoria: vip
    nome: Suporte VIP
    emoji: :staff_badge:  # Cole o emoji personalizado aqui
    descricao: Suporte exclusivo para membros VIP
    ativar: True
```

---

## 🔄 Fluxo de Trabalho Completo

### Para Administradores

1. **Setup Inicial (Uma vez)**
```bash
/ticket-config categoria [categoria]
/ticket-config logs [canal]
/ticket-config cargo-suporte [cargo]
```

2. **Criar Categorias**
```bash
/ticket-config categoria-ticket [...]
# Repetir para cada categoria
```

3. **Personalizar Mensagens**
```bash
/ticket-config mensagem-abertura [...]
/ticket-config mensagem-fechamento [...]
```

4. **Criar Painel**
```bash
/painel
```

### Para Equipe de Suporte

1. **Quando entra ticket novo**
   - Clique em ✋ **Reivindicar**
   - Responda o usuário

2. **Durante o atendimento**
   - Use `/adicionar` se precisar de outro membro
   - Mantenha comunicação clara

3. **Ao finalizar**
   - Clique em 🔒 **Fechar** ou use `/fechar [motivo]`
   - Se necessário, clique em 📄 **Transcrição**

### Para Usuários

1. **Abrir Ticket**
   - Clique no painel
   - Selecione a categoria
   - Aguarde criação do canal

2. **No Ticket**
   - Descreva seu problema
   - Responda às perguntas da equipe
   - Aguarde resolução

3. **Fechar Ticket**
   - Clique em 🔒 ou use `/fechar`
   - Opcional: avalie o atendimento

---

## 📊 Monitoramento e Análise

### Ver Estatísticas

```bash
# Ver tickets abertos
/tickets status:abertos

# Ver seus tickets
/tickets status:meus

# Ver tickets fechados (últimos 25)
/tickets status:fechados
```

### Gerenciar Tickets

```bash
# Adicionar alguém ao ticket
/adicionar usuario:@fulano

# Remover alguém
/remover usuario:@fulano

# Fechar com motivo
/fechar motivo:Problema resolvido com sucesso

# Gerar transcrição manual
# Clique no botão 📄 no painel do ticket
```

---

## 🎨 Personalizações Avançadas

### Painel Customizado com Cores

```bash
/painel
    titulo: ✨ Central de Atendimento
    descricao: Escolha a opção que melhor se adequa à sua necessidade
    cor: #5865F2  # Azul Discord
    
# Outras cores úteis:
# Verde: #43B581
# Vermelho: #F04747
# Amarelo: #FAA61A
# Roxo: #9B59B6
# Rosa: #E91E63
```

### Mensagens com Formatação

```bash
/ticket-config mensagem-abertura
mensagem: **🎫 Bem-vindo ao Ticket #{ticket_id}**

Olá {user}! 👋

__Informações Importantes:__
• Nossa equipe foi notificada
• Responderemos em até 2 horas
• Mantenha a educação e respeito

**Descreva seu problema abaixo:**
```

---

## 💡 Dicas de Uso

### Melhor Performance

1. Configure auto-deleção para manter servidor limpo
2. Use limite de tickets para evitar spam
3. Ative transcrições para manter histórico
4. Configure logs para monitoramento

### Melhor Experiência

1. Use emojis consistentes e intuitivos
2. Mensagens claras e objetivas
3. Categorias bem definidas
4. Tempo de resposta razoável

### Organização

1. Uma categoria Discord para tickets
2. Um canal para logs
3. Cargos bem definidos para equipe
4. Revisar configurações regularmente

---

**📌 Estes são apenas exemplos! Adapte conforme sua necessidade.**

Volte ao `README.md` para documentação completa.
