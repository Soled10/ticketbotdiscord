"""
Cog de Configuração - Gerencia todas as configurações do bot via Discord
"""
import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional

class Configuracao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Grupo de comandos de configuração
    config_group = app_commands.Group(name="config", description="Comandos de configuração do bot")
    
    @config_group.command(name="canal_boas_vindas", description="Define o canal de boas-vindas")
    @app_commands.describe(canal="Canal onde as mensagens de boas-vindas serão enviadas")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_welcome_channel(self, interaction: discord.Interaction, canal: discord.TextChannel):
        """Define o canal de boas-vindas"""
        self.bot.update_guild_config(interaction.guild_id, "welcome_channel", canal.id)
        
        emoji = "✅"
        await interaction.response.send_message(
            f"{emoji} Canal de boas-vindas configurado para {canal.mention}",
            ephemeral=True
        )
    
    @config_group.command(name="canal_despedida", description="Define o canal de despedida")
    @app_commands.describe(canal="Canal onde as mensagens de despedida serão enviadas")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_goodbye_channel(self, interaction: discord.Interaction, canal: discord.TextChannel):
        """Define o canal de despedida"""
        self.bot.update_guild_config(interaction.guild_id, "goodbye_channel", canal.id)
        
        emoji = "✅"
        await interaction.response.send_message(
            f"{emoji} Canal de despedida configurado para {canal.mention}",
            ephemeral=True
        )
    
    @config_group.command(name="canal_logs", description="Define o canal de logs")
    @app_commands.describe(canal="Canal onde os logs serão enviados")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_log_channel(self, interaction: discord.Interaction, canal: discord.TextChannel):
        """Define o canal de logs"""
        self.bot.update_guild_config(interaction.guild_id, "log_channel", canal.id)
        
        emoji = "✅"
        await interaction.response.send_message(
            f"{emoji} Canal de logs configurado para {canal.mention}",
            ephemeral=True
        )
    
    @config_group.command(name="cargo_moderador", description="Define o cargo de moderador")
    @app_commands.describe(cargo="Cargo que terá permissões de moderação")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_mod_role(self, interaction: discord.Interaction, cargo: discord.Role):
        """Define o cargo de moderador"""
        self.bot.update_guild_config(interaction.guild_id, "mod_role", cargo.id)
        
        emoji = "✅"
        await interaction.response.send_message(
            f"{emoji} Cargo de moderador configurado para {cargo.mention}",
            ephemeral=True
        )
    
    @config_group.command(name="cargo_automatico", description="Define cargo automático para novos membros")
    @app_commands.describe(cargo="Cargo que será dado automaticamente aos novos membros")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_auto_role(self, interaction: discord.Interaction, cargo: discord.Role):
        """Define cargo automático"""
        self.bot.update_guild_config(interaction.guild_id, "auto_role", cargo.id)
        config = self.bot.get_guild_config(interaction.guild_id)
        config["enabled_modules"]["auto_role"] = True
        self.bot.save_configs()
        
        emoji = "✅"
        await interaction.response.send_message(
            f"{emoji} Cargo automático configurado para {cargo.mention}",
            ephemeral=True
        )
    
    @config_group.command(name="mensagem_boas_vindas", description="Define mensagem de boas-vindas")
    @app_commands.describe(mensagem="Mensagem personalizada ({user} = menção, {username} = nome, {server} = servidor)")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_welcome_message(self, interaction: discord.Interaction, mensagem: str):
        """Define mensagem personalizada de boas-vindas"""
        self.bot.update_guild_config(interaction.guild_id, "welcome_message", mensagem)
        
        emoji = "✅"
        await interaction.response.send_message(
            f"{emoji} Mensagem de boas-vindas atualizada!\n\n**Preview:**\n{mensagem.format(user=interaction.user.mention, username=interaction.user.name, server=interaction.guild.name)}",
            ephemeral=True
        )
    
    @config_group.command(name="mensagem_despedida", description="Define mensagem de despedida")
    @app_commands.describe(mensagem="Mensagem personalizada ({user} = nome, {server} = servidor)")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_goodbye_message(self, interaction: discord.Interaction, mensagem: str):
        """Define mensagem personalizada de despedida"""
        self.bot.update_guild_config(interaction.guild_id, "goodbye_message", mensagem)
        
        emoji = "✅"
        await interaction.response.send_message(
            f"{emoji} Mensagem de despedida atualizada!\n\n**Preview:**\n{mensagem.format(user=interaction.user.name, server=interaction.guild.name)}",
            ephemeral=True
        )
    
    @config_group.command(name="modulo", description="Ativa/desativa módulos do bot")
    @app_commands.describe(
        modulo="Módulo a ser configurado",
        ativo="Ativar ou desativar"
    )
    @app_commands.choices(modulo=[
        app_commands.Choice(name="Boas-vindas", value="welcome"),
        app_commands.Choice(name="Despedida", value="goodbye"),
        app_commands.Choice(name="Moderação", value="moderation"),
        app_commands.Choice(name="Cargo Automático", value="auto_role")
    ])
    @app_commands.checks.has_permissions(administrator=True)
    async def toggle_module(self, interaction: discord.Interaction, modulo: str, ativo: bool):
        """Ativa ou desativa módulos do bot"""
        config = self.bot.get_guild_config(interaction.guild_id)
        config["enabled_modules"][modulo] = ativo
        self.bot.save_configs()
        
        status = "ativado" if ativo else "desativado"
        emoji = "✅" if ativo else "❌"
        
        await interaction.response.send_message(
            f"{emoji} Módulo **{modulo}** {status}!",
            ephemeral=True
        )
    
    @config_group.command(name="ver", description="Ver todas as configurações atuais")
    @app_commands.checks.has_permissions(administrator=True)
    async def view_config(self, interaction: discord.Interaction):
        """Mostra todas as configurações do servidor"""
        config = self.bot.get_guild_config(interaction.guild_id)
        
        embed = discord.Embed(
            title="⚙️ Configurações do Servidor",
            color=discord.Color.blue(),
            timestamp=discord.utils.utcnow()
        )
        
        # Canais
        welcome_ch = f"<#{config['welcome_channel']}>" if config['welcome_channel'] else "Não configurado"
        goodbye_ch = f"<#{config['goodbye_channel']}>" if config['goodbye_channel'] else "Não configurado"
        log_ch = f"<#{config['log_channel']}>" if config['log_channel'] else "Não configurado"
        
        embed.add_field(
            name="📢 Canais",
            value=f"**Boas-vindas:** {welcome_ch}\n**Despedida:** {goodbye_ch}\n**Logs:** {log_ch}",
            inline=False
        )
        
        # Cargos
        mod_role = f"<@&{config['mod_role']}>" if config['mod_role'] else "Não configurado"
        auto_role = f"<@&{config['auto_role']}>" if config['auto_role'] else "Não configurado"
        
        embed.add_field(
            name="👥 Cargos",
            value=f"**Moderador:** {mod_role}\n**Automático:** {auto_role}",
            inline=False
        )
        
        # Módulos
        modules = config['enabled_modules']
        module_status = "\n".join([
            f"**{name.title()}:** {'✅ Ativo' if status else '❌ Inativo'}"
            for name, status in modules.items()
        ])
        
        embed.add_field(
            name="🔧 Módulos",
            value=module_status,
            inline=False
        )
        
        # Mensagens
        embed.add_field(
            name="💬 Mensagens",
            value=f"**Boas-vindas:** {config['welcome_message'][:100]}...\n**Despedida:** {config['goodbye_message'][:100]}...",
            inline=False
        )
        
        embed.set_footer(text=f"Servidor: {interaction.guild.name}")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @config_group.command(name="resetar", description="Reseta todas as configurações para o padrão")
    @app_commands.checks.has_permissions(administrator=True)
    async def reset_config(self, interaction: discord.Interaction):
        """Reseta as configurações do servidor"""
        # Criar view com botões de confirmação
        view = discord.ui.View(timeout=30)
        
        async def confirm_callback(button_interaction: discord.Interaction):
            if button_interaction.user.id != interaction.user.id:
                await button_interaction.response.send_message("❌ Apenas quem iniciou pode confirmar!", ephemeral=True)
                return
            
            # Deletar configuração
            guild_id_str = str(interaction.guild_id)
            if guild_id_str in self.bot.guild_configs:
                del self.bot.guild_configs[guild_id_str]
                self.bot.save_configs()
            
            await button_interaction.response.edit_message(
                content="✅ Configurações resetadas com sucesso!",
                view=None
            )
        
        async def cancel_callback(button_interaction: discord.Interaction):
            if button_interaction.user.id != interaction.user.id:
                await button_interaction.response.send_message("❌ Apenas quem iniciou pode cancelar!", ephemeral=True)
                return
            
            await button_interaction.response.edit_message(
                content="❌ Reset cancelado.",
                view=None
            )
        
        confirm_button = discord.ui.Button(label="Confirmar", style=discord.ButtonStyle.danger)
        cancel_button = discord.ui.Button(label="Cancelar", style=discord.ButtonStyle.secondary)
        
        confirm_button.callback = confirm_callback
        cancel_button.callback = cancel_callback
        
        view.add_item(confirm_button)
        view.add_item(cancel_button)
        
        await interaction.response.send_message(
            "⚠️ **ATENÇÃO:** Isso irá resetar TODAS as configurações deste servidor para o padrão. Deseja continuar?",
            view=view,
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Configuracao(bot))
