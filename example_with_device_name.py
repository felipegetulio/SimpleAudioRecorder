from simple_recorder import SimpleRecorder, SampleFormat, FileType

device_name = 'PCH [HDA Intel PCH]'

device = SimpleRecorder.find_device_by_name(device_name)

if device is not None:
	rec = SimpleRecorder(device, filename='example_name', channels=2)

	rec.record(5)

	rec.rate = 48000
	rec.filename = 'example_rate'
	rec.record(5)
else:
	print('There is no device matching the name {}'.format(device_name))
