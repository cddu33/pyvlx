"""Module for Frames."""
import struct
from .frame_helper import calc_crc
from .exception import PyVLXException


class FrameBase:
    """Class for Base Frame."""

    def __init__(self, command):
        """Initialize Base Frame."""
        self.command = command

    def __bytes__(self):
        """Get raw bytes of Frame."""
        payload = self.get_payload()
        self.validate_payload_len(payload)
        return self.build_frame(self.command, payload)

    def validate_payload_len(self, payload):
        """Validate payload len."""
        if not hasattr(self, "PAYLOAD_LEN"):
            # No fixed payload len, e.g. within FrameGetSceneListNotification
            return
        # pylint: disable=no-member
        if len(payload) != self.PAYLOAD_LEN:
            raise PyVLXException("Invalid payload len", expected_len=self.PAYLOAD_LEN, current_len=len(payload))

    def get_payload(self):
        """Return Payload."""
        raise NotImplementedError()

    def from_payload(self, payload):
        """Init frame from binary data."""
        raise NotImplementedError()

    def __str__(self):
        """Return human readable string."""
        raise NotImplementedError()

    @staticmethod
    def build_frame(command, payload):
        """Build raw bytes from command and payload."""
        packet_length = 2 + len(payload) + 1
        ret = struct.pack("BB", 0, packet_length)
        ret += struct.pack(">H", command.value)
        ret += payload
        ret += struct.pack("B", calc_crc(ret))
        return ret
