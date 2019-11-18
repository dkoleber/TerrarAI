## TerrarAI

### A reinforcement learning platform for Terraria

Terraria is a mechanically simple 2D sandbox game with a non-complex interface.
As is the case with many sandbox games, the objective of the game is what the player decides it to be.
However, the game contains many implicit objectives, such as staying alive or acquiring items.
These implicit objectives are easy to specify due to the mechanical simplicity of the game, 
which makes the game a great environment for a reinforcement learning agent.

TerrarAI provides many key capabilities that a reinforcement learning environment requires. 
Among them, the TerraAI provides:
* the reporting of internal game state (defined the player state, world state, and non-player character state)
* the configuration of the internal game state
* the automation of entering and exiting the game environment

These capabilities support key reinforcement learning functionality by providing methods to:
* obtain rewards and punishments for agents, and provide ways to judge when a training step should be concluded
* initialize game state and interact with agents during training, via dynamically or statically generated game state configurations
* fully automate the training process without the necessity to write scripts to interact with the game's UI

### For documentation, access the [wiki](https://github.com/dkoleber/TerrarAI/wiki).

## License

Copyright (c) 2019 Derek Koleber

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.