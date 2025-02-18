# -*- coding: utf-8 -*-
"""
****************************************************
*             Modular Voice Assistant              *
*            (c) 2025 Alexander Hering             *
****************************************************
"""
from typing import Generator, Tuple, Callable
from src.configuration import configuration as cfg
from src.services.abstractions.service_abstractions import Service, ServicePackage, EndOfStreamPackage


class HandlerService(Service):
    """
    Handler service.
    """
    def __init__(self, service_parameters: dict | None = None):
        """
        Initiates an instance.
        :param service_parameters: Service parameters.
        """
        parameters = {
            "name": "HandlerService", 
            "description": "Empty handler service.", 
            "config": {}, 
            "logger": cfg.LOGGER
        } 
        if service_parameters is not None:
            parameters.update(service_parameters)
        super().__init__(**parameters)
        self.handler_method = None

    @classmethod
    def validate_configuration(cls, process_config: dict) -> Tuple[bool | None, str]:
        """
        Validates a process configuration.
        :param process_config: Process configuration.
        :return: True or False and validation report depending on validation success. 
            None and validation report in case of warnings. 
        """
        if "handler_method" in process_config and isinstance(process_config["handler_method"], Callable):
            return True, "Validation was successful"
        else:
            return False, "No 'handler_method' given in config."
    
    def setup(self) -> bool:
        """
        Sets up service.
        :returns: True, if successful else False.
        """
        self.handler_method = self.config["handler_method"]
        return True

    def run(self) -> ServicePackage | Generator[ServicePackage, None, None] | None:
        """
        Processes queued input.
        :returns: Service package, a service package generator or None.
        """
        if not self.pause.is_set():
            input_package: ServicePackage = self.input_queue.get(block=True)
            if isinstance(input_package, ServicePackage):
                self.add_uuid(self.received, input_package.uuid)
                self.log_info(f"Received metadata:\n'{input_package.metadata_stack[-1]}'")
                    
                result = self.handler_method(input_package.content, input_package.metadata_stack[-1])
                if isinstance(result, Generator):
                    for response_tuple in result:
                        self.log_info(f"Received response shard\n'{response_tuple[0]}'.")   
                        yield ServicePackage(uuid=input_package.uuid, content=response_tuple[0], metadata_stack=input_package.metadata_stack + [response_tuple[1]])
                    yield EndOfStreamPackage(uuid=input_package.uuid, content="", metadata_stack=input_package.metadata_stack + [response_tuple[1]])
                else: 
                    self.log_info(f"Received response\n'{result[0]}'.") 
                    yield EndOfStreamPackage(uuid=input_package.uuid, content=result[0], metadata_stack=input_package.metadata_stack + [result[1]])
