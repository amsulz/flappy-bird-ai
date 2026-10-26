# every bird has weights, and with them it decides when to jump,
# for example by how far it is from the ground, the top and the pipe.
# the birds that get further are crossed and their children are a bit changed
import sys
import random
import pygame

from game import *
from brain import Brain, crossover

# here we set how many birds, how strong the mutation is and when to stop
POP_SIZE = 60
MUT_RATE = 0.15
MAX_GEN = 100
GOAL = 100  # stop at this score

fast = "fast" in sys.argv  # no fps limit


def get_inputs(bird, pipes):
    # here we collect what the bird sees: its height, distance to the pipe and so on
    pipe = pipes[0]
    if pipe.x + 52 < bird.x:
        pipe = pipes[1]
    gap_center = pipe.gap_y + PIPE_GAP / 2
    return [
        (bird.y - gap_center) / HEIGHT,
        (pipe.x - bird.x) / WIDTH,
        bird.vel / 10,
        bird.y / HEIGHT,
    ]


def play_generation(brains, gen_num):
    birds = []
    for b in brains:
        bird = Bird()
        bird.brain = b
        bird.fitness = 0
        bird.alive = True
        birds.append(bird)

    pipes = [Pipe(350), Pipe(350 + PIPE_DIST)]
    base_x = 0
    score = 0
    clock = pygame.time.Clock()

    while score < GOAL:
        if not fast:
            clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        alive = [b for b in birds if b.alive]
        if not alive:
            break

        for bird in alive:
            if bird.brain.think(get_inputs(bird, pipes)):
                bird.jump()
            bird.move()
            bird.fitness += 1  # the bird gets points while it survives

        update_pipes(pipes)
        base_x = (base_x - SPEED) % -48

        for p in pipes:
            if not p.passed and p.x + 52 < 60:
                p.passed = True
                score += 1

        for bird in alive:
            if bird_dead(bird, pipes):
                bird.alive = False
                # and a penalty, bigger if the mistake was bigger (far from the gap)
                pipe = pipes[0] if pipes[0].x + 52 > bird.x else pipes[1]
                bird.fitness -= abs(bird.y - (pipe.gap_y + PIPE_GAP / 2)) / 5

        draw_window(alive, pipes, base_x, [
            "Gen " + str(gen_num),
            "Alive " + str(len(alive)) + "/" + str(len(birds)),
            "Score " + str(score),
        ])

    return birds, score


def next_generation(birds):
    # like natural selection: the strongest birds have children,
    # if a mutation is lucky the child gets more children, if not it dies out
    birds.sort(key=lambda b: b.fitness, reverse=True)
    best = [b.brain for b in birds[:10]]

    new_brains = [b.copy() for b in best[:4]]  # keep top 4
    while len(new_brains) < POP_SIZE:
        child = crossover(random.choice(best), random.choice(best))
        child.mutate(MUT_RATE)
        new_brains.append(child)
    return new_brains


def main():
    # makes 60 random birds, then every generation: play, find the best and the average score,
    # save the brain of the best bird if it's a new record, stop if it flew far enough,
    # if not make the next generation with mutations
    brains = [Brain() for _ in range(POP_SIZE)]
    record = -1

    for gen in range(1, MAX_GEN + 1):
        birds, score = play_generation(brains, gen)
        top = max(birds, key=lambda b: b.fitness)
        avg = sum(b.fitness for b in birds) / len(birds)
        print(f"gen {gen}: score {score}, best fitness {top.fitness:.0f}, avg {avg:.0f}")

        with open("log.txt", "a") as f:
            f.write(f"{gen},{score},{top.fitness:.1f},{avg:.1f}\n")

        if score > record:
            record = score
            top.brain.save("best_brain.json")
            print("  new record, saved")

        if score >= GOAL:
            print("done!")
            break

        brains = next_generation(birds)


if __name__ == "__main__":
    main()
