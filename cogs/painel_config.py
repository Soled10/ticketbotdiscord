"""
Cog de Painel Interativo - Configuração completa via interface visual
"""
import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View, Select, Modal, TextInput
import asyncio

class ConfigModal(Modal):
    """Modal para configuração de mensagens"""
    def __init__(self, bot, config_type: str, guild_id: int):
        super().__init__(title=f"Configurar {config_type}")
        self.bot = bot
        self.config_type = config_type
        self.guild_id = guild_id
        
        if config_type == "Mensagem de Abertura":
            self.message_input = TextInput(
                label="Mensagem ao abrir ticket",
                style=discord.TextStyle.paragraph,
                placeholder="{user} {username} - Placeholders disponíveis",
                required=True,
                max_length=1000
            )
            self.add_item(self.message_input)
        elif config_type == "Mensagem de Fechamento":
            self.message_input = TextInput(
                label="Mensagem ao fechar ticket",
                style=discord.TextStyle.paragraph,
                placeholder="{user} - Placeholder disponível",
                required=True,
                max_length=1000
            )
            self.add_item(self.message_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        if self.config_type == "Mensagem de Abertura":
            self.bot.update_guild_config(self.guild_id, "ticket_message", self.message_input.value)
        elif self.config_type == "Mensagem de Fechamento":
            self.bot.update_guild_config(self.guild_id, "close_message", self.message_input.value)
        
        await interaction.response.send_message(f"✅ {self.config_type} atualizada!", ephemeral=True)

class CategoryModal(Modal):
    """Modal para criar/editar categoria de ticket"""
    def __init__(self, bot, guild_id: int):
        super().__init__(title="Criar Categoria de Ticket")
        self.bot = bot
        self.guild_id = guild_id
        
        self.cat_id = TextInput(
            label="ID da Categoria",
            placeholder="suporte, vendas, bug (sem espaços)",
            required=True,
            max_length=50
        )
        
        self.cat_name = TextInput(
            label="Nome da Categoria",
            placeholder="Suporte Geral",
            required=True,
            max_length=100
        )
        
        self.cat_emoji = TextInput(
            label="Emoji",
            placeholder="🎫 ou emoji personalizado",
            required=True,
            max_length=50
        )
        
        self.cat_desc = TextInput(
            label="Descrição",
            placeholder="Preciso de ajuda com algo",
            required=True,
            max_length=200,
            style=discord.TextStyle.paragraph
        )
        
        self.add_item(self.cat_id)
        self.add_item(self.cat_name)
        self.add_item(self.cat_emoji)
        self.add_item(self.cat_desc)
    
    async def on_submit(self, interaction: discord.Interaction):
        config = self.bot.get_guild_config(self.guild_id)
        
        config["ticket_categories"][self.cat_id.value] = {
            "name": self.cat_name.value,
            "emoji": self.cat_emoji.value,
            "description": self.cat_desc.value,
            "enabled": True
        }
        
        self.bot.save_configs()
        
        await interaction.response.send_message(
            f"✅ Categoria **{self.cat_emoji.value} {self.cat_name.value}** criada com sucesso!",
            ephemeral=True
        )

class FAQModal(Modal):
    """Modal para adicionar FAQ"""
    def __init__(self, bot, guild_id: int):
        super().__init__(title="Adicionar FAQ")
        self.bot = bot
        self.guild_id = guild_id
        
        self.question = TextInput(
            label="Pergunta",
            placeholder="Como posso...",
            required=True,
            max_length=200
        )
        
        self.answer = TextInput(
            label="Resposta",
            placeholder="Você pode...",
            required=True,
            max_length=1000,
            style=discord.TextStyle.paragraph
        )
        
        self.add_item(self.question)
        self.add_item(self.answer)
    
    async def on_submit(self, interaction: discord.Interaction):
        faq_data = self.bot.get_faq_data(self.guild_id)
        
        faq_data["faqs"].append({
            "question": self.question.value,
            "answer": self.answer.value,
            "id": len(faq_data["faqs"])
        })
        
        self.bot.save_faq_data()
        
        await interaction.response.send_message(
            f"✅ FAQ adicionada com sucesso!",
            ephemeral=True
        )

class PainelConfigView(View):
    """View principal do painel de configuração"""
    def __init__(self, bot, guild_id: int):
        super().__init__(timeout=300)
        self.bot = bot
        self.guild_id = guild_id
    
    @discord.ui.button(label="Canais & Cargos", style=discord.ButtonStyle.primary, emoji="📋", row=0)
    async def channels_roles(self, interaction: discord.Interaction, button: Button):
        """Configurar canais e cargos"""
        embed = discord.Embed(
            title="📋 Configuração de Canais & Cargos",
            description="Use os comandos abaixo para configurar:",
            color=discord.Color.blue()
        )
        
        config = self.bot.get_guild_config(self.guild_id)
        
        cat = f"<#{config['ticket_category']}>" if config['ticket_category'] else "❌ Não configurado"
        logs = f"<#{config['ticket_logs']}>" if config['ticket_logs'] else "❌ Não configurado"
        support = f"<@&{config['support_role']}>" if config['support_role'] else "❌ Não configurado"
        notif = f"<@&{config.get('notification_role')}>" if config.get('notification_role') else "❌ Não configurado"
        
        embed.add_field(
            name="Status Atual",
            value=f"**Categoria:** {cat}\n**Logs:** {logs}\n**Suporte:** {support}\n**Notificação:** {notif}",
            inline=False
        )
        
        embed.add_field(
            name="Como Configurar",
            value="`/config-rapida categoria` - Define categoria dos tickets\n"
                  "`/config-rapida logs` - Define canal de logs\n"
                  "`/config-rapida suporte` - Define cargo de suporte\n"
                  "`/config-rapida notificacao` - Define cargo para notificações",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @discord.ui.button(label="Mensagens", style=discord.ButtonStyle.primary, emoji="💬", row=0)
    async def messages(self, interaction: discord.Interaction, button: Button):
        """Configurar mensagens"""
        view = View(timeout=60)
        
        async def open_callback(inter: discord.Interaction):
            modal = ConfigModal(self.bot, "Mensagem de Abertura", self.guild_id)
            await inter.response.send_modal(modal)
        
        async def close_callback(inter: discord.Interaction):
            modal = ConfigModal(self.bot, "Mensagem de Fechamento", self.guild_id)
            await inter.response.send_modal(modal)
        
        open_btn = Button(label="Abertura", style=discord.ButtonStyle.green, emoji="📥")
        close_btn = Button(label="Fechamento", style=discord.ButtonStyle.red, emoji="📤")
        
        open_btn.callback = open_callback
        close_btn.callback = close_callback
        
        view.add_item(open_btn)
        view.add_item(close_btn)
        
        config = self.bot.get_guild_config(self.guild_id)
        
        embed = discord.Embed(
            title="💬 Configuração de Mensagens",
            description="Clique nos botões para editar as mensagens",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="📥 Mensagem de Abertura",
            value=config['ticket_message'][:100] + "...",
            inline=False
        )
        
        embed.add_field(
            name="📤 Mensagem de Fechamento",
            value=config['close_message'][:100] + "...",
            inline=False
        )
        
        embed.add_field(
            name="💡 Placeholders",
            value="`{user}` - Menção do usuário\n`{username}` - Nome do usuário\n`{server}` - Nome do servidor",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    @discord.ui.button(label="Categorias", style=discord.ButtonStyle.primary, emoji="🎫", row=0)
    async def categories(self, interaction: discord.Interaction, button: Button):
        """Gerenciar categorias de tickets"""
        view = View(timeout=60)
        
        async def add_callback(inter: discord.Interaction):
            modal = CategoryModal(self.bot, self.guild_id)
            await inter.response.send_modal(modal)
        
        async def list_callback(inter: discord.Interaction):
            config = self.bot.get_guild_config(self.guild_id)
            categories = config['ticket_categories']
            
            embed = discord.Embed(
                title="🎫 Categorias de Ticket",
                color=discord.Color.blue()
            )
            
            for cat_id, cat_data in categories.items():
                status = "✅ Ativa" if cat_data['enabled'] else "❌ Inativa"
                embed.add_field(
                    name=f"{cat_data['emoji']} {cat_data['name']}",
                    value=f"**ID:** `{cat_id}`\n**Descrição:** {cat_data['description']}\n**Status:** {status}",
                    inline=True
                )
            
            await inter.response.send_message(embed=embed, ephemeral=True)
        
        add_btn = Button(label="Adicionar", style=discord.ButtonStyle.green, emoji="➕")
        list_btn = Button(label="Listar", style=discord.ButtonStyle.secondary, emoji="📋")
        
        add_btn.callback = add_callback
        list_btn.callback = list_callback
        
        view.add_item(add_btn)
        view.add_item(list_btn)
        
        embed = discord.Embed(
            title="🎫 Gerenciar Categorias",
            description="Adicione ou visualize categorias de tickets",
            color=discord.Color.blue()
        )
        
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    @discord.ui.button(label="Automação", style=discord.ButtonStyle.secondary, emoji="🤖", row=1)
    async def automation(self, interaction: discord.Interaction, button: Button):
        """Configurar automação"""
        config = self.bot.get_guild_config(self.guild_id)
        
        embed = discord.Embed(
            title="🤖 Configurações de Automação",
            color=discord.Color.blue()
        )
        
        auto_del = "✅ Ativo" if config['auto_delete_closed'] else "❌ Inativo"
        transcript = "✅ Ativo" if config['transcript_enabled'] else "❌ Inativo"
        ai_enabled = "✅ Ativo" if config.get('ai_enabled', False) else "❌ Inativo"
        ai_auto = "✅ Ativo" if config.get('ai_auto_respond', False) else "❌ Inativo"
        
        embed.add_field(
            name="Status Atual",
            value=f"**Auto-deletar:** {auto_del} ({config['delete_after_minutes']}min)\n"
                  f"**Transcrições:** {transcript}\n"
                  f"**IA Ativada:** {ai_enabled}\n"
                  f"**IA Auto-resposta:** {ai_auto}",
            inline=False
        )
        
        embed.add_field(
            name="Comandos",
            value="`/automacao auto-deletar` - Configurar deleção automática\n"
                  "`/automacao transcricao` - Ativar/desativar transcrições\n"
                  "`/automacao ia` - Configurar assistente IA\n"
                  "`/automacao limite` - Definir limite de tickets por usuário",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @discord.ui.button(label="FAQ", style=discord.ButtonStyle.secondary, emoji="❓", row=1)
    async def faq_config(self, interaction: discord.Interaction, button: Button):
        """Configurar FAQ"""
        view = View(timeout=60)
        
        async def add_faq_callback(inter: discord.Interaction):
            modal = FAQModal(self.bot, self.guild_id)
            await inter.response.send_modal(modal)
        
        async def list_faq_callback(inter: discord.Interaction):
            faq_data = self.bot.get_faq_data(self.guild_id)
            faqs = faq_data['faqs']
            
            if not faqs:
                await inter.response.send_message("❌ Nenhuma FAQ cadastrada ainda!", ephemeral=True)
                return
            
            embed = discord.Embed(
                title="❓ FAQs Cadastradas",
                color=discord.Color.blue()
            )
            
            for faq in faqs[:10]:
                embed.add_field(
                    name=f"❓ {faq['question']}",
                    value=f"{faq['answer'][:100]}...\n**ID:** {faq['id']}",
                    inline=False
                )
            
            if len(faqs) > 10:
                embed.set_footer(text=f"Mostrando 10 de {len(faqs)} FAQs")
            
            await inter.response.send_message(embed=embed, ephemeral=True)
        
        add_btn = Button(label="Adicionar FAQ", style=discord.ButtonStyle.green, emoji="➕")
        list_btn = Button(label="Ver FAQs", style=discord.ButtonStyle.secondary, emoji="📋")
        
        add_btn.callback = add_faq_callback
        list_btn.callback = list_faq_callback
        
        view.add_item(add_btn)
        view.add_item(list_btn)
        
        embed = discord.Embed(
            title="❓ Gerenciar FAQs",
            description="Adicione perguntas frequentes que a IA pode usar para ajudar",
            color=discord.Color.blue()
        )
        
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    @discord.ui.button(label="Estatísticas", style=discord.ButtonStyle.secondary, emoji="📊", row=1)
    async def stats_view(self, interaction: discord.Interaction, button: Button):
        """Ver estatísticas"""
        stats = self.bot.get_statistics(self.guild_id)
        
        embed = discord.Embed(
            title="📊 Estatísticas do Sistema",
            color=discord.Color.blue()
        )
        
        embed.add_field(name="🎫 Total de Tickets", value=stats['total_tickets'], inline=True)
        
        # Média de avaliação
        if stats['satisfaction_ratings']:
            avg_rating = sum(stats['satisfaction_ratings']) / len(stats['satisfaction_ratings'])
            embed.add_field(name="⭐ Avaliação Média", value=f"{avg_rating:.1f}/5", inline=True)
        else:
            embed.add_field(name="⭐ Avaliação Média", value="Sem dados", inline=True)
        
        # Tickets por categoria
        if stats['tickets_by_category']:
            top_cat = max(stats['tickets_by_category'].items(), key=lambda x: x[1])
            embed.add_field(name="📋 Categoria Mais Usada", value=f"{top_cat[0]} ({top_cat[1]})", inline=True)
        
        embed.add_field(
            name="⏱️ Tempo Médio",
            value=f"Resposta: {stats['average_response_time']}min\nResolução: {stats['average_resolution_time']}min",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @discord.ui.button(label="Criar Painel", style=discord.ButtonStyle.success, emoji="🎯", row=2)
    async def create_panel(self, interaction: discord.Interaction, button: Button):
        """Criar painel de tickets"""
        config = self.bot.get_guild_config(self.guild_id)
        
        if not config.get('ticket_category'):
            await interaction.response.send_message(
                "❌ Configure uma categoria primeiro! Use o botão **Canais & Cargos**",
                ephemeral=True
            )
            return
        
        # Verificar categorias ativas
        categories = config.get('ticket_categories', {})
        active_cats = [c for c in categories.values() if c.get('enabled', True)]
        
        if not active_cats:
            await interaction.response.send_message(
                "❌ Configure pelo menos uma categoria de ticket! Use o botão **Categorias**",
                ephemeral=True
            )
            return
        
        # Criar painel
        cog = self.bot.get_cog('TicketSystem')
        if cog:
            await cog.create_panel_in_channel(interaction.channel, interaction.guild_id)
            await interaction.response.send_message("✅ Painel criado no canal atual!", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Erro ao criar painel!", ephemeral=True)

class PainelConfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="painel", description="Abre o painel de configuração completo")
    @app_commands.checks.has_permissions(administrator=True)
    async def painel(self, interaction: discord.Interaction):
        """Comando principal do painel de configuração"""
        embed = discord.Embed(
            title="⚙️ Painel de Configuração",
            description="Configure todo o sistema de tickets de forma visual e interativa!",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="📋 Canais & Cargos",
            value="Configure onde os tickets serão criados, logs, e cargos da equipe",
            inline=False
        )
        
        embed.add_field(
            name="💬 Mensagens",
            value="Personalize mensagens de abertura e fechamento de tickets",
            inline=False
        )
        
        embed.add_field(
            name="🎫 Categorias",
            value="Adicione e gerencie categorias de tickets personalizadas",
            inline=False
        )
        
        embed.add_field(
            name="🤖 Automação",
            value="Configure auto-deleção, transcrições, IA e mais",
            inline=False
        )
        
        embed.add_field(
            name="❓ FAQ",
            value="Adicione perguntas frequentes para a IA ajudar automaticamente",
            inline=False
        )
        
        embed.add_field(
            name="📊 Estatísticas",
            value="Visualize estatísticas e métricas do sistema",
            inline=False
        )
        
        embed.set_footer(text="Use os botões abaixo para navegar • Timeout: 5 minutos")
        
        view = PainelConfigView(self.bot, interaction.guild_id)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    # Comandos rápidos auxiliares
    @app_commands.command(name="config-rapida", description="Configuração rápida de canais e cargos")
    @app_commands.describe(
        opcao="O que deseja configurar",
        canal="Canal (para categoria/logs)",
        cargo="Cargo (para suporte/notificação)"
    )
    @app_commands.choices(opcao=[
        app_commands.Choice(name="Categoria", value="categoria"),
        app_commands.Choice(name="Logs", value="logs"),
        app_commands.Choice(name="Suporte", value="suporte"),
        app_commands.Choice(name="Notificação", value="notificacao")
    ])
    @app_commands.checks.has_permissions(administrator=True)
    async def config_rapida(
        self,
        interaction: discord.Interaction,
        opcao: str,
        canal: discord.TextChannel = None,
        cargo: discord.Role = None
    ):
        """Configuração rápida"""
        if opcao in ["categoria", "logs"] and not canal:
            await interaction.response.send_message("❌ Especifique um canal!", ephemeral=True)
            return
        
        if opcao in ["suporte", "notificacao"] and not cargo:
            await interaction.response.send_message("❌ Especifique um cargo!", ephemeral=True)
            return
        
        config_map = {
            "categoria": ("ticket_category", canal.id if canal else None, canal.mention if canal else ""),
            "logs": ("ticket_logs", canal.id if canal else None, canal.mention if canal else ""),
            "suporte": ("support_role", cargo.id if cargo else None, cargo.mention if cargo else ""),
            "notificacao": ("notification_role", cargo.id if cargo else None, cargo.mention if cargo else "")
        }
        
        key, value, mention = config_map[opcao]
        self.bot.update_guild_config(interaction.guild_id, key, value)
        
        await interaction.response.send_message(
            f"✅ **{opcao.title()}** configurado para {mention}",
            ephemeral=True
        )
    
    @app_commands.command(name="automacao", description="Configurar automações do sistema")
    @app_commands.describe(
        tipo="Tipo de automação",
        ativar="Ativar ou desativar",
        valor="Valor adicional (minutos, etc)"
    )
    @app_commands.choices(tipo=[
        app_commands.Choice(name="Auto-deletar", value="auto_delete"),
        app_commands.Choice(name="Transcrição", value="transcript"),
        app_commands.Choice(name="IA Ativada", value="ai_enabled"),
        app_commands.Choice(name="IA Auto-resposta", value="ai_auto"),
        app_commands.Choice(name="Limite de Tickets", value="limit")
    ])
    @app_commands.checks.has_permissions(administrator=True)
    async def automacao(
        self,
        interaction: discord.Interaction,
        tipo: str,
        ativar: bool = None,
        valor: int = None
    ):
        """Configurar automações"""
        config = self.bot.get_guild_config(interaction.guild_id)
        
        if tipo == "auto_delete":
            if ativar is not None:
                config['auto_delete_closed'] = ativar
            if valor:
                config['delete_after_minutes'] = min(60, max(1, valor))
            self.bot.save_configs()
            
            status = "ativada" if config['auto_delete_closed'] else "desativada"
            await interaction.response.send_message(
                f"✅ Auto-deleção {status} (deletar após {config['delete_after_minutes']} minutos)",
                ephemeral=True
            )
        
        elif tipo == "transcript":
            if ativar is not None:
                config['transcript_enabled'] = ativar
                self.bot.save_configs()
                status = "ativadas" if ativar else "desativadas"
                await interaction.response.send_message(f"✅ Transcrições {status}", ephemeral=True)
        
        elif tipo == "ai_enabled":
            if ativar is not None:
                config['ai_enabled'] = ativar
                self.bot.save_configs()
                status = "ativada" if ativar else "desativada"
                await interaction.response.send_message(f"✅ IA {status}", ephemeral=True)
        
        elif tipo == "ai_auto":
            if ativar is not None:
                config['ai_auto_respond'] = ativar
                self.bot.save_configs()
                status = "ativada" if ativar else "desativada"
                await interaction.response.send_message(f"✅ Auto-resposta da IA {status}", ephemeral=True)
        
        elif tipo == "limit":
            if valor:
                config['max_tickets_per_user'] = min(10, max(1, valor))
                self.bot.save_configs()
                await interaction.response.send_message(
                    f"✅ Limite de tickets por usuário: {config['max_tickets_per_user']}",
                    ephemeral=True
                )

async def setup(bot):
    await bot.add_cog(PainelConfig(bot))
