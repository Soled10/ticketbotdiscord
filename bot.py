"""
Bot de Tickets para Discord
Bot totalmente configurável via Discord usando slash commands
Sistema completo de tickets com emojis personalizados
"""
import discord
from discord.ext import commands
import os
import json
import asyncio
from datetime import datetime
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

class TicketBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True
        
        super().__init__(
            command_prefix="!",  # Fallback
            intents=intents,
            help_command=None
        )
        
        self.config_file = "config/guild_configs.json"
        self.tickets_file = "config/tickets_data.json"
        self.guild_configs = {}
        self.tickets_data = {}
        
    async def setup_hook(self):
        """Carrega as cogs e sincroniza comandos"""
        # Carregar configurações
        self.load_configs()
        self.load_tickets_data()
        
        # Carregar cogs
        cogs_to_load = [
            "cogs.ticket_config",
            "cogs.ticket_system",
            "cogs.ticket_management",
            "cogs.utilidades"
        ]
        
        for cog in cogs_to_load:
            try:
                await self.load_extension(cog)
                print(f"✅ Cog carregada: {cog}")
            except Exception as e:
                print(f"❌ Erro ao carregar {cog}: {e}")
        
        # Sincronizar comandos slash
        try:
            synced = await self.tree.sync()
            print(f"✅ {len(synced)} comandos slash sincronizados")
        except Exception as e:
            print(f"❌ Erro ao sincronizar comandos: {e}")
    
    def load_configs(self):
        """Carrega configurações de todos os servidores"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.guild_configs = json.load(f)
        else:
            self.guild_configs = {}
            self.save_configs()
    
    def save_configs(self):
        """Salva configurações no arquivo"""
        os.makedirs("config", exist_ok=True)
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.guild_configs, f, indent=4, ensure_ascii=False)
    
    def load_tickets_data(self):
        """Carrega dados dos tickets"""
        if os.path.exists(self.tickets_file):
            with open(self.tickets_file, 'r', encoding='utf-8') as f:
                self.tickets_data = json.load(f)
        else:
            self.tickets_data = {}
            self.save_tickets_data()
    
    def save_tickets_data(self):
        """Salva dados dos tickets"""
        os.makedirs("config", exist_ok=True)
        with open(self.tickets_file, 'w', encoding='utf-8') as f:
            json.dump(self.tickets_data, f, indent=4, ensure_ascii=False)
    
    def get_guild_config(self, guild_id: int):
        """Obtém configuração de um servidor específico"""
        guild_id_str = str(guild_id)
        if guild_id_str not in self.guild_configs:
            # Configuração padrão para sistema de tickets
            self.guild_configs[guild_id_str] = {
                "ticket_category": None,
                "ticket_logs": None,
                "support_role": None,
                "ticket_counter": 0,
                "ticket_message": "Olá {user}! Obrigado por abrir um ticket.\nNossa equipe responderá em breve.",
                "close_message": "Ticket fechado por {user}.",
                "max_tickets_per_user": 3,
                "ticket_categories": {
                    "suporte": {
                        "name": "Suporte Geral",
                        "emoji": "🎫",
                        "description": "Preciso de ajuda com algo",
                        "enabled": True
                    },
                    "duvida": {
                        "name": "Dúvidas",
                        "emoji": "❓",
                        "description": "Tenho uma dúvida",
                        "enabled": True
                    },
                    "denuncia": {
                        "name": "Denúncia",
                        "emoji": "🚨",
                        "description": "Reportar um problema",
                        "enabled": True
                    },
                    "parceria": {
                        "name": "Parcerias",
                        "emoji": "🤝",
                        "description": "Proposta de parceria",
                        "enabled": True
                    }
                },
                "auto_delete_closed": False,
                "delete_after_minutes": 5,
                "transcript_enabled": True
            }
            self.save_configs()
        return self.guild_configs[guild_id_str]
    
    def update_guild_config(self, guild_id: int, key: str, value):
        """Atualiza uma configuração específica"""
        config = self.get_guild_config(guild_id)
        config[key] = value
        self.save_configs()
    
    def get_tickets_data(self, guild_id: int):
        """Obtém dados de tickets de um servidor"""
        guild_id_str = str(guild_id)
        if guild_id_str not in self.tickets_data:
            self.tickets_data[guild_id_str] = {
                "active_tickets": {},
                "closed_tickets": [],
                "user_tickets": {}
            }
            self.save_tickets_data()
        return self.tickets_data[guild_id_str]
    
    async def on_ready(self):
        """Evento quando o bot está pronto"""
        print(f"╔═══════════════════════════════════════╗")
        print(f"║  🎫 Bot de Tickets Online")
        print(f"║  Nome: {self.user.name}")
        print(f"║  ID: {self.user.id}")
        print(f"║  Servidores: {len(self.guilds)}")
        print(f"╚═══════════════════════════════════════╝")
        
        # Definir status
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="tickets | /ajuda"
            )
        )

async def main():
    """Função principal para iniciar o bot"""
    bot = TicketBot()
    
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("❌ ERRO: Token do Discord não encontrado!")
        print("Configure a variável DISCORD_TOKEN no arquivo .env")
        return
    
    try:
        await bot.start(token)
    except KeyboardInterrupt:
        await bot.close()
    except Exception as e:
        print(f"❌ Erro ao iniciar o bot: {e}")
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main())
