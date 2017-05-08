from robophery.base import Interface, Module


class I2cModule(Module):

    def __init__(self, *args, **kwargs):
        super(I2cModule, self).__init__(*args, **kwargs)
        self._interface.setup_addr(self._addr)

    def __str__(self):
        return "{0} (connected to {1}, address {2:#x})".format(self._base_name(), self._interface._name, self._addr)

    def writeRaw8(self, value):
        self._interface.writeRaw8(self._addr, value)

    def write8(self, register, value):
        self._interface.write8(self._addr, register, value)

    def write16(self, register, value):
        self._interface.write16(self._addr, register, value)

    def writeList(self, register, data):
        self._interface.writeList(self._addr, register, data)

    def readRaw8(self):
        return self._interface.readRaw8(self._addr)

    def readU8(self, register):
        return self._interface.readU8(self._addr, register)

    def readS8(self, register):
        return self._interface.readS8(self._addr, register)

    def readU16(self, register, little_endian=True):
        return self._interface.readU16(self._addr, register, little_endian)

    def readS16(self, register, little_endian=True):
        return self._interface.readS16(self._addr, register, little_endian)

    def readList(self, register, length):
        return self._interface.readList(self._addr, register, length)


class I2cInterface(Interface):
    """
    Base class for implementing I2C bus.
    """

    def __init__(self, *args, **kwargs):
        self._addrs_used = []
        super(I2cInterface, self).__init__(*args, **kwargs)

    def __str__(self):
        return "%s (bus number: %s)" % (self._base_name(), self._bus_number)

    def setup_addr(self, addr):
        """
        Set the specified address.
        """
        self._addrs_used.append(addr)

    def writeRaw8(self, addr, value):
        """
        Write an 8-bit value on the bus (without register).
        """
        raise NotImplementedError

    def write8(self, addr, register, value):
        """
        Write an 8-bit value to the specified register.
        """
        raise NotImplementedError

    def write16(self, addr, register, value):
        """
        Write a 16-bit value to the specified register.
        """
        raise NotImplementedError

    def writeList(self, addr, register, data):
        """
        Write bytes to the specified register.
        """
        raise NotImplementedError

    def readRaw8(self):
        """
        Read an 8-bit value on the bus (without register).
        """
        raise NotImplementedError

    def readU8(self, addr, register):
        """
        Read an unsigned byte from the specified register.
        """
        raise NotImplementedError

    def readS8(self, addr, register):
        """
        Read a signed byte from the specified register.
        """
        raise NotImplementedError

    def readU16(self, addr, register, little_endian=True):
        """
        Read an unsigned 16-bit value from the specified register, with the
        specified endianness (default little endian, or least significant byte
        first).
        """
        raise NotImplementedError

    def readS16(self, addr, register, little_endian=True):
        """
        Read a signed 16-bit value from the specified register, with the
        specified endianness (default little endian, or least significant byte
        first).
        """
        raise NotImplementedError

    def readList(self, addr, register, length):
        """
        Read a length number of bytes from the specified register. Results
        will be returned as a bytearray.
        """
        raise NotImplementedError
