from camera_helpers import absolute_move, create_camera

camera = create_camera()


# services = camera.devicemgmt.GetServices({'IncludeCapability': True})
# for s in services: # type: ignore
#     print(f"{s.Namespace} → {s.XAddr}")

# absolute_move(camera)

device_io = camera.create_deviceio_service()
outputs = device_io.GetAudioOutputs()

for out in outputs: # type: ignore
    print(f"Audio Output: {out.token}, Name: {out.Name}")