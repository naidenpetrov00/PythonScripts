from dataclasses import dataclass
import json


@dataclass
class CameraSettings:
    host: str
    port: int
    username: str
    password: str


def load_settings(path="camera_config.json") -> CameraSettings:
    with open(path) as f:
        data = json.load(f)
    return CameraSettings(**data)
