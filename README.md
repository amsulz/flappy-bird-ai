# flappy bird ai

I made this project as part of learning machine learning. I worked on this project over the summer and uploaded it to GitHub later.

AI helped me with parts of the game code while I was working on this project.

It's Flappy Bird in Python, with a mode where birds learn when to jump. You can also play it yourself using space.

## how it works

Each generation has 60 birds, and each bird has its own small neural network. The network uses the bird's height, speed and position relative to the next pipe to decide whether to jump.

The birds that survive the longest are used to make the next generation. Their networks are mixed together and changed slightly through random mutations. The best 4 are kept unchanged.

I wrote the network in plain Python, without a machine learning framework. It has 4 inputs, 6 hidden neurons and one output.

## how to run

You need Python 3. Open a terminal in the project folder and install the dependency:

```sh
python -m pip install -r requirements.txt
```

Then choose one of these modes:

```sh
python game.py          # play yourself, space to jump
python evolve.py        # train the birds
python evolve.py fast   # train without the frame rate limit
python watch.py         # watch the saved bird
```

Training runs for up to 100 generations and stops earlier if a generation reaches a score of 100. Results are written to `log.txt`, and the saved network is in `best_brain.json`.

A saved network is included. New training starts from random networks and can overwrite it, so make a copy first if you want to keep it.

## things to improve

- add a graph of the training results
- improve collision detection
- back up `best_brain.json` automatically before new training

Sprites are from [FlapPyBird](https://github.com/sourabhv/FlapPyBird).
