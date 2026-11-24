"""
Cog de Assistente IA - Sistema de IA para ajudar com tickets
"""
import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import aiohttp
import json
from datetime import datetime

class AIAssistant(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ai_prompts = {
            "pt-BR": {
                "system": """Você é um assistente de suporte técnico experiente e prestativo. 
Seu trabalho é ajudar a equipe de suporte a responder tickets de forma profissional, clara e eficiente.

Diretrizes:
- Seja sempre educado e profissional
- Dê respostas claras e objetivas
- Se não souber algo, admita e sugira alternativas
- Use as FAQs fornecidas quando relevante
- Adapte o tom para ser amigável mas profissional
- Sugira próximos passos quando apropriado

Sempre responda em Português (Brasil).""",
                "suggest_response": "Com base na mensagem do usuário abaixo, sugira uma resposta profissional e útil:\n\n{message}\n\nFAQs relevantes:\n{faqs}",
                "analyze_sentiment": "Analise o sentimento da seguinte mensagem e classifique como: positivo, neutro, negativo, ou urgente:\n\n{message}",
                "categorize": "Com base na mensagem abaixo, sugira qual categoria de ticket seria mais apropriada:\n\n{message}\n\nCategorias disponíveis:\n{categories}",
                "summary": "Resuma este ticket de forma concisa:\n\n{content}"
            }
        }
    
    async def call_openai_api(self, messages: list, temperature: float = 0.7):
        """Chama a API da OpenAI"""
        if not self.bot.ai_api_key:
            return None
        
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {self.bot.ai_api_key}",
                    "Content-Type": "application/json"
                }
                
                data = {
                    "model": self.bot.ai_model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": 500
                }
                
                async with session.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result['choices'][0]['message']['content']
                    else:
                        error_text = await response.text()
                        print(f"OpenAI API Error: {error_text}")
                        return None
        except Exception as e:
            print(f"Erro ao chamar OpenAI: {e}")
            return None
    
    async def call_anthropic_api(self, messages: list, temperature: float = 0.7):
        """Chama a API da Anthropic (Claude)"""
        if not self.bot.ai_api_key:
            return None
        
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "x-api-key": self.bot.ai_api_key,
                    "Content-Type": "application/json",
                    "anthropic-version": "2023-06-01"
                }
                
                # Separar system message
                system_msg = next((m['content'] for m in messages if m['role'] == 'system'), '')
                user_messages = [m for m in messages if m['role'] != 'system']
                
                data = {
                    "model": self.bot.ai_model or "claude-3-sonnet-20240229",
                    "messages": user_messages,
                    "system": system_msg,
                    "temperature": temperature,
                    "max_tokens": 500
                }
                
                async with session.post(
                    "https://api.anthropic.com/v1/messages",
                    headers=headers,
                    json=data,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result['content'][0]['text']
                    else:
                        error_text = await response.text()
                        print(f"Anthropic API Error: {error_text}")
                        return None
        except Exception as e:
            print(f"Erro ao chamar Anthropic: {e}")
            return None
    
    async def call_ai(self, messages: list, temperature: float = 0.7):
        """Chama a API de IA configurada"""
        if self.bot.ai_provider == "openai":
            return await self.call_openai_api(messages, temperature)
        elif self.bot.ai_provider == "anthropic":
            return await self.call_anthropic_api(messages, temperature)
        else:
            return None
    
    async def suggest_response(self, user_message: str, guild_id: int):
        """Sugere uma resposta para a mensagem do usuário"""
        config = self.bot.get_guild_config(guild_id)
        
        if not config.get('ai_enabled', False):
            return None
        
        if not self.bot.ai_enabled or not self.bot.ai_api_key:
            return None
        
        # Buscar FAQs relevantes
        faq_data = self.bot.get_faq_data(guild_id)
        faqs = faq_data.get('faqs', [])
        faq_text = "\n".join([f"Q: {faq['question']}\nA: {faq['answer']}" for faq in faqs[:5]])
        
        if not faq_text:
            faq_text = "Nenhuma FAQ disponível"
        
        language = config.get('ai_language', 'pt-BR')
        prompts = self.ai_prompts.get(language, self.ai_prompts['pt-BR'])
        
        messages = [
            {"role": "system", "content": prompts['system']},
            {"role": "user", "content": prompts['suggest_response'].format(
                message=user_message,
                faqs=faq_text
            )}
        ]
        
        response = await self.call_ai(messages, temperature=0.7)
        return response
    
    async def analyze_sentiment(self, message: str, guild_id: int):
        """Analisa o sentimento da mensagem"""
        config = self.bot.get_guild_config(guild_id)
        
        if not config.get('ai_enabled', False) or not config.get('ai_sentiment_analysis', True):
            return "neutro"
        
        if not self.bot.ai_enabled or not self.bot.ai_api_key:
            return "neutro"
        
        language = config.get('ai_language', 'pt-BR')
        prompts = self.ai_prompts.get(language, self.ai_prompts['pt-BR'])
        
        messages = [
            {"role": "system", "content": "Responda apenas com uma palavra: positivo, neutro, negativo, ou urgente"},
            {"role": "user", "content": prompts['analyze_sentiment'].format(message=message)}
        ]
        
        response = await self.call_ai(messages, temperature=0.3)
        
        if response:
            response = response.lower().strip()
            if any(word in response for word in ['positivo', 'positive']):
                return "positivo"
            elif any(word in response for word in ['negativo', 'negative', 'irritado', 'angry']):
                return "negativo"
            elif any(word in response for word in ['urgente', 'urgent', 'crítico', 'critical']):
                return "urgente"
        
        return "neutro"
    
    async def categorize_message(self, message: str, guild_id: int):
        """Sugere uma categoria para a mensagem"""
        config = self.bot.get_guild_config(guild_id)
        
        if not config.get('ai_enabled', False):
            return None
        
        if not self.bot.ai_enabled or not self.bot.ai_api_key:
            return None
        
        categories = config.get('ticket_categories', {})
        cat_text = "\n".join([f"- {cat_id}: {cat_data['name']} - {cat_data['description']}" 
                             for cat_id, cat_data in categories.items() 
                             if cat_data.get('enabled', True)])
        
        language = config.get('ai_language', 'pt-BR')
        prompts = self.ai_prompts.get(language, self.ai_prompts['pt-BR'])
        
        messages = [
            {"role": "system", "content": "Responda apenas com o ID da categoria mais apropriada"},
            {"role": "user", "content": prompts['categorize'].format(
                message=message,
                categories=cat_text
            )}
        ]
        
        response = await self.call_ai(messages, temperature=0.3)
        
        if response:
            # Verificar se a resposta é uma categoria válida
            for cat_id in categories.keys():
                if cat_id in response.lower():
                    return cat_id
        
        return None
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Monitora mensagens em tickets para sugestões de IA"""
        # Ignorar mensagens do bot
        if message.author.bot:
            return
        
        # Verificar se é um canal de ticket
        if not message.guild:
            return
        
        tickets_data = self.bot.get_tickets_data(message.guild.id)
        ticket_info = tickets_data['active_tickets'].get(str(message.channel.id))
        
        if not ticket_info:
            return
        
        config = self.bot.get_guild_config(message.guild.id)
        
        # Verificar se IA está ativada
        if not config.get('ai_enabled', False):
            return
        
        # Se for o usuário do ticket (não staff)
        if message.author.id == ticket_info['user_id']:
            # Análise de sentimento
            if config.get('ai_sentiment_analysis', True):
                sentiment = await self.analyze_sentiment(message.content, message.guild.id)
                
                # Se for urgente ou negativo, notificar staff
                if sentiment in ['urgente', 'negativo']:
                    support_role_id = config.get('support_role')
                    notification_role_id = config.get('notification_role')
                    
                    mention_role = None
                    if notification_role_id:
                        mention_role = message.guild.get_role(notification_role_id)
                    elif support_role_id:
                        mention_role = message.guild.get_role(support_role_id)
                    
                    if mention_role and sentiment == 'urgente':
                        embed = discord.Embed(
                            title="⚠️ Ticket Urgente Detectado",
                            description=f"A IA detectou que este ticket pode ser urgente.",
                            color=discord.Color.red()
                        )
                        embed.add_field(name="Mensagem", value=message.content[:500], inline=False)
                        await message.channel.send(content=mention_role.mention, embed=embed)
            
            # Auto-resposta com FAQ
            if config.get('ai_auto_respond', False):
                faq_data = self.bot.get_faq_data(message.guild.id)
                if faq_data.get('auto_suggest', True) and faq_data.get('faqs'):
                    # Tentar encontrar FAQ relevante
                    suggested = await self.suggest_response(message.content, message.guild.id)
                    
                    if suggested:
                        embed = discord.Embed(
                            title="🤖 Sugestão da IA",
                            description=suggested,
                            color=discord.Color.blue()
                        )
                        embed.set_footer(text="Esta é uma sugestão automática. Nossa equipe responderá em breve.")
                        await message.channel.send(embed=embed)
    
    @app_commands.command(name="ia-sugerir", description="IA sugere uma resposta para a última mensagem")
    async def ai_suggest(self, interaction: discord.Interaction):
        """Comando para sugerir resposta com IA"""
        # Verificar se é um canal de ticket
        tickets_data = self.bot.get_tickets_data(interaction.guild_id)
        ticket_info = tickets_data['active_tickets'].get(str(interaction.channel_id))
        
        if not ticket_info:
            await interaction.response.send_message(
                "❌ Este comando só funciona em canais de ticket!",
                ephemeral=True
            )
            return
        
        config = self.bot.get_guild_config(interaction.guild_id)
        
        if not config.get('ai_enabled', False):
            await interaction.response.send_message(
                "❌ IA não está ativada! Use `/automacao ia_enabled ativar:True`",
                ephemeral=True
            )
            return
        
        if not self.bot.ai_enabled or not self.bot.ai_api_key:
            await interaction.response.send_message(
                "❌ IA não configurada no bot! Configure AI_API_KEY no .env",
                ephemeral=True
            )
            return
        
        await interaction.response.defer(ephemeral=True)
        
        # Buscar última mensagem do usuário
        async for msg in interaction.channel.history(limit=50):
            if msg.author.id == ticket_info['user_id'] and not msg.author.bot:
                suggestion = await self.suggest_response(msg.content, interaction.guild_id)
                
                if suggestion:
                    embed = discord.Embed(
                        title="🤖 Sugestão da IA",
                        description=suggestion,
                        color=discord.Color.blue()
                    )
                    embed.add_field(name="Mensagem Original", value=msg.content[:200], inline=False)
                    embed.set_footer(text="Esta é apenas uma sugestão. Revise e adapte conforme necessário.")
                    
                    await interaction.followup.send(embed=embed, ephemeral=True)
                else:
                    await interaction.followup.send(
                        "❌ Não foi possível gerar uma sugestão. Verifique a configuração da IA.",
                        ephemeral=True
                    )
                return
        
        await interaction.followup.send(
            "❌ Nenhuma mensagem do usuário encontrada recentemente.",
            ephemeral=True
        )
    
    @app_commands.command(name="ia-analisar", description="Analisa o sentimento da última mensagem do usuário")
    async def ai_analyze(self, interaction: discord.Interaction):
        """Analisa sentimento com IA"""
        # Verificar se é um canal de ticket
        tickets_data = self.bot.get_tickets_data(interaction.guild_id)
        ticket_info = tickets_data['active_tickets'].get(str(interaction.channel_id))
        
        if not ticket_info:
            await interaction.response.send_message(
                "❌ Este comando só funciona em canais de ticket!",
                ephemeral=True
            )
            return
        
        config = self.bot.get_guild_config(interaction.guild_id)
        
        if not config.get('ai_enabled', False):
            await interaction.response.send_message(
                "❌ IA não está ativada!",
                ephemeral=True
            )
            return
        
        await interaction.response.defer(ephemeral=True)
        
        # Buscar última mensagem do usuário
        async for msg in interaction.channel.history(limit=20):
            if msg.author.id == ticket_info['user_id'] and not msg.author.bot:
                sentiment = await self.analyze_sentiment(msg.content, interaction.guild_id)
                
                sentiment_emoji = {
                    "positivo": "😊",
                    "neutro": "😐",
                    "negativo": "😠",
                    "urgente": "🚨"
                }
                
                sentiment_color = {
                    "positivo": discord.Color.green(),
                    "neutro": discord.Color.blue(),
                    "negativo": discord.Color.orange(),
                    "urgente": discord.Color.red()
                }
                
                embed = discord.Embed(
                    title=f"{sentiment_emoji.get(sentiment, '🤖')} Análise de Sentimento",
                    description=f"Sentimento detectado: **{sentiment.upper()}**",
                    color=sentiment_color.get(sentiment, discord.Color.blue())
                )
                embed.add_field(name="Mensagem Analisada", value=msg.content[:300], inline=False)
                
                await interaction.followup.send(embed=embed, ephemeral=True)
                return
        
        await interaction.followup.send(
            "❌ Nenhuma mensagem do usuário encontrada.",
            ephemeral=True
        )
    
    @app_commands.command(name="ia-resumo", description="Gera um resumo do ticket com IA")
    async def ai_summary(self, interaction: discord.Interaction):
        """Gera resumo do ticket"""
        tickets_data = self.bot.get_tickets_data(interaction.guild_id)
        ticket_info = tickets_data['active_tickets'].get(str(interaction.channel_id))
        
        if not ticket_info:
            await interaction.response.send_message(
                "❌ Este comando só funciona em canais de ticket!",
                ephemeral=True
            )
            return
        
        config = self.bot.get_guild_config(interaction.guild_id)
        
        if not config.get('ai_enabled', False):
            await interaction.response.send_message("❌ IA não está ativada!", ephemeral=True)
            return
        
        if not self.bot.ai_enabled or not self.bot.ai_api_key:
            await interaction.response.send_message("❌ IA não configurada!", ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)
        
        # Coletar mensagens do ticket
        messages_text = []
        async for msg in interaction.channel.history(limit=100, oldest_first=True):
            if not msg.author.bot or msg.embeds:
                author_name = "Staff" if msg.author.id != ticket_info['user_id'] else "Usuário"
                messages_text.append(f"{author_name}: {msg.content[:200]}")
        
        content = "\n".join(messages_text)
        
        language = config.get('ai_language', 'pt-BR')
        prompts = self.ai_prompts.get(language, self.ai_prompts['pt-BR'])
        
        ai_messages = [
            {"role": "system", "content": prompts['system']},
            {"role": "user", "content": prompts['summary'].format(content=content[:3000])}
        ]
        
        summary = await self.call_ai(ai_messages, temperature=0.5)
        
        if summary:
            embed = discord.Embed(
                title="📝 Resumo do Ticket (IA)",
                description=summary,
                color=discord.Color.blue()
            )
            embed.set_footer(text=f"Ticket #{ticket_info['id']:04d}")
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            await interaction.followup.send("❌ Erro ao gerar resumo.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(AIAssistant(bot))
