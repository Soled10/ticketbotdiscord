"""
Cog de Estatísticas - Sistema avançado de métricas e análises
"""
import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timedelta
import json
from collections import defaultdict

class Statistics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def update_ticket_stats(self, guild_id: int, category: str, staff_id: int = None):
        """Atualiza estatísticas quando um ticket é criado/fechado"""
        stats = self.bot.get_statistics(guild_id)
        
        stats['total_tickets'] += 1
        
        # Incrementar contagem por categoria
        if category not in stats['tickets_by_category']:
            stats['tickets_by_category'][category] = 0
        stats['tickets_by_category'][category] += 1
        
        # Atualizar horário mais movimentado
        hour = datetime.utcnow().hour
        if str(hour) not in stats['busiest_hours']:
            stats['busiest_hours'][str(hour)] = 0
        stats['busiest_hours'][str(hour)] += 1
        
        # Atualizar top staff
        if staff_id:
            staff_str = str(staff_id)
            if staff_str not in stats['top_staff']:
                stats['top_staff'][staff_str] = 0
            stats['top_staff'][staff_str] += 1
        
        # Estatísticas mensais
        month_key = datetime.utcnow().strftime('%Y-%m')
        if month_key not in stats['monthly_stats']:
            stats['monthly_stats'][month_key] = {
                'tickets': 0,
                'closed': 0,
                'ratings': []
            }
        stats['monthly_stats'][month_key]['tickets'] += 1
        
        self.bot.save_statistics()
    
    def add_rating(self, guild_id: int, rating: int):
        """Adiciona uma avaliação"""
        stats = self.bot.get_statistics(guild_id)
        stats['satisfaction_ratings'].append(rating)
        
        # Manter apenas últimas 100 avaliações
        if len(stats['satisfaction_ratings']) > 100:
            stats['satisfaction_ratings'] = stats['satisfaction_ratings'][-100:]
        
        # Adicionar ao mês atual
        month_key = datetime.utcnow().strftime('%Y-%m')
        if month_key in stats['monthly_stats']:
            if 'ratings' not in stats['monthly_stats'][month_key]:
                stats['monthly_stats'][month_key]['ratings'] = []
            stats['monthly_stats'][month_key]['ratings'].append(rating)
        
        self.bot.save_statistics()
    
    @app_commands.command(name="estatisticas", description="Ver estatísticas detalhadas do sistema")
    @app_commands.describe(periodo="Período para análise")
    @app_commands.choices(periodo=[
        app_commands.Choice(name="Geral", value="all"),
        app_commands.Choice(name="Mês Atual", value="month"),
        app_commands.Choice(name="Última Semana", value="week")
    ])
    async def estatisticas(self, interaction: discord.Interaction, periodo: str = "all"):
        """Mostra estatísticas detalhadas"""
        stats = self.bot.get_statistics(interaction.guild_id)
        
        embed = discord.Embed(
            title="📊 Estatísticas do Sistema de Tickets",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        
        # Estatísticas gerais
        embed.add_field(
            name="🎫 Tickets",
            value=f"**Total:** {stats['total_tickets']}\n"
                  f"**Abertos:** {len(self.bot.get_tickets_data(interaction.guild_id)['active_tickets'])}",
            inline=True
        )
        
        # Avaliação média
        if stats['satisfaction_ratings']:
            avg_rating = sum(stats['satisfaction_ratings']) / len(stats['satisfaction_ratings'])
            stars = "⭐" * int(round(avg_rating))
            embed.add_field(
                name="⭐ Avaliação",
                value=f"{avg_rating:.1f}/5.0\n{stars}\n({len(stats['satisfaction_ratings'])} avaliações)",
                inline=True
            )
        else:
            embed.add_field(name="⭐ Avaliação", value="Sem avaliações ainda", inline=True)
        
        # Tempos médios
        if stats['average_response_time'] or stats['average_resolution_time']:
            embed.add_field(
                name="⏱️ Tempo Médio",
                value=f"**Resposta:** {stats['average_response_time']}min\n"
                      f"**Resolução:** {stats['average_resolution_time']}min",
                inline=True
            )
        
        # Top 5 categorias
        if stats['tickets_by_category']:
            sorted_cats = sorted(stats['tickets_by_category'].items(), key=lambda x: x[1], reverse=True)[:5]
            cat_text = "\n".join([f"**{cat}:** {count}" for cat, count in sorted_cats])
            embed.add_field(name="📋 Top Categorias", value=cat_text, inline=True)
        
        # Horário mais movimentado
        if stats['busiest_hours']:
            sorted_hours = sorted(stats['busiest_hours'].items(), key=lambda x: x[1], reverse=True)[:3]
            hours_text = "\n".join([f"**{hour}h:** {count} tickets" for hour, count in sorted_hours])
            embed.add_field(name="🕐 Horários Pico", value=hours_text, inline=True)
        
        # Top staff
        if stats['top_staff']:
            sorted_staff = sorted(stats['top_staff'].items(), key=lambda x: x[1], reverse=True)[:5]
            staff_text = []
            for staff_id, count in sorted_staff:
                member = interaction.guild.get_member(int(staff_id))
                if member:
                    staff_text.append(f"**{member.name}:** {count}")
            if staff_text:
                embed.add_field(name="👥 Top Staff", value="\n".join(staff_text), inline=True)
        
        # Estatísticas do mês
        if periodo == "month":
            month_key = datetime.utcnow().strftime('%Y-%m')
            if month_key in stats['monthly_stats']:
                month_data = stats['monthly_stats'][month_key]
                embed.add_field(
                    name=f"📅 {month_key}",
                    value=f"**Tickets:** {month_data.get('tickets', 0)}\n"
                          f"**Fechados:** {month_data.get('closed', 0)}",
                    inline=False
                )
        
        embed.set_footer(text=f"Sistema de Tickets • {interaction.guild.name}")
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="ranking-staff", description="Ranking da equipe de suporte")
    async def ranking_staff(self, interaction: discord.Interaction):
        """Mostra ranking da equipe"""
        stats = self.bot.get_statistics(interaction.guild_id)
        
        if not stats['top_staff']:
            await interaction.response.send_message(
                "❌ Ainda não há dados suficientes para gerar um ranking!",
                ephemeral=True
            )
            return
        
        embed = discord.Embed(
            title="🏆 Ranking da Equipe de Suporte",
            description="Top membros da equipe que mais resolveram tickets",
            color=discord.Color.gold()
        )
        
        sorted_staff = sorted(stats['top_staff'].items(), key=lambda x: x[1], reverse=True)
        
        medals = ["🥇", "🥈", "🥉"]
        
        for idx, (staff_id, count) in enumerate(sorted_staff[:10]):
            member = interaction.guild.get_member(int(staff_id))
            if member:
                medal = medals[idx] if idx < 3 else f"#{idx + 1}"
                embed.add_field(
                    name=f"{medal} {member.name}",
                    value=f"**{count}** tickets resolvidos",
                    inline=True
                )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="grafico", description="Gera gráfico de estatísticas (texto)")
    @app_commands.describe(tipo="Tipo de gráfico")
    @app_commands.choices(tipo=[
        app_commands.Choice(name="Categorias", value="categories"),
        app_commands.Choice(name="Horários", value="hours"),
        app_commands.Choice(name="Mensal", value="monthly")
    ])
    async def grafico(self, interaction: discord.Interaction, tipo: str):
        """Gera gráfico em ASCII/texto"""
        stats = self.bot.get_statistics(interaction.guild_id)
        
        embed = discord.Embed(
            title=f"📊 Gráfico - {tipo.title()}",
            color=discord.Color.blue()
        )
        
        if tipo == "categories":
            if not stats['tickets_by_category']:
                await interaction.response.send_message("❌ Sem dados!", ephemeral=True)
                return
            
            sorted_cats = sorted(stats['tickets_by_category'].items(), key=lambda x: x[1], reverse=True)
            max_count = max(count for _, count in sorted_cats) if sorted_cats else 1
            
            graph = []
            for cat, count in sorted_cats[:10]:
                bar_length = int((count / max_count) * 20)
                bar = "█" * bar_length
                graph.append(f"{cat[:15]:<15} {bar} {count}")
            
            embed.description = f"```\n" + "\n".join(graph) + "\n```"
        
        elif tipo == "hours":
            if not stats['busiest_hours']:
                await interaction.response.send_message("❌ Sem dados!", ephemeral=True)
                return
            
            sorted_hours = sorted(stats['busiest_hours'].items(), key=lambda x: int(x[0]))
            max_count = max(count for _, count in sorted_hours) if sorted_hours else 1
            
            graph = []
            for hour, count in sorted_hours:
                bar_length = int((count / max_count) * 15)
                bar = "█" * bar_length
                graph.append(f"{hour:>2}h {bar} {count}")
            
            embed.description = f"```\n" + "\n".join(graph) + "\n```"
        
        elif tipo == "monthly":
            if not stats['monthly_stats']:
                await interaction.response.send_message("❌ Sem dados!", ephemeral=True)
                return
            
            sorted_months = sorted(stats['monthly_stats'].items())[-6:]  # Últimos 6 meses
            max_count = max(data['tickets'] for _, data in sorted_months) if sorted_months else 1
            
            graph = []
            for month, data in sorted_months:
                count = data['tickets']
                bar_length = int((count / max_count) * 20)
                bar = "█" * bar_length
                graph.append(f"{month} {bar} {count}")
            
            embed.description = f"```\n" + "\n".join(graph) + "\n```"
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="avaliar", description="Avalie o atendimento do ticket")
    @app_commands.describe(nota="Nota de 1 a 5 estrelas")
    @app_commands.choices(nota=[
        app_commands.Choice(name="⭐ 1 - Muito Ruim", value=1),
        app_commands.Choice(name="⭐⭐ 2 - Ruim", value=2),
        app_commands.Choice(name="⭐⭐⭐ 3 - Regular", value=3),
        app_commands.Choice(name="⭐⭐⭐⭐ 4 - Bom", value=4),
        app_commands.Choice(name="⭐⭐⭐⭐⭐ 5 - Excelente", value=5)
    ])
    async def avaliar(self, interaction: discord.Interaction, nota: int):
        """Avaliar o atendimento"""
        # Verificar se é um ticket
        tickets_data = self.bot.get_tickets_data(interaction.guild_id)
        ticket_info = tickets_data['active_tickets'].get(str(interaction.channel_id))
        
        if not ticket_info:
            # Verificar tickets fechados
            closed_tickets = tickets_data.get('closed_tickets', [])
            ticket_info = next(
                (t for t in closed_tickets if t.get('channel_id') == interaction.channel_id),
                None
            )
            
            if not ticket_info:
                await interaction.response.send_message(
                    "❌ Este não é um canal de ticket!",
                    ephemeral=True
                )
                return
        
        # Verificar se é o usuário do ticket
        if interaction.user.id != ticket_info['user_id']:
            await interaction.response.send_message(
                "❌ Apenas o criador do ticket pode avaliar!",
                ephemeral=True
            )
            return
        
        # Salvar avaliação
        self.add_rating(interaction.guild_id, nota)
        
        # Feedback visual
        stars = "⭐" * nota
        messages = {
            1: "Sentimos muito pela experiência ruim. Trabalharemos para melhorar!",
            2: "Desculpe pela experiência não satisfatória. Vamos nos esforçar mais!",
            3: "Obrigado pelo feedback! Sempre podemos melhorar.",
            4: "Que bom que você teve uma boa experiência!",
            5: "Muito obrigado! Ficamos felizes em ajudar!"
        }
        
        embed = discord.Embed(
            title="✅ Avaliação Registrada",
            description=f"{stars}\n\n{messages.get(nota, 'Obrigado pela avaliação!')}",
            color=discord.Color.green()
        )
        
        await interaction.response.send_message(embed=embed)
        
        # Log no canal de logs
        config = self.bot.get_guild_config(interaction.guild_id)
        log_channel_id = config.get('ticket_logs')
        if log_channel_id:
            log_channel = interaction.guild.get_channel(log_channel_id)
            if log_channel:
                log_embed = discord.Embed(
                    title="⭐ Nova Avaliação",
                    description=f"Ticket #{ticket_info.get('id', '?'):04d}",
                    color=discord.Color.blue()
                )
                log_embed.add_field(name="Usuário", value=interaction.user.mention, inline=True)
                log_embed.add_field(name="Nota", value=stars, inline=True)
                log_embed.add_field(name="Categoria", value=ticket_info.get('category', 'N/A'), inline=True)
                
                try:
                    await log_channel.send(embed=log_embed)
                except:
                    pass

async def setup(bot):
    await bot.add_cog(Statistics(bot))
