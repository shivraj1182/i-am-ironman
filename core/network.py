"""
Network Connectivity Checker
Detects if system is online or offline
"""

import socket
import requests
from typing import Tuple
import logging

logger = logging.getLogger(__name__)

class NetworkManager:
    """Manages network connectivity detection"""
    
    def __init__(self):
        self.is_online = False
        self.check_interval = 30  # Check every 30 seconds
        self.last_check = 0
    
    def check_internet(self) -> bool:
        """
        Check if internet connection is available
        Returns: True if online, False if offline
        """
        try:
            # Try multiple DNS servers for reliability
            for host in ['8.8.8.8', '1.1.1.1', 'google.com']:
                try:
                    socket.create_connection((host, 53), timeout=2)
                    self.is_online = True
                    logger.info(f"🟢 Online - Connected via {host}")
                    return True
                except (socket.timeout, socket.error):
                    continue
            
            # Fallback: Try HTTP request to Google
            try:
                response = requests.get('https://www.google.com', timeout=3)
                self.is_online = True
                logger.info("🟢 Online - HTTP connection successful")
                return True
            except:
                pass
            
            self.is_online = False
            logger.warning("🔴 Offline - No internet connection detected")
            return False
            
        except Exception as e:
            logger.error(f"Error checking internet: {e}")
            self.is_online = False
            return False
    
    def get_status(self) -> Tuple[bool, str]:
        """
        Get current network status
        Returns: (is_online: bool, status_message: str)
        """
        is_online = self.check_internet()
        status_msg = "🟢 ONLINE MODE" if is_online else "🔴 OFFLINE MODE"
        return is_online, status_msg
    
    def is_connected(self) -> bool:
        """Quick check if currently connected"""
        return self.is_online
