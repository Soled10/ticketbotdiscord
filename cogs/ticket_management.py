"""
Cog de Gerenciamento de Tickets - Comandos para gerenciar tickets abertos
"""
import discord
from discord import app_commands
from discord.ext import commands
import asyncio
from datetime import datetime
import io

class TicketManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def is_ticket_channel(self, channel_id: int, guild_id: int) -> bool:
        """Verifica se o canal é um ticket"""
        tickets_data = self.bot.get_tickets_data(guild_id)
        return str(channel_id) in tickets_data.get('active_tickets', {})
    
    def can_manage_ticket(self, member: discord.Member, guild_id: int) -> bool:
        """Verifica se o membro pode gerenciar tickets"""
        if member.guild_permissions.administrator:
            return True
        
        config = self.bot.get_guild_config(guild_id)
        support_role_id = config.get('support_role')
        
        if support_role_id:
            return any(role.id == support_role_id for role in member.roles)
        return False
    
    @app_commands.command(name="fechar", description="Fecha o ticket atual")
    @app_commands.describe(motivo="Motivo do fechamento")
    async def close(self, interaction: discord.Interaction, motivo: str = "Sem motivo especificado"):
        """Fecha o ticket"""
        if not self.is_ticket_channel(interaction.channel_id, interaction.guild_id):
            await interaction.response.send_message("❌ Este não é um canal de ticket!", ephemeral=True)
            return
        
        tickets_data = self.bot.get_tickets_data(interaction.guild_id)
        ticket_info = tickets_data['active_tickets'].get(str(interaction.channel_id))
        
        # Verificar permissões
        if not self.can_manage_ticket(interaction.user, interaction.guild_id):
            if interaction.user.id != ticket_info['user_id']:
                await interaction.response.send_message(
                    "❌ Apenas o criador do ticket ou a equipe de suporte pode fechá-lo!",
                    ephemeral=True
                )
                return
        
        await self.close_ticket(interaction, motivo)
    
    async def close_ticket_interaction(self, interaction: discord.Interaction):
        """Fecha ticket via botão"""
        await self.close_ticket(interaction, "Fechado via botão")
    
    async def close_ticket(self, interaction: discord.Interaction, motivo: str):
        """Lógica de fechamento de ticket"""
        config = self.bot.get_guild_config(interaction.guild_id)
        tickets_data = self.bot.get_tickets_data(interaction.guild_id)
        
        ticket_info = tickets_data['active_tickets'].get(str(interaction.channel_id))
        if not ticket_info:
            await interaction.response.send_message("❌ Ticket não encontrado!", ephemeral=True)
            return
        
        await interaction.response.defer()
        
        # Gerar transcrição se ativado
        transcript_file = None
        if config.get('transcript_enabled', True):
            transcript_file = await self.generate_transcript(interaction.channel)
        
        # Mensagem de fechamento
        close_msg = config.get('close_message', 'Ticket fechado por {user}.')
        close_msg = close_msg.replace('{user}', interaction.user.mention)
        
        embed = discord.Embed(
            title="🔒 Ticket Fechado",
            description=close_msg,
            color=discord.Color.red(),
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(name="📝 Motivo", value=motivo, inline=False)
        embed.add_field(name="👤 Fechado por", value=interaction.user.mention, inline=True)
        
        if config.get('auto_delete_closed', False):
            delete_time = config.get('delete_after_minutes', 5)
            embed.add_field(
                name="⏰ Auto-deleção",
                value=f"Este canal será deletado em {delete_time} minutos",
                inline=True
            )
        
        await interaction.channel.send(embed=embed)
        
        # Atualizar dados
        ticket_info['closed'] = True
        ticket_info['closed_by'] = interaction.user.id
        ticket_info['closed_at'] = datetime.utcnow().isoformat()
        ticket_info['close_reason'] = motivo
        
        # Mover para tickets fechados
        tickets_data['closed_tickets'].append(ticket_info)
        del tickets_data['active_tickets'][str(interaction.channel_id)]
        
        # Remover da lista de tickets do usuário
        user_id_str = str(ticket_info['user_id'])
        if user_id_str in tickets_data['user_tickets']:
            if interaction.channel_id in tickets_data['user_tickets'][user_id_str]:
                tickets_data['user_tickets'][user_id_str].remove(interaction.channel_id)
        
        self.bot.save_tickets_data()
        
        # Enviar log com transcrição
        log_channel_id = config.get('ticket_logs')
        if log_channel_id:
            log_channel = self.bot.get_channel(log_channel_id)
            if log_channel:
                log_embed = discord.Embed(
                    title="🔒 Ticket Fechado",
                    color=discord.Color.red(),
                    timestamp=datetime.utcnow()
                )
                
                log_embed.add_field(name="🆔 Ticket", value=f"#{ticket_info['id']:04d}", inline=True)
                log_embed.add_field(name="📝 Categoria", value=ticket_info['category'], inline=True)
                log_embed.add_field(name="👤 Criador", value=f"<@{ticket_info['user_id']}>", inline=True)
                log_embed.add_field(name="🔒 Fechado por", value=interaction.user.mention, inline=True)
                log_embed.add_field(name="📝 Motivo", value=motivo, inline=False)
                
                if transcript_file:
                    await log_channel.send(embed=log_embed, file=transcript_file)
                else:
                    await log_channel.send(embed=log_embed)
        
        await interaction.followup.send("✅ Ticket fechado com sucesso!")
        
        # Remover permissões do usuário
        try:
            user = interaction.guild.get_member(ticket_info['user_id'])
            if user:
                await interaction.channel.set_permissions(user, read_messages=False)
        except:
            pass
        
        # Auto-deletar se ativado
        if config.get('auto_delete_closed', False):
            delete_time = config.get('delete_after_minutes', 5) * 60
            await asyncio.sleep(delete_time)
            try:
                await interaction.channel.delete(reason="Ticket fechado - Auto-deleção")
            except:
                pass
    
    @app_commands.command(name="adicionar", description="Adiciona um usuário ao ticket")
    @app_commands.describe(usuario="Usuário a ser adicionado")
    async def add_user(self, interaction: discord.Interaction, usuario: discord.Member):
        """Adiciona um usuário ao ticket"""
        if not self.is_ticket_channel(interaction.channel_id, interaction.guild_id):
            await interaction.response.send_message("❌ Este não é um canal de ticket!", ephemeral=True)
            return
        
        if not self.can_manage_ticket(interaction.user, interaction.guild_id):
            tickets_data = self.bot.get_tickets_data(interaction.guild_id)
            ticket_info = tickets_data['active_tickets'].get(str(interaction.channel_id))
            if interaction.user.id != ticket_info['user_id']:
                await interaction.response.send_message(
                    "❌ Apenas o criador do ticket ou a equipe pode adicionar usuários!",
                    ephemeral=True
                )
                return
        
        try:
            await interaction.channel.set_permissions(
                usuario,
                read_messages=True,
                send_messages=True,
                attach_files=True,
                embed_links=True
            )
            
            embed = discord.Embed(
                description=f"✅ {usuario.mention} foi adicionado ao ticket por {interaction.user.mention}",
                color=discord.Color.green()
            )
            
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao adicionar usuário: {e}", ephemeral=True)
    
    @app_commands.command(name="remover", description="Remove um usuário do ticket")
    @app_commands.describe(usuario="Usuário a ser removido")
    async def remove_user(self, interaction: discord.Interaction, usuario: discord.Member):
        """Remove um usuário do ticket"""
        if not self.is_ticket_channel(interaction.channel_id, interaction.guild_id):
            await interaction.response.send_message("❌ Este não é um canal de ticket!", ephemeral=True)
            return
        
        if not self.can_manage_ticket(interaction.user, interaction.guild_id):
            tickets_data = self.bot.get_tickets_data(interaction.guild_id)
            ticket_info = tickets_data['active_tickets'].get(str(interaction.channel_id))
            if interaction.user.id != ticket_info['user_id']:
                await interaction.response.send_message(
                    "❌ Apenas o criador do ticket ou a equipe pode remover usuários!",
                    ephemeral=True
                )
                return
        
        tickets_data = self.bot.get_tickets_data(interaction.guild_id)
        ticket_info = tickets_data['active_tickets'].get(str(interaction.channel_id))
        
        if usuario.id == ticket_info['user_id']:
            await interaction.response.send_message("❌ Você não pode remover o criador do ticket!", ephemeral=True)
            return
        
        try:
            await interaction.channel.set_permissions(usuario, read_messages=False)
            
            embed = discord.Embed(
                description=f"✅ {usuario.mention} foi removido do ticket por {interaction.user.mention}",
                color=discord.Color.orange()
            )
            
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao remover usuário: {e}", ephemeral=True)
    
    async def claim_ticket_interaction(self, interaction: discord.Interaction):
        """Reivindica um ticket via botão"""
        if not self.can_manage_ticket(interaction.user, interaction.guild_id):
            await interaction.response.send_message(
                "❌ Apenas a equipe de suporte pode reivindicar tickets!",
                ephemeral=True
            )
            return
        
        tickets_data = self.bot.get_tickets_data(interaction.guild_id)
        ticket_info = tickets_data['active_tickets'].get(str(interaction.channel_id))
        
        if ticket_info['claimed_by']:
            claimed_user = interaction.guild.get_member(ticket_info['claimed_by'])
            await interaction.response.send_message(
                f"❌ Este ticket já foi reivindicado por {claimed_user.mention if claimed_user else 'alguém'}!",
                ephemeral=True
            )
            return
        
        ticket_info['claimed_by'] = interaction.user.id
        ticket_info['claimed_at'] = datetime.utcnow().isoformat()
        self.bot.save_tickets_data()
        
        embed = discord.Embed(
            description=f"✋ {interaction.user.mention} reivindicou este ticket!",
            color=discord.Color.blue()
        )
        
        await interaction.response.send_message(embed=embed)
    
    async def transcript_interaction(self, interaction: discord.Interaction):
        """Gera transcrição via botão"""
        await interaction.response.defer(ephemeral=True)
        
        transcript = await self.generate_transcript(interaction.channel)
        
        if transcript:
            await interaction.followup.send(
                "📄 Transcrição do ticket:",
                file=transcript,
                ephemeral=True
            )
        else:
            await interaction.followup.send("❌ Erro ao gerar transcrição!", ephemeral=True)
    
    async def generate_transcript(self, channel: discord.TextChannel):
        """Gera uma transcrição do ticket em formato HTML"""
        try:
            messages = []
            async for message in channel.history(limit=None, oldest_first=True):
                messages.append(message)
            
            html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Ticket #{channel.name}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #36393f;
            color: #dcddde;
            padding: 20px;
        }}
        .header {{
            background-color: #202225;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}
        .message {{
            background-color: #40444b;
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
            border-left: 4px solid #5865f2;
        }}
        .author {{
            color: #5865f2;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .timestamp {{
            color: #72767d;
            font-size: 0.8em;
        }}
        .content {{
            margin-top: 10px;
            line-height: 1.5;
        }}
        .embed {{
            background-color: #2f3136;
            border-left: 4px solid #5865f2;
            padding: 10px;
            margin-top: 10px;
            border-radius: 4px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Transcrição do Ticket: {channel.name}</h1>
        <p>Servidor: {channel.guild.name}</p>
        <p>Total de mensagens: {len(messages)}</p>
        <p>Gerado em: {datetime.utcnow().strftime('%d/%m/%Y %H:%M:%S')} UTC</p>
    </div>
"""
            
            for msg in messages:
                timestamp = msg.created_at.strftime('%d/%m/%Y %H:%M:%S')
                content = msg.content.replace('<', '&lt;').replace('>', '&gt;')
                
                html_content += f"""
    <div class="message">
        <div class="author">{msg.author.name}#{msg.author.discriminator}</div>
        <div class="timestamp">{timestamp}</div>
        <div class="content">{content}</div>
"""
                
                if msg.embeds:
                    for embed in msg.embeds:
                        html_content += f"""
        <div class="embed">
            <strong>{embed.title or ''}</strong>
            <p>{embed.description or ''}</p>
        </div>
"""
                
                if msg.attachments:
                    html_content += "<div><strong>Anexos:</strong><br>"
                    for att in msg.attachments:
                        html_content += f'<a href="{att.url}">{att.filename}</a><br>'
                    html_content += "</div>"
                
                html_content += "    </div>\n"
            
            html_content += """
</body>
</html>
"""
            
            # Criar arquivo
            file_name = f"transcript-{channel.name}-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}.html"
            file = discord.File(
                io.BytesIO(html_content.encode('utf-8')),
                filename=file_name
            )
            
            return file
        except Exception as e:
            print(f"Erro ao gerar transcrição: {e}")
            return None

async def setup(bot):
    await bot.add_cog(TicketManagement(bot))
