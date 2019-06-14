from simple_recorder import SimpleRecorder, FileType

devices = SimpleRecorder.list_devices()

print(devices)
# in my case, there was just one device
chosen_device = devices[0]

rec = SimpleRecorder(chosen_device, filename='example', channels=2, file_type=FileType.VOC)
rec.record(3)
rec.filename = 'another_example'
rec.record(3)

