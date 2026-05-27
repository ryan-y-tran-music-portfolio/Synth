import sounddevice as sd
import mido

AMPLITUDE = 0.708 # Full Scale
RAMP_UP = 0.010 # Milliseconds
RAMP_DOWN = 0.010 # Milliseconds
SAMPLE_RATE = 48000

ATTACK_SAMPLES = RAMP_UP * SAMPLE_RATE
INCREASE_DURING_ATTACK = 1.0 / ATTACK_SAMPLES

RELEASE_SAMPLES = RAMP_DOWN * SAMPLE_RATE
DECREASE_DURING_RELEASE = 1.0 / ATTACK_SAMPLES

def midi_note_to_frequency(midi_value: int) -> float:
    """Take Midi Note and convert it to a frequency
    
    Args:
        midi_note (int): Midi Note

    Returns:
        Frequency in Hz
    """

if __name__ == "__main__":
    print("Hello")