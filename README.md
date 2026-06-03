# Synth

## What did I do?

I created a sawtooth wave monophonic synthesizer that runs at -3dBFS (0.708 full scale). The program is set up in away such that key events are processed between sample outputs; the sound produced by the samples are then sent to the system's default output.

Because I do not have an actual MIDI controller, I had to download [VMPK](https://vmpk.sourceforge.io/); while the program should still allow the easy connection of actual MIDI controllers, the main usage has [Windows MIDI Services](https://microsoft.github.io/MIDI/get-latest/) in mind.

For any individuals downloading this program, it should be easy for them to modify the synthesizer parameters, especially the base frequency, so make the synthesizer sound different as they please!

Also, much like I did for the Aletoric project, I scaled the volume by 0.2 to avoid shattering eardrums.

## How did it Go?

The process of creating the synthesizer went well, with a few hurdles; the Synthesizer itself had me struggling to determine the best way to contain it and how to provide its callback to sounddevice. Secondly, I had to create a Synthesizer without an actual MIDI controller. Figuring out how to connect a virtual MIDI controller to a port such that the Synthesizer recognizes it took a while, but I managed to do it.

I think it sounds like a real synthesizer! Although admittedly at first I thought it sounded kinda awful.

## What's next?

There are plenty of upgrades to my synthesizer that would make it better. One, adding a --midi-device argument so the program automatically connects to a named MIDI controller rather than prompting the user what to connect to. Two, instead of just an Attack-Release envelope, this synthesizer could be modified to add decay time and sustain level. My program also has a limited numbered of MIDI messages: there's note on/off, but I could also add aftertouch, pitch bend, and program change.

## How to Build

### Installing uv

Follow the instructions to install the uv package manager [here](https://docs.astral.sh/uv/getting-started/installation/).

### Installing VMPK

a

### Installing Windows MIDI Services

a

### Connecting VMPK With Windows MIDI Services

a

### Running the Program

a
