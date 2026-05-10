#!/usr/bin/env python3
"""Script principal para ejecutar el bot de Minecraft."""

import sys
import logging
from src.bot import MinecraftBot

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Función principal."""
    try:
        logger.info("=" * 60)
        logger.info("🤖 MINECRAFT BOT - INICIANDO")
        logger.info("=" * 60)
        
        # Crear instancia del bot
        bot = MinecraftBot(config_path="config.yaml")
        
        # Mostrar información inicial
        logger.info(f"Bot: {bot.config['bot']['username']}")
        logger.info(f"Servidor: {bot.config['server']['host']}:{bot.config['server']['port']}")
        logger.info(f"Modo offline: {bot.config['bot']['offline_mode']}")
        
        # Iniciar bot
        bot.start()
        
    except KeyboardInterrupt:
        logger.info("\n⏹ Bot detenido por el usuario")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error fatal: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
