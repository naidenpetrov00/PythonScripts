from onvif import ONVIFCamera

from camera_settings import load_settings


def create_camera():
    camera_settings = load_settings()
    print(f"Settings: {camera_settings}")

    camera = ONVIFCamera(
        camera_settings.host,
        camera_settings.port,
        camera_settings.username,
        camera_settings.password,
    )
    print_camera_info(camera)
    return camera


def print_camera_info(camera: ONVIFCamera):
    print(camera)
    print("My camera`s hostname: " + str(camera.host))
