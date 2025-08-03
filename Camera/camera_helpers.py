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
        # "/home/naidenpetrov00/dev/PythonScripts/Camera/python-onvif-zeep/wsdl"
    )
    print_camera_info(camera)
    return camera


def print_camera_info(camera: ONVIFCamera):
    print(camera)
    print("My camera`s hostname: " + str(camera.host))


def absolute_move(camera: ONVIFCamera):
    media_service = camera.create_media_service()
    ptz_service = camera.create_ptz_service()

    profile = media_service.GetProfiles()[0]  # type: ignore
    token = profile.token

    req = ptz_service.create_type("AbsoluteMove")
    req.ProfileToken = token

    req.Position = {"PanTilt": {"x": 0.2, "y": 0.3}, "Zoom": {"x": 0.5}}

    ptz_service.AbsoluteMove(req)
