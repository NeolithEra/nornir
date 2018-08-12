from typing import Any, Dict, Optional

from napalm import get_network_driver

from nornir.core.configuration import Config
from nornir.core.connections import ConnectionPlugin


class Napalm(ConnectionPlugin):
    """
    This plugin connects to the device using the NAPALM driver and sets the
    relevant connection.

    Inventory:
        advanced_options: passed as it is to the napalm driver
        advanced_options["timeout"]: maps to ``timeout``.
    """

    def open(
        self,
        hostname: Optional[str],
        username: Optional[str],
        password: Optional[str],
        port: Optional[int],
        platform: Optional[str],
        advanced_options: Optional[Dict[str, Any]] = None,
        configuration: Optional[Config] = None,
    ) -> None:
        advanced_options = advanced_options or {}

        parameters: Dict[str, Any] = {
            "hostname": hostname,
            "username": username,
            "password": password,
            "optional_args": {},
        }
        parameters.update(advanced_options)

        if port and "port" not in advanced_options:
            parameters["optional_args"]["port"] = port

        if advanced_options.get("timeout"):
            parameters["timeout"] = advanced_options["timeout"]

        network_driver = get_network_driver(platform)
        connection = network_driver(**parameters)
        connection.open()
        self.connection = connection

    def close(self) -> None:
        self.connection.close()
