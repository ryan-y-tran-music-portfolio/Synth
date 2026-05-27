import sounddevice as sd
import mido
import questionary

AMPLITUDE = 0.708 # Full Scale
RAMP_UP = 0.010 # Milliseconds
RAMP_DOWN = 0.010 # Milliseconds
SAMPLE_RATE = 48000

ATTACK_SAMPLES = RAMP_UP * SAMPLE_RATE
INCREASE_DURING_ATTACK = 1.0 / ATTACK_SAMPLES

RELEASE_SAMPLES = RAMP_DOWN * SAMPLE_RATE
DECREASE_DURING_RELEASE = 1.0 / ATTACK_SAMPLES

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
    result = get_midi_port()
    print(f"Using {result}")