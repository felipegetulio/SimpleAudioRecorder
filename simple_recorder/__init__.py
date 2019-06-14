import subprocess
import re
from enum import Enum

'''
arecord is a command-line sound recorder for ALSA(Advanced Linux Sound Architecture) sound card drivers. 
It supports several file formats and multiple soundcards with multiple devices. It is basically used 
to record audio using the command-line interface.

Syntax:

arecord [flags] [filename]
If the filename is not specified then it uses Standard input.

	   -h, --help
			  Help: show syntax.

	   --version
			  Print current version.

	   -l, --list-devices
			  List all soundcards and digital audio devices

	   -L, --list-pcms
			  List all PCMs defined

	   -D, --device=NAME
			  Select PCM by name

	   -q --quiet
			  Quiet mode. Suppress messages (not sound :))

	   -t, --file-type TYPE
			  File type (voc, wav, raw or au).  If this parameter is omitted the WAVE  format  is
			  used.

	   -c, --channels=#
			  The  number  of  channels.  The default is one channel.  Valid values are 1 through
			  32.

	   -f --format=FORMAT
			  Sample format
			  Recognized sample formats are: S8 U8 S16_LE  S16_BE  U16_LE  U16_BE  S24_LE  S24_BE
			  U24_LE  U24_BE  S32_LE S32_BE U32_LE U32_BE FLOAT_LE FLOAT_BE FLOAT64_LE FLOAT64_BE
			  IEC958_SUBFRAME_LE IEC958_SUBFRAME_BE  MU_LAW  A_LAW  IMA_ADPCM  MPEG  GSM  SPECIAL
			  S24_3LE  S24_3BE  U24_3LE  U24_3BE  S20_3LE S20_3BE U20_3LE U20_3BE S18_3LE S18_3BE
			  U18_3LE
			  Some of these may not be available on selected hardware
			  The available format shortcuts are:
			  -f cd (16 bit little endian, 44100, stereo) [-f S16_LE -c2 -r44100]
			  -f cdr (16 bit big endian, 44100, stereo) [-f S16_BE -c2 -f44100]
			  -f dat (16 bit little endian, 48000, stereo) [-f S16_LE -c2 -r48000]
			  If no format is given U8 is used.

	   -r, --rate=#<Hz>
			  Sampling rate in Hertz. The default rate is 8000 Hertz.  If the value specified  is
			  less than 300, it is taken as the rate in kilohertz.  Valid values are 2000 through
			  192000 Hertz.

	   -d, --duration=#
			  Interrupt after # seconds.  A value of zero means infinity.  The default  is  zero,
			  so if this option is omitted then the arecord process will run until it is killed.

	   -s, --sleep-min=#
			  Min ticks to sleep. The default is not to sleep.

	   -M, --mmap
			  Use memory-mapped (mmap) I/O mode for the audio stream.  If this option is not set,
			  the read/write I/O mode will be used.

	   -N, --nonblock
			  Open the audio device in non-blocking mode. If the device is busy the program  will
			  exit immediately.  If this option is not set the program will block until the audio
			  device is available again.

	   -F, --period-time=#
			  Distance between interrupts is # microseconds.  If no period  time  and  no  period
			  size is given then a quarter of the buffer time is set.

	   -B, --buffer-time=#
			  Buffer  duration  is  #  microseconds If no buffer time and no buffer size is given
			  then the maximal allowed buffer time but not more than 500ms is set.

	   --period-size=#
			  Distance between interrupts is # frames If no period size and  no  period  time  is
			  given then a quarter of the buffer size is set.

	   --buffer-size=#
			  Buffer  duration is # frames If no buffer time and no buffer size is given then the
			  maximal allowed buffer time but not more than 500ms is set.

	   -A, --avail-min=#
			  Min available space for wakeup is # microseconds

	   -R, --start-delay=#
			  Delay for automatic PCM start is # microseconds (relative to buffer size if <= 0)

	   -T, --stop-delay=#
			  Delay for automatic PCM stop is # microseconds from xrun

	   -v, --verbose
			  Show PCM structure and setup.  This  option  is  accumulative.   The  VU  meter  is
			  displayed when this is given twice or three times.

	   -V, --vumeter=TYPE
			  Specifies  the  VU-meter  type,  either  stereo  or  mono.   The stereo VU-meter is
			  available only for 2-channel stereo samples with interleaved format.

	   -I, --separate-channels
			  One file for each channel.  This option disables  max-file-time  and  use-strftime,
			  and ignores SIGUSR1.  The stereo VU meter is not available with separate channels.

	   -P     Playback.  This is the default if the program is invoked by typing aplay.

	   -C     Record.  This is the default if the program is invoked by typing arecord.

	   -i, --interactive
			  Allow  interactive  operation  via stdin.  Currently only pause/resume via space or
			  enter key is implemented.

	   -m, --chmap=ch1,ch2,...
			  Give the channel map to override or follow.  Pass channel position strings like FL,
			  FR, etc.

			  If a device supports the override of the channel map, aplay tries to pass the given
			  channel map.  If it doesn't support the channel map override but still it  provides
			  the  channel  map  information,  aplay  tries to rearrange the channel order in the
			  buffer to match with the returned channel map from the device.

	   --disable-resample
			  Disable automatic rate resample.

	   --disable-channels
			  Disable automatic channel conversions.

	   --disable-format
			  Disable automatic format conversions.

	   --disable-softvol
			  Disable software volume control (softvol).

	   --test-position
			  Test ring buffer position.

	   --test-coef=<coef>
			  Test coefficient for ring buffer position; default is 8.  Expression for validation
			  is: coef * (buffer_size / 2).  Minimum value is 1.

	   --test-nowait
			  Do not wait for the ring buffer ‐ eats the whole CPU.

	   --max-file-time
			  While  recording,  when  the output file has been accumulating sound for this long,
			  close it and open a new output file.  Default is the maximum size supported by  the
			  file   format:   2   GiB   for   WAV   files.    This   option  has  no  effect  if
			  --separate-channels is specified.

	   --process-id-file <file name>
			  aplay writes its process ID here, so other programs can send signals to it.

	   --use-strftime
			  When recording, interpret %-codes in the file name  parameter  using  the  strftime
			  facility  whenever the output file is opened.  The important strftime codes are: %Y
			  is the year, %m month, %d day of the month, %H hour, %M minute and %S  second.   In
			  addition,  %v  is  the  file number, starting at 1.  When this option is specified,
			  intermediate directories for the  output  file  are  created  automatically.   This
			  option has no effect if --separate-channels is specified.

	   --dump-hw-params
			  Dump  hw_params  of  the  device  preconfigured  status  to  stderr. The dump lists
			  capabilities of the selected device such  as  supported  formats,  sampling  rates,
			  numbers of channels, period and buffer bytes/sizes/times.  For raw device hw:X this
			  option basically lists hardware capabilities of the soundcard.

	   --fatal-errors
			  Disables recovery attempts when errors  (e.g.  xrun)  are  encountered;  the  aplay
			  process instead aborts immediately.

'''

