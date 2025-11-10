"""
Cog de Utilidades - Comandos úteis e informativos para o sistema de tickets
"""
import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
import platform

class Utilidades(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="ajuda", description="Mostra todos os comandos disponíveis")
    async def help(self, interaction: discord.Interaction):
        """Comando de ajuda principal"""
        embed = discord.Embed(
            title="🎫 Central de Ajuda - Bot de Tickets",
            description="Sistema completo de tickets configurável via Discord!",
            color=discord.Color.blue()
        )
        
        # Configuração
        config_commands = """
        `/ticket-config categoria` - Define categoria dos tickets
        `/ticket-config logs` - Define canal de logs
        `/ticket-config cargo-suporte` - Define cargo da equipe
        `/ticket-config mensagem-abertura` - Mensagem ao abrir
        `/ticket-config mensagem-fechamento` - Mensagem ao fechar
        `/ticket-config limite-tickets` - Limite por usuário
        `/ticket-config auto-deletar` - Auto-deletar tickets fechados
        `/ticket-config transcrição` - Ativar/desativar transcrições
        `/ticket-config categoria-ticket` - Criar categorias personalizadas
        `/ticket-config ver` - Ver todas as configurações
        """
        embed.add_field(name="⚙️ Configuração", value=config_commands, inline=False)
        
        # Sistema de Tickets
        ticket_commands = """
        `/painel` - Criar painel de abertura de tickets
        `/fechar` - Fechar o ticket atual
        `/adicionar` - Adicionar usuário ao ticket
        `/remover` - Remover usuário do ticket
        `/tickets` - Ver tickets abertos/fechados
        """
        embed.add_field(name="🎫 Tickets", value=ticket_commands, inline=False)
        
        # Utilidades
        util_commands = """
        `/ajuda` - Mostra esta mensagem
        `/botinfo` - Informações do bot
        `/ping` - Verifica latência
        `/emoji-list` - Lista emojis do servidor
        """
        embed.add_field(name="🔧 Utilidades", value=util_commands, inline=False)
        
        # Emojis personalizados
        emoji_info = """
        O bot suporta emojis personalizados do servidor!
        Configure emojis nas categorias de ticket
        Use emojis nas mensagens personalizadas
        Veja os emojis com `/emoji-list`
        """
        embed.add_field(name="😄 Emojis Personalizados", value=emoji_info, inline=False)
        
        embed.set_footer(text="Bot de Tickets • Totalmente configurável via Discord")
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="tickets", description="Lista tickets abertos ou fechados")
    @app_commands.describe(status="Status dos tickets a listar")
    @app_commands.choices(status=[
        app_commands.Choice(name="Abertos", value="open"),
        app_commands.Choice(name="Fechados", value="closed"),
        app_commands.Choice(name="Meus Tickets", value="mine")
    ])
    async def list_tickets(self, interaction: discord.Interaction, status: str = "open"):
        """Lista tickets"""
        tickets_data = self.bot.get_tickets_data(interaction.guild_id)
        
        embed = discord.Embed(
            title="🎫 Lista de Tickets",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        
        if status == "open":
            active = tickets_data.get('active_tickets', {})
            if not active:
                embed.description = "Nenhum ticket aberto no momento."
            else:
                ticket_list = []
                for channel_id, ticket in active.items():
                    user = interaction.guild.get_member(ticket['user_id'])
                    claimed = ""
                    if ticket.get('claimed_by'):
                        claimer = interaction.guild.get_member(ticket['claimed_by'])
                        claimed = f" | ✋ {claimer.mention if claimer else 'Alguém'}"
                    
                    ticket_list.append(
                        f"<#{channel_id}> - #{ticket['id']:04d} | {user.mention if user else 'Usuário Desconhecido'}{claimed}"
                    )
                
                embed.description = "\n".join(ticket_list[:25])
                if len(ticket_list) > 25:
                    embed.set_footer(text=f"Mostrando 25 de {len(ticket_list)} tickets")
        
        elif status == "closed":
            closed = tickets_data.get('closed_tickets', [])
            if not closed:
                embed.description = "Nenhum ticket fechado registrado."
            else:
                # Pegar os últimos 25
                recent = closed[-25:][::-1]
                ticket_list = []
                for ticket in recent:
                    user = interaction.guild.get_member(ticket['user_id'])
                    closed_by = interaction.guild.get_member(ticket.get('closed_by', 0))
                    
                    ticket_list.append(
                        f"#{ticket['id']:04d} | {user.name if user else 'Desconhecido'} | "
                        f"Fechado por {closed_by.name if closed_by else 'Desconhecido'}"
                    )
                
                embed.description = "\n".join(ticket_list)
                embed.set_footer(text=f"Total de tickets fechados: {len(closed)}")
        
        elif status == "mine":
            user_id_str = str(interaction.user.id)
            user_tickets = tickets_data.get('user_tickets', {}).get(user_id_str, [])
            
            if not user_tickets:
                embed.description = "Você não tem tickets abertos."
            else:
                ticket_list = []
                for channel_id in user_tickets:
                    ticket = tickets_data['active_tickets'].get(str(channel_id))
                    if ticket:
                        ticket_list.append(f"<#{channel_id}> - #{ticket['id']:04d} | Categoria: {ticket['category']}")
                
                embed.description = "\n".join(ticket_list) if ticket_list else "Nenhum ticket aberto encontrado."
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="botinfo", description="Mostra informações do bot")
    async def botinfo(self, interaction: discord.Interaction):
        """Informações sobre o bot"""
        embed = discord.Embed(
            title="🤖 Bot de Tickets",
            description="Sistema completo de tickets configurável via Discord",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        
        # Estatísticas
        total_tickets = sum(
            len(data.get('closed_tickets', [])) + len(data.get('active_tickets', {}))
            for data in self.bot.tickets_data.values()
        )
        
        embed.add_field(name="📊 Servidores", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="🎫 Tickets Criados", value=total_tickets, inline=True)
        embed.add_field(name="💬 Comandos", value=len(self.bot.tree.get_commands()), inline=True)
        
        # Informações técnicas
        embed.add_field(name="🐍 Python", value=platform.python_version(), inline=True)
        embed.add_field(name="📚 Discord.py", value=discord.__version__, inline=True)
        embed.add_field(name="⏱️ Ping", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        
        # Recursos
        features = """
        ✅ Slash Commands
        ✅ Configuração Total via Discord
        ✅ Categorias Personalizadas
        ✅ Painel com Select Menu
        ✅ Emojis Personalizados
        ✅ Sistema de Logs
        ✅ Transcrições HTML
        ✅ Auto-deleção Configurável
        ✅ Sistema de Reivindicação
        ✅ Gerenciamento de Usuários
        """
        embed.add_field(name="🌟 Recursos", value=features, inline=False)
        
        embed.set_footer(text="Bot de Tickets • 100% configurável")
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="ping", description="Verifica a latência do bot")
    async def ping(self, interaction: discord.Interaction):
        """Mostra a latência do bot"""
        latency = round(self.bot.latency * 1000)
        
        if latency < 100:
            emoji = "🟢"
            status = "Excelente"
            color = discord.Color.green()
        elif latency < 200:
            emoji = "🟡"
            status = "Bom"
            color = discord.Color.gold()
        else:
            emoji = "🔴"
            status = "Alto"
            color = discord.Color.red()
        
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"{emoji} Latência: **{latency}ms** ({status})",
            color=color
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="emoji-list", description="Lista todos os emojis personalizados do servidor")
    async def emoji_list(self, interaction: discord.Interaction):
        """Lista os emojis personalizados do servidor"""
        guild = interaction.guild
        emojis = guild.emojis
        
        if not emojis:
            await interaction.response.send_message("❌ Este servidor não possui emojis personalizados!", ephemeral=True)
            return
        
        embed = discord.Embed(
            title=f"😄 Emojis de {guild.name}",
            description=f"Total: {len(emojis)} emojis\n\nVocê pode usar estes emojis nas configurações do bot!",
            color=discord.Color.blue()
        )
        
        # Separar estáticos e animados
        static_emojis = [e for e in emojis if not e.animated]
        animated_emojis = [e for e in emojis if e.animated]
        
        if static_emojis:
            static_text = " ".join([str(e) for e in static_emojis[:50]])
            if len(static_emojis) > 50:
                static_text += f"\n... e mais {len(static_emojis) - 50} emojis"
            embed.add_field(name=f"Estáticos ({len(static_emojis)})", value=static_text, inline=False)
        
        if animated_emojis:
            animated_text = " ".join([str(e) for e in animated_emojis[:50]])
            if len(animated_emojis) > 50:
                animated_text += f"\n... e mais {len(animated_emojis) - 50} emojis"
            embed.add_field(name=f"Animados ({len(animated_emojis)})", value=animated_text, inline=False)
        
        embed.add_field(
            name="💡 Como usar",
            value="Copie o emoji e cole nas configurações das categorias de ticket!",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Utilidades(bot))
