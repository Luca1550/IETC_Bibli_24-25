import json
import os
from datetime import datetime
from enum import Enum
import enums

import repositories.models 



class Encoder(json.JSONEncoder):
    """    
    Custom JSON encoder to handle serialization of custom objects.
    This class herits from json.JSONEncoder and overrides the default method to handle custom objects.
    """
    def default(self, obj):
        """
        Custom method to serialize custom objects into JSON format.
        This method checks the type of the object and returns a dictionary representation of it.
        Args:
            obj (any): Object to be serialized.
        Returns:
            dict: Dictionary representation of the object.
        """
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, Enum):  
            return {
                "__enum__": obj.__class__.__name__,  
                "value": obj.value 
            }
        elif hasattr(obj, '__dict__'):
            data = {
                key: value for key, value in obj.__dict__.items() 
                if not key.startswith('_')
            }
            return {
                "__type__": obj.__class__.__name__,
                **data
            }
        return super().default(obj)
    
class Decoder:

    _models_dict = {
    name: obj
    for name, obj in repositories.models.__dict__.items()
    if hasattr(obj, '__dict__') and isinstance(obj, type)
    }

    _enums_dict = {
        name: obj
    for name, obj in enums.__dict__.items()
    if hasattr(obj, '__dict__') and isinstance(obj, type)
    }

    @staticmethod
    def decoder_hook(dct):
        """
        Custom JSON decoder to handle deserialization of custom objects.
        This method checks the '__type__' key in the dictionary and returns the corresponding object.
        Args:
            dct (dict): Dictionary to be decoded.
        Returns:
            object: The corresponding object based on the '__type__' key.
        """
        if '__enum__' in dct:
                    type_name = dct.pop('__enum__')
                    model = Decoder._enums_dict.get(type_name)
                    if model is not None:
                        return model(**dct)
        if '__type__' in dct:
            type_name = dct.pop('__type__')
            model = Decoder._models_dict.get(type_name)
            if model is not None:
                return model(**dct)
        return dct

class JsonStorage:
    
    @staticmethod
    def _encode(jsonFile, data):
        """
        Save data to a JSON file.
        Args:
            jsonFile (str): Path to the JSON file where data will be saved.
            data (any): Data to be saved in JSON format.
        """
        try:
            with open(jsonFile, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, cls=Encoder)
        except Exception as e:
            raise Exception(f"🛑 Error {e}")

    @staticmethod
    def _decode(jsonFile):
        """
        Load data from a JSON file.
        Args:
            jsonFile (str): Path to the JSON file from which data will be loaded.
        Returns:
            any: Data loaded from the JSON file.
        """
        try:
            with open(jsonFile, 'r', encoding='utf-8') as file:
                data = json.load(file, object_hook=Decoder.decoder_hook)
                return data
        except Exception as e:
            raise Exception(f"🛑 Error {e}")

    @staticmethod
    def save_all(path, data):
        """
        Saves the list of authors to the JSON file.
        If the file doesn't exist, it creates a new one.
        """
        JsonStorage._encode(path, data)

    @staticmethod
    def load_all(path):
        """
        Loads the list of authors from the JSON file.
        If the file doesn't exist, it returns an empty list.
        """
        if os.path.isfile(path):
            data = JsonStorage._decode(path)
            return data
        else:
            return []