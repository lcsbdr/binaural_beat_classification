import select, serial, threading, time

# Byte codes
CONNECT              = '\xc0'
DISCONNECT           = '\xc1'
AUTOCONNECT          = '\xc2'
SYNC                 = '\xaa'
EXCODE               = '\x55'
POOR_SIGNAL          = '\x02'
ATTENTION            = '\x04'
MEDITATION           = '\x05'
BLINK                = '\x16'
HEADSET_CONNECTED    = '\xd0'
HEADSET_NOT_FOUND    = '\xd1'
HEADSET_DISCONNECTED = '\xd2'
REQUEST_DENIED       = '\xd3'
STANDBY_SCAN         = '\xd4'
ASIC_EEG_POWER       = '\x83'
RAW_DATA             = '\x80'

# Status codes
STATUS_CONNECTED     = 'connected'
STATUS_SCANNING      = 'scanning'
STATUS_STANDBY       = 'standby'

class Headset(object):
    """
    A MindWave Headset
    """

    class DongleListener(threading.Thread):
        """
        Serial listener for dongle device.
        """
        def __init__(self, headset, *args, **kwargs):
            """Set up the listener device."""
            self.headset = headset
            super(Headset.DongleListener, self).__init__(*args, **kwargs)

        def run(self):
            """Run the listener thread."""
            s = self.headset.dongle

            # Re-apply settings to ensure packet stream
            s.write(DISCONNECT)
            d = s.getSettingsDict()
            for i in xrange(2):
                d['rtscts'] = not d['rtscts']
                s.applySettingsDict(d)

            while True:
                # Begin listening for packets
                try:
                    if s.read() == SYNC and s.read() == SYNC:
                        # Packet found, determine plength
                        while True:
                            plength = ord(s.read())
                            if plength != 170:
                                break
                        if plength > 170:
                            continue

                        # Read in the payload
                        payload = s.read(plength)

                        # Verify its checksum
                        val = sum(ord(b) for b in payload[:-1])
                        val &= 0xff
                        val = ~val & 0xff
                        chksum = ord(s.read())

                        #if val == chksum:
                        if True: # ignore bad checksums
                            self.parse_payload(payload)
                except (select.error, OSError):
                    break
                except serial.SerialException:
                    s.close()
                    break

        def parse_payload(self, payload):
            """Parse the payload to determine an action."""
            while payload:
                # Parse data row
                excode = 0
                try:
                    code, payload = payload[0], payload[1:]
                except IndexError:
                    pass
                while code == EXCODE:
                    # Count excode bytes
                    excode += 1
                    try:
                        code, payload = payload[0], payload[1:]
                    except IndexError:
                        pass
                if ord(code) < 0x80:
                    # This is a single-byte code
                    try:
                        value, payload = payload[0], payload[1:]
                    except IndexError:
                        pass
                    if code == POOR_SIGNAL:
                        # Poor signal
                        old_poor_signal = self.headset.poor_signal
                        self.headset.poor_signal = ord(value)
                        if self.headset.poor_signal > 0:
                            if old_poor_signal == 0:
                                for handler in \
                                        self.headset.poor_signal_handlers:
                                    handler(self.headset,
                                            self.headset.poor_signal)
                        else:
                            if old_poor_signal > 0:
                                for handler in \
                                        self.headset.good_signal_handlers:
                                    handler(self.headset,
                                            self.headset.poor_signal)
                    elif code == ATTENTION:
                        # Attention level
                        self.headset.attention = ord(value)
                        for handler in self.headset.attention_handlers:
                            handler(self.headset, self.headset.attention)
                    elif code == MEDITATION:
                        # Meditation level
                        self.headset.meditation = ord(value)
                        for handler in self.headset.meditation_handlers:
                            handler(self.headset, self.headset.meditation)
                    elif code == BLINK:
                        # Blink strength
                        self.headset.blink = ord(value)
                        for handler in self.headset.blink_handlers:
                            handler(self.headset, self.headset.blink)
                else:
                    # This is a multi-byte code
                    try:
                        vlength, payload = ord(payload[0]), payload[1:]
                    except IndexError:
                        continue
                    value, payload = payload[:vlength], payload[vlength:]
                    # Multi-byte EEG and Raw Wave codes not included
                    # See Mindset Communications Protocol
                    if code == RAW_DATA:
                        try:
                            self.headset.raw_data =  int( "".join("{0:x}".format(ord(c)) for c in value),16)
                        except:
                            pass
                    if code == ASIC_EEG_POWER:
                         #multi byte code for EEG band data
                        try:
                            self.headset.delta = int( "".join("{0:x}".format(ord(c)) for c in value[0:3]),16)
                            self.headset.theta = int( "".join("{0:x}".format(ord(c)) for c in value[3:6]),16)
                            self.headset.low_alpha = int( "".join("{0:x}".format(ord(c)) for c in value[6:9]),16)
                            self.headset.high_alpha = int( "".join("{0:x}".format(ord(c)) for c in value[9:12]),16)
                            self.headset.low_beta = int( "".join("{0:x}".format(ord(c)) for c in value[12:15]),16)
                            self.headset.high_beta = int( "".join("{0:x}".format(ord(c)) for c in value[15:18]),16)
                            self.headset.low_gamma = int( "".join("{0:x}".format(ord(c)) for c in value[18:21]),16)
                            self.headset.mid_gamma = int( "".join("{0:x}".format(ord(c)) for c in value[21:24]),16)
                            
                        except:
                            continue
                        
                        for handler in self.headset.low_alpha_handlers:
                            handler(self.headset, self.headset.low_alpha)
                        for handler in self.headset.high_alpha_handlers:
                            handler(self.headset, self.headset.high_alpha)
                        for handler in self.headset.low_beta_handlers:
                            handler(self.headset, self.headset.low_beta)
                        for handler in self.headset.high_beta_handlers:
                            handler(self.headset, self.headset.high_beta)
                        for handler in self.headset.delta_handlers:
                            handler(self.headset, self.headset.delta)
                        for handler in self.headset.theta_handlers:
                            handler(self.headset, self.headset.theta)
                        for handler in self.headset.low_gamma_handlers:
                            handler(self.headset, self.headset.low_gamma)
                        for handler in self.headset.mid_gamma_handlers:
                            handler(self.headset, self.headset.mid_gamma)
                            

                    if code == HEADSET_CONNECTED:
                        # Headset connect success
                        run_handlers = self.headset.status != STATUS_CONNECTED
                        self.headset.status = STATUS_CONNECTED
                        self.headset.headset_id = value.encode('hex')
                        if run_handlers:
                            for handler in \
                                    self.headset.headset_connected_handlers:
                                handler(self.headset)
                    elif code == HEADSET_NOT_FOUND:
                        # Headset not found
                        if vlength > 0:
                            not_found_id = value.encode('hex')
                            for handler in \
                                    self.headset.headset_notfound_handlers:
                                handler(self.headset, not_found_id)
                        else:
                            for handler in \
                                    self.headset.headset_notfound_handlers:
                                handler(self.headset, None)
                    elif code == HEADSET_DISCONNECTED:
                        # Headset disconnected
                        headset_id = value.encode('hex')
                        for handler in \
                                self.headset.headset_disconnected_handlers:
                            handler(self.headset, headset_id)
                    elif code == REQUEST_DENIED:
                        # Request denied
                        for handler in self.headset.request_denied_handlers:
                            handler(self.headset)
                    elif code == STANDBY_SCAN:
                        # Standby/Scan mode
                        try:
                            byte = ord(value[0])
                        except IndexError:
                            byte = None
                        if byte:
                            run_handlers = (self.headset.status !=
                                            STATUS_SCANNING)
                            self.headset.status = STATUS_SCANNING
                            if run_handlers:
                                for handler in self.headset.scanning_handlers:
                                    handler(self.headset)
                        else:
                            run_handlers = (self.headset.status !=
                                            STATUS_STANDBY)
                            self.headset.status = STATUS_STANDBY
                            if run_handlers:
                                for handler in self.headset.standby_handlers:
                                    handler(self.headset)


    def __init__(self, device, headset_id=None, open_serial=True):
        """Initialize the  headset."""
        # Initialize headset values
        self.dongle = None
        self.listener = None
        self.device = device
        self.headset_id = headset_id
        self.poor_signal = 255
        self.attention = 0
        self.meditation = 0
        self.blink = 0
        self.status = None

        # Create event handler lists
        self.poor_signal_handlers = []
        self.good_signal_handlers = []
        self.attention_handlers = []
        self.meditation_handlers = []
        self.blink_handlers = []
        self.headset_connected_handlers = []
        self.headset_notfound_handlers = []
        self.headset_disconnected_handlers = []
        self.request_denied_handlers = []
        self.scanning_handlers = []
        self.standby_handlers = []
        self.delta_handlers = []
        self.theta_handlers = []
        self.low_alpha_handlers = []
        self.high_alpha_handlers = []
        self.low_beta_handlers = []
        self.high_beta_handlers = []
        self.low_gamma_handlers = []
        self.mid_gamma_handlers = []
        
        

        # Open the socket
        if open_serial:
            self.serial_open()

    def connect(self, headset_id=None):
        """Connect to the specified headset id."""
        if headset_id:
            self.headset_id = headset_id
        else:
            headset_id = self.headset_id
            if not headset_id:
                self.autoconnect()
                return
        self.dongle.write(''.join([CONNECT, headset_id.decode('hex')]))

    def autoconnect(self):
        """Automatically connect device to headset."""
        self.dongle.write(AUTOCONNECT)

    def disconnect(self):
        """Disconnect the device from the headset."""
        self.dongle.write(DISCONNECT)

    def serial_open(self):
        """Open the serial connection and begin listening for data."""
        # Establish serial connection to the dongle
        if not self.dongle or not self.dongle.isOpen():
            self.dongle = serial.Serial(self.device, 115200)

        # Begin listening to the serial device
        if not self.listener or not self.listener.isAlive():
            self.listener = self.DongleListener(self)
            self.listener.daemon = True
            self.listener.start()

    def serial_close(self):
        """Close the serial connection."""
        self.dongle.close()