class Flags(Enum):
	HELP = '-h'
	VERSION = '--version'
	LIST_DEVICES = '-l'
	LIST_PCMS = '-L'
	PCM_NAME = '-D'
	QUIT = '-q'
	FILE_TYPE = '-t'
	CHANNELS = '-c'
	SAMPLE_FORMAT = '-f'
	SAMPLE_RATE = '-r'
	DURATION = '-d'
	SLEEP_MIN = '-s'
	MMAP = '-M'
	NON_BLOCK = '-N'
	PERIOD_TIME = '-F'
	BUFFER_TIME = '-B'

class SampleFormat(Enum):

	A_LAW = 'A_LAW'
	FLOAT64_BE = 'FLOAT64_BE'
	FLOAT64_LE = 'FLOAT64_LE'
	FLOAT_BE = 'FLOAT_BE'
	FLOAT_LE = 'FLOAT_LE'
	GSM = 'GSM'
	IEC958_SUBFRAME_BE = 'IEC958_SUBFRAME_BE'
	IEC958_SUBFRAME_LE = 'IEC958_SUBFRAME_LE'
	IMA_ADPCM = 'IMA_ADPCM'
	MPEG = 'MPEG'
	MU_LAW = 'MU_LAW'
	S16_BE = 'S16_BE'
	S16_LE = 'S16_LE'
	S18_3BE = 'S18_3BE'
	S18_3LE = 'S18_3LE'
	S20_3BE = 'S20_3BE'
	S20_3LE = 'S20_3LE'
	S24_3BE = 'S24_3BE'
	S24_3LE = 'S24_3LE'
	S24_BE = 'S24_BE'
	S24_LE = 'S24_LE'
	S32_BE = 'S32_BE'
	S32_LE = 'S32_LE'
	S8 = 'S8'
	SPECIAL = 'SPECIAL'
	U16_BE = 'U16_BE'
	U16_LE = 'U16_LE'
	U18_3LE = 'U18_3LE'
	U20_3BE = 'U20_3BE'
	U20_3LE = 'U20_3LE'
	U24_3BE = 'U24_3BE'
	U24_3LE = 'U24_3LE'
	U24_BE = 'U24_BE'
	U24_LE = 'U24_LE'
	U32_BE = 'U32_BE'
	U32_LE = 'U32_LE'
	U8 = 'U8'

