"""
Cog de Boas-vindas e Despedidas - Gerencia eventos de membros
"""
import discord
from discord.ext import commands
import re

class BoasVindas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Evento quando um membro entra no servidor"""
        config = self.bot.get_guild_config(member.guild.id)
        
        # Verificar se módulo de boas-vindas está ativo
        if not config['enabled_modules'].get('welcome', True):
            return
        
        # Enviar mensagem de boas-vindas
        welcome_channel_id = config.get('welcome_channel')
        if welcome_channel_id:
            channel = member.guild.get_channel(welcome_channel_id)
            if channel:
                message = config.get('welcome_message', 'Bem-vindo(a) {user} ao servidor!')
                
                # Substituir placeholders
                message = message.replace('{user}', member.mention)
                message = message.replace('{username}', member.name)
                message = message.replace('{server}', member.guild.name)
                message = message.replace('{member_count}', str(member.guild.member_count))
                
                # Processar emojis personalizados
                message = self.process_custom_emojis(message, member.guild)
                
                try:
                    # Criar embed de boas-vindas
                    embed = discord.Embed(
                        title="🎉 Novo Membro!",
                        description=message,
                        color=discord.Color.green(),
                        timestamp=discord.utils.utcnow()
                    )
                    
                    embed.set_thumbnail(url=member.display_avatar.url)
                    embed.add_field(name="Membro", value=f"{member.name}#{member.discriminator}", inline=True)
                    embed.add_field(name="ID", value=member.id, inline=True)
                    embed.add_field(name="Conta Criada", value=f"<t:{int(member.created_at.timestamp())}:R>", inline=True)
                    embed.set_footer(text=f"Total de membros: {member.guild.member_count}")
                    
                    await channel.send(embed=embed)
                except Exception as e:
                    print(f"Erro ao enviar mensagem de boas-vindas: {e}")
        
        # Cargo automático
        if config['enabled_modules'].get('auto_role', False):
            auto_role_id = config.get('auto_role')
            if auto_role_id:
                role = member.guild.get_role(auto_role_id)
                if role:
                    try:
                        await member.add_roles(role, reason="Cargo automático")
                    except Exception as e:
                        print(f"Erro ao adicionar cargo automático: {e}")
    
    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        """Evento quando um membro sai do servidor"""
        config = self.bot.get_guild_config(member.guild.id)
        
        # Verificar se módulo de despedida está ativo
        if not config['enabled_modules'].get('goodbye', True):
            return
        
        # Enviar mensagem de despedida
        goodbye_channel_id = config.get('goodbye_channel')
        if goodbye_channel_id:
            channel = member.guild.get_channel(goodbye_channel_id)
            if channel:
                message = config.get('goodbye_message', 'Adeus {user}!')
                
                # Substituir placeholders (sem mention pois o membro já saiu)
                message = message.replace('{user}', member.name)
                message = message.replace('{username}', member.name)
                message = message.replace('{server}', member.guild.name)
                message = message.replace('{member_count}', str(member.guild.member_count))
                
                # Processar emojis personalizados
                message = self.process_custom_emojis(message, member.guild)
                
                try:
                    # Criar embed de despedida
                    embed = discord.Embed(
                        title="👋 Membro Saiu",
                        description=message,
                        color=discord.Color.red(),
                        timestamp=discord.utils.utcnow()
                    )
                    
                    embed.set_thumbnail(url=member.display_avatar.url)
                    embed.add_field(name="Membro", value=f"{member.name}#{member.discriminator}", inline=True)
                    embed.add_field(name="ID", value=member.id, inline=True)
                    embed.set_footer(text=f"Total de membros: {member.guild.member_count}")
                    
                    await channel.send(embed=embed)
                except Exception as e:
                    print(f"Erro ao enviar mensagem de despedida: {e}")
    
    def process_custom_emojis(self, text: str, guild: discord.Guild):
        """Processa tags de emojis personalizados no texto"""
        # Padrão: :emoji_name: ou <:emoji_name:id> ou <a:emoji_name:id>
        emoji_pattern = r':([a-zA-Z0-9_]+):'
        
        def replace_emoji(match):
            emoji_name = match.group(1)
            # Procurar emoji no servidor
            emoji = discord.utils.get(guild.emojis, name=emoji_name)
            if emoji:
                return str(emoji)
            return match.group(0)  # Retorna o original se não encontrar
        
        return re.sub(emoji_pattern, replace_emoji, text)
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        """Evento quando o bot entra em um servidor"""
        print(f"Bot adicionado ao servidor: {guild.name} (ID: {guild.id})")
        
        # Criar configuração padrão
        self.bot.get_guild_config(guild.id)
        
        # Tentar enviar mensagem de configuração para o dono ou canal do sistema
        try:
            # Tentar o canal do sistema primeiro
            if guild.system_channel:
                embed = discord.Embed(
                    title="👋 Obrigado por me adicionar!",
                    description="Sou um bot totalmente configurável via Discord!",
                    color=discord.Color.blue()
                )
                
                embed.add_field(
                    name="🚀 Como começar",
                    value="Use `/config ver` para ver as configurações atuais\nUse `/ajuda` para ver todos os comandos disponíveis",
                    inline=False
                )
                
                embed.add_field(
                    name="⚙️ Configuração Rápida",
                    value="1. `/config canal_boas_vindas` - Define onde enviar boas-vindas\n"
                          "2. `/config mensagem_boas_vindas` - Personaliza a mensagem\n"
                          "3. `/config cargo_automatico` - Define cargo para novos membros",
                    inline=False
                )
                
                embed.set_footer(text="Use /ajuda para ver todos os comandos")
                
                await guild.system_channel.send(embed=embed)
        except:
            pass

async def setup(bot):
    await bot.add_cog(BoasVindas(bot))
