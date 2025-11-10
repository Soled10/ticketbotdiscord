"""
Bot de Discord Configurável
Bot totalmente configurável via Discord usando slash commands
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

class ConfigurableBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True
        
        super().__init__(
            command_prefix="!",  # Fallback, mas usaremos slash commands
            intents=intents,
            help_command=None
        )
        
        self.config_file = "config/guild_configs.json"
        self.guild_configs = {}
        
    async def setup_hook(self):
        """Carrega as cogs e sincroniza comandos"""
        # Carregar configurações
        self.load_configs()
        
        # Carregar cogs
        cogs_to_load = [
            "cogs.configuracao",
            "cogs.moderacao",
            "cogs.utilidades",
            "cogs.boas_vindas"
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
    
    def get_guild_config(self, guild_id: int):
        """Obtém configuração de um servidor específico"""
        guild_id_str = str(guild_id)
        if guild_id_str not in self.guild_configs:
            # Configuração padrão
            self.guild_configs[guild_id_str] = {
                "prefix": "!",
                "welcome_channel": None,
                "goodbye_channel": None,
                "log_channel": None,
                "mod_role": None,
                "auto_role": None,
                "welcome_message": "Bem-vindo(a) {user} ao servidor!",
                "goodbye_message": "Adeus {user}!",
                "custom_emojis": {},
                "enabled_modules": {
                    "welcome": True,
                    "goodbye": True,
                    "moderation": True,
                    "auto_role": False
                }
            }
            self.save_configs()
        return self.guild_configs[guild_id_str]
    
    def update_guild_config(self, guild_id: int, key: str, value):
        """Atualiza uma configuração específica"""
        config = self.get_guild_config(guild_id)
        config[key] = value
        self.save_configs()
    
    async def on_ready(self):
        """Evento quando o bot está pronto"""
        print(f"╔═══════════════════════════════════════╗")
        print(f"║  Bot Online: {self.user.name}")
        print(f"║  ID: {self.user.id}")
        print(f"║  Servidores: {len(self.guilds)}")
        print(f"╚═══════════════════════════════════════╝")
        
        # Definir status
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="Use /ajuda para começar"
            )
        )

async def main():
    """Função principal para iniciar o bot"""
    bot = ConfigurableBot()
    
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
