"""
Cog de Moderação - Comandos de moderação e gerenciamento
"""
import discord
from discord import app_commands
from discord.ext import commands
from datetime import timedelta
import asyncio

class Moderacao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def is_moderator(self, member: discord.Member, guild_id: int):
        """Verifica se o membro é moderador"""
        if member.guild_permissions.administrator:
            return True
        
        config = self.bot.get_guild_config(guild_id)
        mod_role_id = config.get('mod_role')
        
        if mod_role_id:
            return any(role.id == mod_role_id for role in member.roles)
        return False
    
    @app_commands.command(name="kick", description="Expulsa um membro do servidor")
    @app_commands.describe(
        membro="Membro a ser expulso",
        motivo="Motivo da expulsão"
    )
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, membro: discord.Member, motivo: str = "Sem motivo especificado"):
        """Expulsa um membro"""
        if membro.top_role >= interaction.user.top_role:
            await interaction.response.send_message("❌ Você não pode expulsar alguém com cargo igual ou superior ao seu!", ephemeral=True)
            return
        
        if membro.id == interaction.guild.owner_id:
            await interaction.response.send_message("❌ Você não pode expulsar o dono do servidor!", ephemeral=True)
            return
        
        try:
            # Tentar enviar DM para o membro
            try:
                embed = discord.Embed(
                    title="🚪 Você foi expulso!",
                    description=f"Você foi expulso do servidor **{interaction.guild.name}**",
                    color=discord.Color.orange()
                )
                embed.add_field(name="Motivo", value=motivo)
                embed.add_field(name="Moderador", value=interaction.user.mention)
                await membro.send(embed=embed)
            except:
                pass
            
            await membro.kick(reason=f"{interaction.user}: {motivo}")
            
            # Log
            await self.log_action(
                interaction.guild_id,
                "Kick",
                interaction.user,
                membro,
                motivo
            )
            
            embed = discord.Embed(
                title="✅ Membro Expulso",
                description=f"{membro.mention} foi expulso do servidor",
                color=discord.Color.green()
            )
            embed.add_field(name="Motivo", value=motivo)
            embed.add_field(name="Moderador", value=interaction.user.mention)
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao expulsar: {e}", ephemeral=True)
    
    @app_commands.command(name="ban", description="Bane um membro do servidor")
    @app_commands.describe(
        membro="Membro a ser banido",
        motivo="Motivo do banimento",
        deletar_mensagens="Deletar mensagens dos últimos dias (0-7)"
    )
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, membro: discord.Member, motivo: str = "Sem motivo especificado", deletar_mensagens: int = 0):
        """Bane um membro"""
        if membro.top_role >= interaction.user.top_role:
            await interaction.response.send_message("❌ Você não pode banir alguém com cargo igual ou superior ao seu!", ephemeral=True)
            return
        
        if membro.id == interaction.guild.owner_id:
            await interaction.response.send_message("❌ Você não pode banir o dono do servidor!", ephemeral=True)
            return
        
        deletar_mensagens = max(0, min(7, deletar_mensagens))
        
        try:
            # Tentar enviar DM para o membro
            try:
                embed = discord.Embed(
                    title="🔨 Você foi banido!",
                    description=f"Você foi banido do servidor **{interaction.guild.name}**",
                    color=discord.Color.red()
                )
                embed.add_field(name="Motivo", value=motivo)
                embed.add_field(name="Moderador", value=interaction.user.mention)
                await membro.send(embed=embed)
            except:
                pass
            
            await membro.ban(reason=f"{interaction.user}: {motivo}", delete_message_days=deletar_mensagens)
            
            # Log
            await self.log_action(
                interaction.guild_id,
                "Ban",
                interaction.user,
                membro,
                motivo
            )
            
            embed = discord.Embed(
                title="✅ Membro Banido",
                description=f"{membro.mention} foi banido do servidor",
                color=discord.Color.green()
            )
            embed.add_field(name="Motivo", value=motivo)
            embed.add_field(name="Moderador", value=interaction.user.mention)
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao banir: {e}", ephemeral=True)
    
    @app_commands.command(name="unban", description="Remove o banimento de um usuário")
    @app_commands.describe(
        user_id="ID do usuário a ser desbanido",
        motivo="Motivo do desbanimento"
    )
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, user_id: str, motivo: str = "Sem motivo especificado"):
        """Remove o ban de um usuário"""
        try:
            user_id_int = int(user_id)
            user = await self.bot.fetch_user(user_id_int)
            
            await interaction.guild.unban(user, reason=f"{interaction.user}: {motivo}")
            
            embed = discord.Embed(
                title="✅ Usuário Desbanido",
                description=f"{user.mention} foi desbanido do servidor",
                color=discord.Color.green()
            )
            embed.add_field(name="Motivo", value=motivo)
            embed.add_field(name="Moderador", value=interaction.user.mention)
            
            await interaction.response.send_message(embed=embed)
            
        except ValueError:
            await interaction.response.send_message("❌ ID de usuário inválido!", ephemeral=True)
        except discord.NotFound:
            await interaction.response.send_message("❌ Usuário não encontrado ou não está banido!", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao desbanir: {e}", ephemeral=True)
    
    @app_commands.command(name="timeout", description="Coloca um membro em timeout")
    @app_commands.describe(
        membro="Membro a receber timeout",
        duracao="Duração em minutos",
        motivo="Motivo do timeout"
    )
    @app_commands.checks.has_permissions(moderate_members=True)
    async def timeout(self, interaction: discord.Interaction, membro: discord.Member, duracao: int, motivo: str = "Sem motivo especificado"):
        """Coloca um membro em timeout"""
        if membro.top_role >= interaction.user.top_role:
            await interaction.response.send_message("❌ Você não pode dar timeout em alguém com cargo igual ou superior ao seu!", ephemeral=True)
            return
        
        if membro.id == interaction.guild.owner_id:
            await interaction.response.send_message("❌ Você não pode dar timeout no dono do servidor!", ephemeral=True)
            return
        
        if duracao < 1 or duracao > 40320:  # Max 28 dias
            await interaction.response.send_message("❌ Duração deve ser entre 1 minuto e 28 dias (40320 minutos)!", ephemeral=True)
            return
        
        try:
            timeout_until = discord.utils.utcnow() + timedelta(minutes=duracao)
            await membro.timeout(timeout_until, reason=f"{interaction.user}: {motivo}")
            
            # Log
            await self.log_action(
                interaction.guild_id,
                "Timeout",
                interaction.user,
                membro,
                f"{motivo} (Duração: {duracao} minutos)"
            )
            
            embed = discord.Embed(
                title="🔇 Membro em Timeout",
                description=f"{membro.mention} está em timeout",
                color=discord.Color.orange()
            )
            embed.add_field(name="Duração", value=f"{duracao} minutos")
            embed.add_field(name="Motivo", value=motivo)
            embed.add_field(name="Moderador", value=interaction.user.mention)
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao aplicar timeout: {e}", ephemeral=True)
    
    @app_commands.command(name="limpar", description="Limpa mensagens do canal")
    @app_commands.describe(quantidade="Quantidade de mensagens a deletar (1-100)")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, quantidade: int):
        """Limpa mensagens do canal"""
        if quantidade < 1 or quantidade > 100:
            await interaction.response.send_message("❌ Quantidade deve ser entre 1 e 100!", ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)
        
        try:
            deleted = await interaction.channel.purge(limit=quantidade)
            await interaction.followup.send(f"✅ {len(deleted)} mensagens deletadas!", ephemeral=True)
            
            # Log
            await self.log_action(
                interaction.guild_id,
                "Limpeza de Mensagens",
                interaction.user,
                None,
                f"{len(deleted)} mensagens deletadas em {interaction.channel.mention}"
            )
            
        except Exception as e:
            await interaction.followup.send(f"❌ Erro ao limpar mensagens: {e}", ephemeral=True)
    
    async def log_action(self, guild_id: int, action: str, moderator: discord.User, target: discord.Member = None, reason: str = ""):
        """Registra ações de moderação no canal de logs"""
        config = self.bot.get_guild_config(guild_id)
        log_channel_id = config.get('log_channel')
        
        if not log_channel_id:
            return
        
        try:
            channel = self.bot.get_channel(log_channel_id)
            if not channel:
                return
            
            embed = discord.Embed(
                title=f"📋 {action}",
                color=discord.Color.blue(),
                timestamp=discord.utils.utcnow()
            )
            
            embed.add_field(name="Moderador", value=moderator.mention, inline=True)
            if target:
                embed.add_field(name="Alvo", value=target.mention, inline=True)
            if reason:
                embed.add_field(name="Motivo/Detalhes", value=reason, inline=False)
            
            embed.set_footer(text=f"ID do Moderador: {moderator.id}")
            
            await channel.send(embed=embed)
        except:
            pass

async def setup(bot):
    await bot.add_cog(Moderacao(bot))
