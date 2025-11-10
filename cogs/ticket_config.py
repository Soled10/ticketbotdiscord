"""
Cog de Configuração de Tickets - Gerencia todas as configurações do sistema de tickets
"""
import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional

class TicketConfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    config_group = app_commands.Group(name="ticket-config", description="Configurações do sistema de tickets")
    
    @config_group.command(name="categoria", description="Define a categoria onde os tickets serão criados")
    @app_commands.describe(categoria="Categoria para criar canais de tickets")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_category(self, interaction: discord.Interaction, categoria: discord.CategoryChannel):
        """Define a categoria dos tickets"""
        self.bot.update_guild_config(interaction.guild_id, "ticket_category", categoria.id)
        await interaction.response.send_message(
            f"✅ Categoria de tickets configurada para: **{categoria.name}**",
            ephemeral=True
        )
    
    @config_group.command(name="logs", description="Define o canal de logs de tickets")
    @app_commands.describe(canal="Canal onde os logs serão enviados")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_logs(self, interaction: discord.Interaction, canal: discord.TextChannel):
        """Define o canal de logs"""
        self.bot.update_guild_config(interaction.guild_id, "ticket_logs", canal.id)
        await interaction.response.send_message(
            f"✅ Canal de logs configurado para: {canal.mention}",
            ephemeral=True
        )
    
    @config_group.command(name="cargo-suporte", description="Define o cargo da equipe de suporte")
    @app_commands.describe(cargo="Cargo que terá acesso aos tickets")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_support_role(self, interaction: discord.Interaction, cargo: discord.Role):
        """Define o cargo de suporte"""
        self.bot.update_guild_config(interaction.guild_id, "support_role", cargo.id)
        await interaction.response.send_message(
            f"✅ Cargo de suporte configurado para: {cargo.mention}",
            ephemeral=True
        )
    
    @config_group.command(name="mensagem-abertura", description="Define mensagem ao abrir ticket")
    @app_commands.describe(mensagem="Mensagem personalizada ({user} = menção, {username} = nome)")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_open_message(self, interaction: discord.Interaction, mensagem: str):
        """Define mensagem de abertura"""
        self.bot.update_guild_config(interaction.guild_id, "ticket_message", mensagem)
        
        preview = mensagem.replace("{user}", interaction.user.mention).replace("{username}", interaction.user.name)
        await interaction.response.send_message(
            f"✅ Mensagem de abertura atualizada!\n\n**Preview:**\n{preview}",
            ephemeral=True
        )
    
    @config_group.command(name="mensagem-fechamento", description="Define mensagem ao fechar ticket")
    @app_commands.describe(mensagem="Mensagem personalizada ({user} = quem fechou)")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_close_message(self, interaction: discord.Interaction, mensagem: str):
        """Define mensagem de fechamento"""
        self.bot.update_guild_config(interaction.guild_id, "close_message", mensagem)
        
        preview = mensagem.replace("{user}", interaction.user.mention)
        await interaction.response.send_message(
            f"✅ Mensagem de fechamento atualizada!\n\n**Preview:**\n{preview}",
            ephemeral=True
        )
    
    @config_group.command(name="limite-tickets", description="Define quantos tickets um usuário pode ter abertos")
    @app_commands.describe(limite="Número máximo de tickets por usuário (1-10)")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_ticket_limit(self, interaction: discord.Interaction, limite: int):
        """Define limite de tickets por usuário"""
        if limite < 1 or limite > 10:
            await interaction.response.send_message("❌ O limite deve ser entre 1 e 10!", ephemeral=True)
            return
        
        self.bot.update_guild_config(interaction.guild_id, "max_tickets_per_user", limite)
        await interaction.response.send_message(
            f"✅ Limite de tickets por usuário definido para: **{limite}**",
            ephemeral=True
        )
    
    @config_group.command(name="auto-deletar", description="Deletar automaticamente tickets fechados")
    @app_commands.describe(
        ativar="Ativar ou desativar deleção automática",
        minutos="Minutos para deletar após fechar (1-60)"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def set_auto_delete(self, interaction: discord.Interaction, ativar: bool, minutos: int = 5):
        """Configura deleção automática de tickets"""
        if minutos < 1 or minutos > 60:
            await interaction.response.send_message("❌ O tempo deve ser entre 1 e 60 minutos!", ephemeral=True)
            return
        
        config = self.bot.get_guild_config(interaction.guild_id)
        config["auto_delete_closed"] = ativar
        config["delete_after_minutes"] = minutos
        self.bot.save_configs()
        
        status = f"ativada (deletar após {minutos} minutos)" if ativar else "desativada"
        await interaction.response.send_message(
            f"✅ Deleção automática de tickets: **{status}**",
            ephemeral=True
        )
    
    @config_group.command(name="transcrição", description="Ativar/desativar transcrições de tickets")
    @app_commands.describe(ativar="Ativar ou desativar transcrições")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_transcript(self, interaction: discord.Interaction, ativar: bool):
        """Ativa/desativa transcrições"""
        self.bot.update_guild_config(interaction.guild_id, "transcript_enabled", ativar)
        
        status = "ativadas" if ativar else "desativadas"
        await interaction.response.send_message(
            f"✅ Transcrições de tickets: **{status}**",
            ephemeral=True
        )
    
    @config_group.command(name="categoria-ticket", description="Configura uma categoria de ticket")
    @app_commands.describe(
        id_categoria="ID único (ex: suporte, vendas, bug)",
        nome="Nome da categoria",
        emoji="Emoji para a categoria",
        descricao="Descrição da categoria",
        ativar="Ativar ou desativar esta categoria"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def set_ticket_category(
        self, 
        interaction: discord.Interaction, 
        id_categoria: str,
        nome: str,
        emoji: str,
        descricao: str,
        ativar: bool = True
    ):
        """Configura uma categoria de ticket personalizada"""
        # Validar ID (apenas letras, números e _)
        if not id_categoria.replace("_", "").replace("-", "").isalnum():
            await interaction.response.send_message(
                "❌ O ID deve conter apenas letras, números, _ ou -",
                ephemeral=True
            )
            return
        
        config = self.bot.get_guild_config(interaction.guild_id)
        
        config["ticket_categories"][id_categoria] = {
            "name": nome,
            "emoji": emoji,
            "description": descricao,
            "enabled": ativar
        }
        
        self.bot.save_configs()
        
        await interaction.response.send_message(
            f"✅ Categoria de ticket configurada!\n\n"
            f"**ID:** {id_categoria}\n"
            f"**Nome:** {emoji} {nome}\n"
            f"**Descrição:** {descricao}\n"
            f"**Status:** {'✅ Ativa' if ativar else '❌ Desativada'}",
            ephemeral=True
        )
    
    @config_group.command(name="remover-categoria", description="Remove uma categoria de ticket")
    @app_commands.describe(id_categoria="ID da categoria a remover")
    @app_commands.checks.has_permissions(administrator=True)
    async def remove_ticket_category(self, interaction: discord.Interaction, id_categoria: str):
        """Remove uma categoria de ticket"""
        config = self.bot.get_guild_config(interaction.guild_id)
        
        if id_categoria not in config["ticket_categories"]:
            await interaction.response.send_message(
                f"❌ Categoria **{id_categoria}** não encontrada!",
                ephemeral=True
            )
            return
        
        cat_info = config["ticket_categories"][id_categoria]
        del config["ticket_categories"][id_categoria]
        self.bot.save_configs()
        
        await interaction.response.send_message(
            f"✅ Categoria **{cat_info['emoji']} {cat_info['name']}** removida!",
            ephemeral=True
        )
    
    @config_group.command(name="ver", description="Ver todas as configurações")
    @app_commands.checks.has_permissions(administrator=True)
    async def view_config(self, interaction: discord.Interaction):
        """Mostra todas as configurações"""
        config = self.bot.get_guild_config(interaction.guild_id)
        
        embed = discord.Embed(
            title="⚙️ Configurações do Sistema de Tickets",
            color=discord.Color.blue(),
            timestamp=discord.utils.utcnow()
        )
        
        # Configurações básicas
        category = f"<#{config['ticket_category']}>" if config['ticket_category'] else "Não configurado"
        logs = f"<#{config['ticket_logs']}>" if config['ticket_logs'] else "Não configurado"
        support = f"<@&{config['support_role']}>" if config['support_role'] else "Não configurado"
        
        embed.add_field(
            name="📋 Configurações Básicas",
            value=f"**Categoria:** {category}\n"
                  f"**Logs:** {logs}\n"
                  f"**Cargo Suporte:** {support}\n"
                  f"**Limite por usuário:** {config['max_tickets_per_user']}",
            inline=False
        )
        
        # Automação
        auto_delete = "✅ Ativo" if config['auto_delete_closed'] else "❌ Inativo"
        transcript = "✅ Ativo" if config['transcript_enabled'] else "❌ Inativo"
        
        embed.add_field(
            name="🤖 Automação",
            value=f"**Auto-deletar:** {auto_delete}\n"
                  f"**Tempo para deletar:** {config['delete_after_minutes']} minutos\n"
                  f"**Transcrições:** {transcript}",
            inline=False
        )
        
        # Categorias de ticket
        categories = config['ticket_categories']
        cat_list = []
        for cat_id, cat_data in categories.items():
            status = "✅" if cat_data['enabled'] else "❌"
            cat_list.append(f"{status} {cat_data['emoji']} **{cat_data['name']}** (`{cat_id}`)")
        
        embed.add_field(
            name="🎫 Categorias de Ticket",
            value="\n".join(cat_list) if cat_list else "Nenhuma categoria configurada",
            inline=False
        )
        
        embed.set_footer(text=f"Total de tickets criados: {config['ticket_counter']}")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(TicketConfig(bot))
