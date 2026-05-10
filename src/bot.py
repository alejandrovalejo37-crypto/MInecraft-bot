import logging
import yaml
import time
import random
from datetime import datetime
from typing import Dict, List, Tuple
from pathlib import Path

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MinecraftBot:
    """Bot automático para Minecraft que se conecta como un jugador normal."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Inicializar el bot con configuración.
        
        Args:
            config_path (str): Ruta al archivo de configuración YAML
        """
        self.config = self._load_config(config_path)
        self.is_running = False
        self.inventory = {}
        self.current_position = {"x": 0.0, "y": 64.0, "z": 0.0}
        self.target_position = {"x": 0.0, "y": 64.0, "z": 0.0}
        logger.info(f"Bot inicializado: {self.config['bot']['username']}")
    
    def _load_config(self, config_path: str) -> Dict:
        """Cargar configuración desde archivo YAML."""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            logger.info(f"Configuración cargada desde {config_path}")
            return config
        except FileNotFoundError:
            logger.error(f"Archivo de configuración no encontrado: {config_path}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Error al parsear YAML: {e}")
            raise
    
    def connect(self) -> bool:
        """
        Conectar al servidor de Minecraft.
        
        Returns:
            bool: True si la conexión fue exitosa, False en caso contrario
        """
        try:
            server_config = self.config['server']
            logger.info(f"Conectando a {server_config['host']}:{server_config['port']}")
            
            # Aquí iría la lógica real de conexión con minecraft-protocol
            # Por ahora es simulado
            time.sleep(2)
            
            self.is_running = True
            logger.info(f"✓ Conectado exitosamente al servidor {server_config['name']}")
            return True
            
        except Exception as e:
            logger.error(f"✗ Error al conectar: {e}")
            return False
    
    def disconnect(self):
        """Desconectar del servidor."""
        try:
            logger.info("Desconectando del servidor...")
            self.is_running = False
            logger.info("✓ Desconexión completada")
        except Exception as e:
            logger.error(f"Error al desconectar: {e}")
    
    def move(self, direction: str = "random"):
        """
        Moverse en el servidor.
        
        Args:
            direction (str): Dirección del movimiento (random, north, south, east, west)
        """
        movement_config = self.config['movement']
        
        if not movement_config['enabled']:
            return
        
        if direction == "random":
            # Movimiento aleatorio
            dx = random.uniform(-5, 5)
            dz = random.uniform(-5, 5)
        else:
            # Movimiento direccional
            directions = {
                "north": (0, -5),
                "south": (0, 5),
                "east": (5, 0),
                "west": (-5, 0)
            }
            dx, dz = directions.get(direction, (0, 0))
        
        # Actualizar posición objetivo
        self.target_position['x'] += dx
        self.target_position['z'] += dz
        
        # Limitar a rango de movimiento configurado
        self.target_position['x'] = max(
            movement_config['min_x'],
            min(movement_config['max_x'], self.target_position['x'])
        )
        self.target_position['z'] = max(
            movement_config['min_z'],
            min(movement_config['max_z'], self.target_position['z'])
        )
        
        # Interpolar movimiento actual
        self.current_position['x'] += dx * 0.1
        self.current_position['z'] += dz * 0.1
        
        logger.debug(f"Moviéndose a {self.current_position['x']:.1f}, {self.current_position['z']:.1f}")
    
    def collect_blocks(self) -> List[str]:
        """
        Recolectar bloques cercanos.
        
        Returns:
            List[str]: Lista de bloques recolectados
        """
        collection_config = self.config['collection']
        
        if not collection_config['enabled']:
            return []
        
        collected = []
        target_blocks = collection_config['target_blocks']
        
        # Simular búsqueda de bloques cercanos
        for block_type in target_blocks:
            if random.random() > 0.7:  # 30% de probabilidad
                self.inventory[block_type] = self.inventory.get(block_type, 0) + 1
                collected.append(block_type)
                logger.info(f"✓ Bloques recolectados: {block_type} (Total: {self.inventory[block_type]})")
        
        return collected
    
    def build_structure(self, structure_type: str = "wall", size: int = 5) -> bool:
        """
        Construir una estructura.
        
        Args:
            structure_type (str): Tipo de estructura (wall, tower, house)
            size (int): Tamaño de la estructura
            
        Returns:
            bool: True si se construyó exitosamente
        """
        building_config = self.config['building']
        
        if not building_config['enabled']:
            logger.warning("Construcción deshabilitada en configuración")
            return False
        
        build_blocks = building_config['build_blocks']
        
        if not build_blocks:
            logger.warning("No hay bloques disponibles para construir")
            return False
        
        try:
            logger.info(f"Construyendo {structure_type} de tamaño {size}...")
            
            if structure_type == "wall":
                blocks_needed = size * size
            elif structure_type == "tower":
                blocks_needed = size * 3
            elif structure_type == "house":
                blocks_needed = size * size * 2
            else:
                blocks_needed = size
            
            # Verificar inventario
            total_blocks = sum(self.inventory.values())
            if total_blocks < blocks_needed:
                logger.warning(
                    f"Inventario insuficiente: tengo {total_blocks}, "
                    f"necesito {blocks_needed}"
                )
                return False
            
            # Usar bloques del inventario
            for block_type in build_blocks:
                if self.inventory.get(block_type, 0) >= blocks_needed:
                    self.inventory[block_type] -= blocks_needed
                    logger.info(f"✓ {structure_type} construido exitosamente")
                    return True
            
            logger.error("No hay suficientes bloques del tipo correcto")
            return False
            
        except Exception as e:
            logger.error(f"Error al construir: {e}")
            return False
    
    def get_inventory(self) -> Dict[str, int]:
        """
        Obtener inventario actual.
        
        Returns:
            Dict[str, int]: Inventario con bloques y cantidades
        """
        return self.inventory.copy()
    
    def get_position(self) -> Tuple[float, float, float]:
        """
        Obtener posición actual del bot.
        
        Returns:
            Tuple[float, float, float]: Coordenadas (x, y, z)
        """
        return (
            self.current_position['x'],
            self.current_position['y'],
            self.current_position['z']
        )
    
    def run_cycle(self):
        """Ejecutar un ciclo de acciones automáticas."""
        try:
            # Movimiento
            if self.config['movement']['enabled']:
                self.move()
            
            # Recolección
            if self.config['collection']['enabled']:
                self.collect_blocks()
            
            # Construcción automática (cada 10 ciclos)
            if random.random() > 0.9 and self.config['building']['enabled']:
                self.build_structure("wall", size=3)
            
            time.sleep(self.config['behavior']['action_delay'])
            
        except Exception as e:
            logger.error(f"Error en ciclo: {e}")
    
    def start(self):
        """Iniciar el bot y ejecutar en bucle."""
        if not self.connect():
            logger.error("No se pudo conectar al servidor")
            return
        
        try:
            logger.info("Bot iniciado. Presiona Ctrl+C para detener.")
            max_time = self.config['behavior']['max_session_time']
            start_time = time.time()
            cycle_count = 0
            
            while self.is_running:
                # Verificar tiempo máximo
                if max_time > 0 and (time.time() - start_time) > max_time:
                    logger.info("Tiempo máximo de sesión alcanzado")
                    break
                
                self.run_cycle()
                cycle_count += 1
                
                # Log de progreso cada 100 ciclos
                if cycle_count % 100 == 0:
                    pos = self.get_position()
                    inv_count = sum(self.get_inventory().values())
                    logger.info(
                        f"Ciclo #{cycle_count} - Posición: ({pos[0]:.1f}, {pos[2]:.1f}) - "
                        f"Items: {inv_count}"
                    )
        
        except KeyboardInterrupt:
            logger.info("\n⏹ Deteniendo bot...")
        
        finally:
            self.disconnect()
    
    def get_status(self) -> Dict:
        """
        Obtener estado actual del bot.
        
        Returns:
            Dict: Estado con posición, inventario e información de conexión
        """
        return {
            "running": self.is_running,
            "position": self.get_position(),
            "inventory": self.get_inventory(),
            "inventory_count": sum(self.get_inventory().values()),
            "timestamp": datetime.now().isoformat()
        }