class FileType(Enum):
	VOC = 'voc'
	WAV = 'wav'
	RAW = 'raw'
	AU = 'au'

class SimpleAudioDevice:  
	def __init__(self, full_name, subdevices):
		self.__full_name = full_name
		self.__subdevices = subdevices
		self.__extract_other_properties()

	def __extract_other_properties(self):
		regex = re.compile(':\s|\s')
		card_info, dev_info = self.__full_name.split(', ')
		card, card_id, card_name = regex.split(card_info, 2)
		dev, dev_id, dev_name = regex.split(dev_info, 2)

		self.__card_name = card_name
		self.__dev_name = dev_name
		self.__card_id = card_id
		self.__dev_id = dev_id
		self.__audio_device_id = 'hw:{},{}'.format(card_id, dev_id)
	
	@property
	def name(self):
		return self.__card_name

	@property
	def card_name(self):
		return self.__card_name
	
	@property
	def dev_name(self):
		return self.__dev_name
	
	@property
	def card_id(self):
		return self.__card_id

	@property
	def dev_id(self):
		return self.__dev_id

	@property
	def id(self):
		return self.__audio_device_id

	@property
	def full_name(self):
		return self.__full_name

	@property
	def subdevices(self):
		return self.__subdevices

	def __repr__(self):
		return 'AudioDevice(name:{}, id:{}, subdevices:{})'.format(self.name, self.id, self.subdevices)

	def __str__(self):
		return repr(self)


