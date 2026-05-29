import sounddevice as sd
import mido
import numpy
import questionary
import time

AMPLITUDE = 0.708  # Full Scale
RAMP_UP = 0.010  # Milliseconds
RAMP_DOWN = 0.010  # Milliseconds
SAMPLE_RATE = 48000
BLOCK_SIZE = 256

ATTACK_SAMPLES = RAMP_UP * SAMPLE_RATE
INCREASE_DURING_ATTACK = 1.0 / ATTACK_SAMPLES

RELEASE_SAMPLES = RAMP_DOWN * SAMPLE_RATE
DECREASE_DURING_RELEASE = 1.0 / RELEASE_SAMPLES


class Synthesizer:
    def __init__(self):
        """Initializor for Synthesizer"""
        self.phase = 0.0  # For Sawtooth
        self.synthesizer_amplitude = 0.0
        self.base_frequency = 440.0  # Edit to whatever
        self.current_frequency = 440.0
        self.state = "IDLE"  # IDLE (No Press), ATTACK, RELEASE, SUSTAIN
        self.midi_note = None  # Current MIDI note

    def synthesizer_callback(
        self, outdata: numpy.ndarray, frames: int, time, status: sd.CallbackFlags
    ) -> None:
        """Callback for SoundDevice

        Args:
            outdata (numpy.ndarray): Where Outgoing audio samples will be written to
            frames (int): Frames to be processed
            time (cffi.CData): Timestamp Info
            status (sd.CallbackFlags): Stream Status Flags
        """
        phase_increment = self.current_frequency / SAMPLE_RATE

        for i in range(frames):
            # First, update envelope amplitude
            if self.state == "ATTACK":
                self.synthesizer_amplitude += INCREASE_DURING_ATTACK
                if self.synthesizer_amplitude >= 1.0:
                    self.synthesizer_amplitude = 1.0
                    self.state = "SUSTAIN"

            elif self.state == "RELEASE":
                self.synthesizer_amplitude -= DECREASE_DURING_RELEASE
                if self.synthesizer_amplitude <= 0.0:
                    self.synthesizer_amplitude = 0.0
                    self.state = "IDLE"

            elif self.state == "IDLE":
                self.synthesizer_amplitude = 0.0

            elif self.state == "SUSTAIN":
                self.synthesizer_amplitude = 1.0

            # Then generate Sawtooth Sample
            if self.state == "IDLE":
                sample = 0.0  # Wave at the moment
            else:
                sample = (2.0 * self.phase) - 1.0  # Phase to Audio Range
                self.phase += phase_increment
                if self.phase >= 1.0:
                    self.phase = -1.0  # Keep in range

            outdata[i, 0] = (
                AMPLITUDE * self.synthesizer_amplitude * sample * 0.2
            )  # Last number scales the master volume


def start_synthesizer(midi_port: str) -> None:
    """Start the Synthesizer, with given midi port.

    Args:
        midi_port (str): Name of Midi Port.
    """

    print(f"Initializing synthesizer with input port: {midi_port}")
    synthesizer = Synthesizer()  # Initialize Synthesizer

    output_stream = sd.OutputStream(
        samplerate=SAMPLE_RATE,
        blocksize=BLOCK_SIZE,
        channels=1,
        callback=synthesizer.synthesizer_callback,
        latency="low",
    )

    with output_stream:
        try:
            with mido.open_input(midi_port) as inport:
                while True:
                    for msg in inport.iter_pending():
                        if msg.type == "note_on" and msg.velocity > 0:
                            synthesizer.midi_note = msg.note
                            synthesizer.current_frequency = midi_note_to_frequency(
                                synthesizer.base_frequency, synthesizer.midi_note
                            )
                            synthesizer.state = "ATTACK"
                        elif msg.type == "note_off" or (
                            msg.type == "note_on" and msg.velocity == 0
                        ):
                            if msg.note == synthesizer.midi_note:
                                synthesizer.state = "RELEASE"
                    time.sleep(0.00001)
        except KeyboardInterrupt:
            print("Keyboard exception. Shutting down.")


def get_midi_port() -> str:
    """Get MIDI Port, whether it's virtual or physical.

    Returns:
        Name of MIDI Port
    """
    # Download VMPK
    # Download Windows MIDI Services (https://microsoft.github.io/MIDI/get-latest/)
    # VMPK -> Edit -> MIDI Connections
    # MIDI OUT Driver -> Windows MM
    # Output MIDI Connection -> Default App Loopback A
    midi_ports = mido.get_input_names()
    if not midi_ports:
        raise Exception("There were no ports found, therefore the program cannot run.")

    return questionary.select("Choose MIDI Input.", choices=midi_ports).ask()


def midi_note_to_frequency(base_frequency: float, midi_note: int) -> float:
    """Take Midi Note and convert it to a frequency

    Args:
        base_frequency (float): Base Frequency in Hz
        midi_note (int): Midi Note

    Returns:
        Frequency in Hz
    """
    return base_frequency * (2 ** ((midi_note - 69) / 12))


if __name__ == "__main__":
    midi_port = get_midi_port()
    start_synthesizer(midi_port)
