"""
Cog de Sistema de Tickets - Gerencia criação e painel de tickets
"""
import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View, Select
import asyncio
from datetime import datetime
import re

class TicketCreateView(View):
    def __init__(self, bot, guild_id: int):
        super().__init__(timeout=None)
        self.bot = bot
        self.guild_id = guild_id
        
        # Adicionar select menu com categorias
        config = bot.get_guild_config(guild_id)
        categories = config.get('ticket_categories', {})
        
        options = []
        for cat_id, cat_data in categories.items():
            if cat_data.get('enabled', True):
                # Processar emoji personalizado se necessário
                emoji = cat_data.get('emoji', '🎫')
                
                options.append(
                    discord.SelectOption(
                        label=cat_data['name'],
                        description=cat_data['description'][:100],
                        emoji=emoji,
                        value=cat_id
                    )
                )
        
        if options:
            select = Select(
                placeholder="🎫 Selecione o tipo de ticket...",
                options=options,
                custom_id=f"ticket_select_{guild_id}"
            )
            select.callback = self.select_callback
            self.add_item(select)
    
    async def select_callback(self, interaction: discord.Interaction):
        """Callback quando usuário seleciona uma categoria"""
        category_id = interaction.data['values'][0]
        
        # Criar o ticket
        cog = self.bot.get_cog('TicketSystem')
        if cog:
            await cog.create_ticket(interaction, category_id)

class TicketControlView(View):
    def __init__(self, bot, ticket_channel_id: int):
        super().__init__(timeout=None)
        self.bot = bot
        self.ticket_channel_id = ticket_channel_id
    
    @discord.ui.button(label="Fechar", style=discord.ButtonStyle.danger, emoji="🔒", custom_id="close_ticket")
    async def close_button(self, interaction: discord.Interaction, button: Button):
        """Botão para fechar ticket"""
        cog = self.bot.get_cog('TicketManagement')
        if cog:
            await cog.close_ticket_interaction(interaction)
    
    @discord.ui.button(label="Reivindicar", style=discord.ButtonStyle.primary, emoji="✋", custom_id="claim_ticket")
    async def claim_button(self, interaction: discord.Interaction, button: Button):
        """Botão para reivindicar ticket"""
        cog = self.bot.get_cog('TicketManagement')
        if cog:
            await cog.claim_ticket_interaction(interaction)
    
    @discord.ui.button(label="Transcrição", style=discord.ButtonStyle.secondary, emoji="📄", custom_id="transcript_ticket")
    async def transcript_button(self, interaction: discord.Interaction, button: Button):
        """Botão para gerar transcrição"""
        cog = self.bot.get_cog('TicketManagement')
        if cog:
            await cog.transcript_interaction(interaction)

class TicketSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="painel", description="Cria um painel para abertura de tickets")
    @app_commands.describe(
        titulo="Título do painel",
        descricao="Descrição do painel",
        cor="Cor do embed (hex, ex: #FF0000)"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def create_panel(
        self, 
        interaction: discord.Interaction, 
        titulo: str = "🎫 Sistema de Tickets",
        descricao: str = "Clique no botão abaixo para abrir um ticket!",
        cor: str = "#5865F2"
    ):
        """Cria um painel de tickets"""
        config = self.bot.get_guild_config(interaction.guild_id)
        
        # Verificar se está configurado
        if not config.get('ticket_category'):
            await interaction.response.send_message(
                "❌ Configure uma categoria primeiro usando `/ticket-config categoria`",
                ephemeral=True
            )
            return
        
        # Verificar se há categorias ativas
        categories = config.get('ticket_categories', {})
        active_cats = [c for c in categories.values() if c.get('enabled', True)]
        
        if not active_cats:
            await interaction.response.send_message(
                "❌ Configure pelo menos uma categoria de ticket ativa!",
                ephemeral=True
            )
            return
        
        # Converter cor
        try:
            color = discord.Color(int(cor.replace("#", ""), 16))
        except:
            color = discord.Color.blue()
        
        # Criar embed
        embed = discord.Embed(
            title=titulo,
            description=descricao,
            color=color
        )
        
        # Adicionar categorias disponíveis
        cat_text = []
        for cat_data in active_cats:
            cat_text.append(f"{cat_data['emoji']} **{cat_data['name']}** - {cat_data['description']}")
        
        embed.add_field(
            name="📋 Categorias Disponíveis",
            value="\n".join(cat_text),
            inline=False
        )
        
        embed.add_field(
            name="ℹ️ Como usar",
            value="Selecione o tipo de ticket no menu abaixo e aguarde a criação do seu canal privado.",
            inline=False
        )
        
        if interaction.guild.icon:
            embed.set_thumbnail(url=interaction.guild.icon.url)
        
        embed.set_footer(text=f"{interaction.guild.name} • Sistema de Tickets")
        
        # Criar view com botões
        view = TicketCreateView(self.bot, interaction.guild_id)
        
        # Enviar painel
        await interaction.channel.send(embed=embed, view=view)
        await interaction.response.send_message("✅ Painel de tickets criado!", ephemeral=True)
    
    async def create_ticket(self, interaction: discord.Interaction, category_id: str):
        """Cria um novo ticket"""
        config = self.bot.get_guild_config(interaction.guild_id)
        tickets_data = self.bot.get_tickets_data(interaction.guild_id)
        
        # Verificar limite de tickets por usuário
        user_id_str = str(interaction.user.id)
        user_tickets = tickets_data.get('user_tickets', {}).get(user_id_str, [])
        max_tickets = config.get('max_tickets_per_user', 3)
        
        if len(user_tickets) >= max_tickets:
            await interaction.response.send_message(
                f"❌ Você já atingiu o limite de **{max_tickets}** tickets abertos!",
                ephemeral=True
            )
            return
        
        # Verificar categoria do Discord
        category_channel = self.bot.get_channel(config['ticket_category'])
        if not category_channel:
            await interaction.response.send_message(
                "❌ Categoria de tickets não configurada corretamente!",
                ephemeral=True
            )
            return
        
        await interaction.response.defer(ephemeral=True)
        
        # Incrementar contador
        config['ticket_counter'] += 1
        ticket_number = config['ticket_counter']
        self.bot.save_configs()
        
        # Obter dados da categoria
        cat_data = config['ticket_categories'].get(category_id, {})
        cat_name = cat_data.get('name', 'Ticket')
        cat_emoji = cat_data.get('emoji', '🎫')
        
        # Criar canal
        try:
            # Configurar permissões
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                interaction.user: discord.PermissionOverwrite(
                    read_messages=True,
                    send_messages=True,
                    attach_files=True,
                    embed_links=True
                ),
                interaction.guild.me: discord.PermissionOverwrite(
                    read_messages=True,
                    send_messages=True,
                    manage_channels=True,
                    manage_messages=True
                )
            }
            
            # Adicionar cargo de suporte
            if config.get('support_role'):
                support_role = interaction.guild.get_role(config['support_role'])
                if support_role:
                    overwrites[support_role] = discord.PermissionOverwrite(
                        read_messages=True,
                        send_messages=True,
                        attach_files=True,
                        embed_links=True
                    )
            
            # Nome do canal
            channel_name = f"ticket-{ticket_number:04d}"
            
            # Criar canal
            ticket_channel = await category_channel.create_text_channel(
                name=channel_name,
                overwrites=overwrites,
                topic=f"Ticket de {interaction.user.name} | Categoria: {cat_name} | ID: {ticket_number}"
            )
            
            # Salvar dados do ticket
            ticket_info = {
                "id": ticket_number,
                "channel_id": ticket_channel.id,
                "user_id": interaction.user.id,
                "category": category_id,
                "created_at": datetime.utcnow().isoformat(),
                "claimed_by": None,
                "closed": False
            }
            
            tickets_data['active_tickets'][str(ticket_channel.id)] = ticket_info
            
            if user_id_str not in tickets_data['user_tickets']:
                tickets_data['user_tickets'][user_id_str] = []
            tickets_data['user_tickets'][user_id_str].append(ticket_channel.id)
            
            self.bot.save_tickets_data()
            
            # Mensagem de boas-vindas no ticket
            welcome_message = config.get('ticket_message', 'Olá {user}! Obrigado por abrir um ticket.')
            welcome_message = welcome_message.replace('{user}', interaction.user.mention)
            welcome_message = welcome_message.replace('{username}', interaction.user.name)
            
            embed = discord.Embed(
                title=f"{cat_emoji} {cat_name} - Ticket #{ticket_number:04d}",
                description=welcome_message,
                color=discord.Color.green(),
                timestamp=datetime.utcnow()
            )
            
            embed.add_field(name="📝 Categoria", value=f"{cat_emoji} {cat_name}", inline=True)
            embed.add_field(name="👤 Aberto por", value=interaction.user.mention, inline=True)
            embed.add_field(name="🆔 ID do Ticket", value=f"#{ticket_number:04d}", inline=True)
            
            embed.set_footer(text="Use os botões abaixo para gerenciar este ticket")
            
            # Enviar mensagem com controles
            view = TicketControlView(self.bot, ticket_channel.id)
            await ticket_channel.send(
                content=f"{interaction.user.mention}",
                embed=embed,
                view=view
            )
            
            # Log
            await self.log_ticket_action(
                interaction.guild_id,
                "Ticket Aberto",
                interaction.user,
                ticket_channel,
                f"Categoria: {cat_emoji} {cat_name}"
            )
            
            await interaction.followup.send(
                f"✅ Ticket criado! {ticket_channel.mention}",
                ephemeral=True
            )
            
        except Exception as e:
            await interaction.followup.send(
                f"❌ Erro ao criar ticket: {str(e)}",
                ephemeral=True
            )
    
    async def log_ticket_action(self, guild_id: int, action: str, user: discord.User, channel: discord.TextChannel = None, details: str = ""):
        """Registra ação de ticket no canal de logs"""
        config = self.bot.get_guild_config(guild_id)
        log_channel_id = config.get('ticket_logs')
        
        if not log_channel_id:
            return
        
        try:
            log_channel = self.bot.get_channel(log_channel_id)
            if not log_channel:
                return
            
            embed = discord.Embed(
                title=f"📋 {action}",
                color=discord.Color.blue(),
                timestamp=datetime.utcnow()
            )
            
            embed.add_field(name="👤 Usuário", value=user.mention, inline=True)
            if channel:
                embed.add_field(name="📢 Canal", value=channel.mention, inline=True)
            if details:
                embed.add_field(name="📝 Detalhes", value=details, inline=False)
            
            embed.set_footer(text=f"ID do Usuário: {user.id}")
            
            await log_channel.send(embed=embed)
        except:
            pass

async def setup(bot):
    await bot.add_cog(TicketSystem(bot))