class SimpleRecorder:

	EXEC = 'arecord'

	def __init__(self, device, filename='test', file_type=FileType.WAV, channels=1, sample_format=SampleFormat.S16_LE, rate=44100,
				non_block_mode=False, separate_channels=False, strftime=None, max_file_time=None):
		
		assert isinstance(device, SimpleAudioDevice), 'device must be of type SimpleAudioDevice'
		assert isinstance(sample_format, SampleFormat), 'sample_format must be of type SampleFormat'
		assert isinstance(file_type, FileType), 'file_type must be of type FileType'

		self.__filename = filename
		self.__file_type = file_type
		self.__channels = channels
		self.__sample_format = sample_format
		self.__rate = rate
		self.__device = device
		self.__non_block_mode = '' if non_block_mode else None
		self.__separate_channels = '' if separate_channels else None
		self.__strftime = strftime
		self.__max_file_time = max_file_time
		
		self.__flags = {
			'-t': self.__file_type.value,
			'-c': self.__channels,
			'-f': self.__sample_format.value,
			'-r': self.__rate,
			'-D': self.__device.id,
			'-N': self.__non_block_mode,
			'-I': self.__separate_channels,
			'--use-strftime': self.__strftime,
			'--max-file-time': self.__max_file_time
		}

	@staticmethod
	def find_device_by_name(name):
		available_devices = SimpleRecorder.list_devices()
		
		for device in available_devices:
			if device.name == name:
				return device

		return None
		
	@staticmethod
	def version():
		output = subprocess.run([SimpleRecorder.EXEC, '--version'], stdout=subprocess.PIPE)
		return output.stdout.decode('utf-8')

	@staticmethod
	def list_devices():
		output = subprocess.run([SimpleRecorder.EXEC, '-l'], stdout=subprocess.PIPE)
		lines = output.stdout.decode('utf-8')[43:].split('\n')[:-1]

		device_info = {}
		subdevices = []
		last_line = None
		
		for line in lines:
			if 'card' in line:
				
				if last_line in device_info:
					device_info[last_line] = subdevices

				last_line = line
				subdevices = []
				device_info[line] = None

			else:
				subdevices.append(line.strip())

		if device_info[last_line] is None:
			device_info[last_line] = subdevices

		devices = []

		for full_name, subdevices in device_info.items():
			devices.append(SimpleAudioDevice(full_name, subdevices))
		
		return devices

	@property
	def filename(self):
		return self.__filename

	@filename.setter
	def filename(self, value):
		assert isinstance(value, str), 'must assign a string to filename'
		self.__filename = value
	
	@property
	def file_type(self):
		return self.__file_type

	@file_type.setter
	def file_type(self, value):
		assert isinstance(value, FileType), 'must assign a FileType object to file_type'
		self.__file_type = value
		self.__flags['-t'] = self.__file_type


	@property
	def channels(self):
		return self.__channels

	@channels.setter
	def channels(self, value):
		assert isinstance(value, int) and 1 <= value <= 32, 'Valid channel values are 1 through 32.'
		self.__channels = self.__flags['-c'] = value
	
	@property
	def sample_format(self):
		return self.__sample_format

	@sample_format.setter
	def sample_format(self, value):
		assert isinstance(value, SampleFormat), 'must assign a SampleFormat object to sample_format'
		self.__sample_format = value
		self.__flags['-f'] = self.__sample_format.value
	
	@property
	def rate(self):
		return self.__rate
	
	@rate.setter
	def rate(self, value):
		assert isinstance(value, int) and (1 <= value < 300 or 2000 <= value <= 192000), 'Valid values are 2000 through 192000 Hertz.'
		self.__rate = self.__flags['-r'] = value

	@property
	def device(self):
		return self.__device

	@device.setter
	def device(self, value):
		assert isinstance(value, SimpleAudioDevice), 'must assign a SimpleAudioDevice object to device property'
		self.__device = value
	
	@property
	def non_block_mode(self):
		return self.__non_block_mode

	@property
	def separate_channels(self):
		return self.__separate_channels
	
	@property
	def strftime(self):
		return self.__strftime

	@property
	def max_file_time(self):
		return self.__max_file_time

	@property
	def command(self):
		command = [self.EXEC]
		for key, value in self.__flags.items():
			if(value is not None):
				command += [key, str(value)]
		command.append('{}.{}'.format(self.__filename, self.__file_type.value))
		return command

	def record(self, duration=None):
		assert duration is None or isinstance(duration, int), 'duration must be an integer or None'
		self.__flags['-d'] = duration
		subprocess.run(self.command)


	
		
