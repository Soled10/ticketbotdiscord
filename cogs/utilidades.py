"""
Cog de Utilidades - Comandos úteis e informativos
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
            title="📚 Central de Ajuda - Bot Configurável",
            description="Aqui estão todos os comandos disponíveis organizados por categoria:",
            color=discord.Color.blue()
        )
        
        # Configuração
        config_commands = """
        `/config canal_boas_vindas` - Define canal de boas-vindas
        `/config canal_despedida` - Define canal de despedida
        `/config canal_logs` - Define canal de logs
        `/config cargo_moderador` - Define cargo de moderador
        `/config cargo_automatico` - Define cargo automático
        `/config mensagem_boas_vindas` - Personaliza mensagem de boas-vindas
        `/config mensagem_despedida` - Personaliza mensagem de despedida
        `/config modulo` - Ativa/desativa módulos
        `/config ver` - Ver todas as configurações
        `/config resetar` - Reseta configurações
        """
        embed.add_field(name="⚙️ Configuração", value=config_commands, inline=False)
        
        # Moderação
        mod_commands = """
        `/kick` - Expulsa um membro
        `/ban` - Bane um membro
        `/unban` - Remove banimento
        `/timeout` - Coloca membro em timeout
        `/limpar` - Limpa mensagens do canal
        """
        embed.add_field(name="🛡️ Moderação", value=mod_commands, inline=False)
        
        # Utilidades
        util_commands = """
        `/ajuda` - Mostra esta mensagem
        `/serverinfo` - Informações do servidor
        `/userinfo` - Informações de um usuário
        `/botinfo` - Informações do bot
        `/ping` - Verifica latência do bot
        `/avatar` - Mostra avatar de um usuário
        """
        embed.add_field(name="🔧 Utilidades", value=util_commands, inline=False)
        
        # Emojis personalizados
        emoji_info = """
        O bot suporta emojis personalizados do servidor!
        Use `/emoji_list` para ver os emojis do servidor
        Configure emojis específicos nas mensagens de boas-vindas/despedida
        """
        embed.add_field(name="😄 Emojis Personalizados", value=emoji_info, inline=False)
        
        embed.set_footer(text="Use /ajuda para mais informações • Bot totalmente configurável via Discord")
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="serverinfo", description="Mostra informações do servidor")
    async def serverinfo(self, interaction: discord.Interaction):
        """Informações detalhadas do servidor"""
        guild = interaction.guild
        
        embed = discord.Embed(
            title=f"📊 {guild.name}",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        # Informações básicas
        embed.add_field(name="🆔 ID", value=guild.id, inline=True)
        embed.add_field(name="👑 Dono", value=guild.owner.mention if guild.owner else "Desconhecido", inline=True)
        embed.add_field(name="📅 Criado em", value=f"<t:{int(guild.created_at.timestamp())}:F>", inline=True)
        
        # Contadores
        embed.add_field(name="👥 Membros", value=guild.member_count, inline=True)
        embed.add_field(name="💬 Canais", value=len(guild.channels), inline=True)
        embed.add_field(name="🎭 Cargos", value=len(guild.roles), inline=True)
        
        # Emojis
        emoji_count = len(guild.emojis)
        emoji_static = len([e for e in guild.emojis if not e.animated])
        emoji_animated = len([e for e in guild.emojis if e.animated])
        embed.add_field(
            name="😄 Emojis",
            value=f"Total: {emoji_count}\nEstáticos: {emoji_static}\nAnimados: {emoji_animated}",
            inline=True
        )
        
        # Boost
        embed.add_field(name="🚀 Nível de Boost", value=guild.premium_tier, inline=True)
        embed.add_field(name="💎 Boosts", value=guild.premium_subscription_count, inline=True)
        
        # Verificação
        verification_level = {
            discord.VerificationLevel.none: "Nenhuma",
            discord.VerificationLevel.low: "Baixa",
            discord.VerificationLevel.medium: "Média",
            discord.VerificationLevel.high: "Alta",
            discord.VerificationLevel.highest: "Máxima"
        }
        embed.add_field(name="🔒 Verificação", value=verification_level.get(guild.verification_level, "Desconhecida"), inline=True)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="userinfo", description="Mostra informações de um usuário")
    @app_commands.describe(usuario="Usuário para ver informações (deixe vazio para ver suas próprias)")
    async def userinfo(self, interaction: discord.Interaction, usuario: discord.Member = None):
        """Informações detalhadas de um usuário"""
        user = usuario or interaction.user
        
        embed = discord.Embed(
            title=f"👤 {user.name}",
            color=user.color if user.color != discord.Color.default() else discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        
        embed.set_thumbnail(url=user.display_avatar.url)
        
        # Informações básicas
        embed.add_field(name="🆔 ID", value=user.id, inline=True)
        embed.add_field(name="📝 Nome", value=user.name, inline=True)
        embed.add_field(name="🏷️ Display Name", value=user.display_name, inline=True)
        
        # Datas
        embed.add_field(name="📅 Conta Criada", value=f"<t:{int(user.created_at.timestamp())}:F>", inline=False)
        embed.add_field(name="📥 Entrou em", value=f"<t:{int(user.joined_at.timestamp())}:F>", inline=False)
        
        # Cargos
        roles = [role.mention for role in user.roles if role.name != "@everyone"]
        if roles:
            embed.add_field(
                name=f"🎭 Cargos ({len(roles)})",
                value=" ".join(roles[:10]) + (f" e mais {len(roles) - 10}..." if len(roles) > 10 else ""),
                inline=False
            )
        
        # Status
        status_emoji = {
            discord.Status.online: "🟢 Online",
            discord.Status.idle: "🟡 Ausente",
            discord.Status.dnd: "🔴 Não Perturbe",
            discord.Status.offline: "⚫ Offline"
        }
        embed.add_field(name="📡 Status", value=status_emoji.get(user.status, "Desconhecido"), inline=True)
        
        # Bot?
        embed.add_field(name="🤖 Bot", value="Sim" if user.bot else "Não", inline=True)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="botinfo", description="Mostra informações do bot")
    async def botinfo(self, interaction: discord.Interaction):
        """Informações sobre o bot"""
        embed = discord.Embed(
            title="🤖 Informações do Bot",
            description="Bot de Discord totalmente configurável via comandos slash",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        
        # Estatísticas
        embed.add_field(name="📊 Servidores", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="👥 Usuários", value=sum(g.member_count for g in self.bot.guilds), inline=True)
        embed.add_field(name="💬 Comandos", value=len(self.bot.tree.get_commands()), inline=True)
        
        # Informações técnicas
        embed.add_field(name="🐍 Python", value=platform.python_version(), inline=True)
        embed.add_field(name="📚 Discord.py", value=discord.__version__, inline=True)
        embed.add_field(name="⏱️ Ping", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        
        # Recursos
        features = """
        ✅ Slash Commands
        ✅ Configuração via Discord
        ✅ Sistema de Moderação
        ✅ Boas-vindas Personalizadas
        ✅ Emojis Personalizados
        ✅ Sistema de Logs
        ✅ Cargos Automáticos
        """
        embed.add_field(name="🌟 Recursos", value=features, inline=False)
        
        embed.set_footer(text="Bot criado para ser 100% configurável via Discord")
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="ping", description="Verifica a latência do bot")
    async def ping(self, interaction: discord.Interaction):
        """Mostra a latência do bot"""
        latency = round(self.bot.latency * 1000)
        
        if latency < 100:
            emoji = "🟢"
            status = "Excelente"
        elif latency < 200:
            emoji = "🟡"
            status = "Bom"
        else:
            emoji = "🔴"
            status = "Alto"
        
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"{emoji} Latência: **{latency}ms** ({status})",
            color=discord.Color.green()
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="avatar", description="Mostra o avatar de um usuário")
    @app_commands.describe(usuario="Usuário para ver o avatar (deixe vazio para ver o seu)")
    async def avatar(self, interaction: discord.Interaction, usuario: discord.Member = None):
        """Mostra o avatar de um usuário em alta resolução"""
        user = usuario or interaction.user
        
        embed = discord.Embed(
            title=f"🖼️ Avatar de {user.name}",
            color=user.color if user.color != discord.Color.default() else discord.Color.blue()
        )
        
        embed.set_image(url=user.display_avatar.url)
        embed.add_field(name="🔗 Link", value=f"[Clique aqui]({user.display_avatar.url})")
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="emoji_list", description="Lista todos os emojis personalizados do servidor")
    async def emoji_list(self, interaction: discord.Interaction):
        """Lista os emojis personalizados do servidor"""
        guild = interaction.guild
        emojis = guild.emojis
        
        if not emojis:
            await interaction.response.send_message("❌ Este servidor não possui emojis personalizados!", ephemeral=True)
            return
        
        embed = discord.Embed(
            title=f"😄 Emojis de {guild.name}",
            description=f"Total: {len(emojis)} emojis",
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
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Utilidades(bot))
