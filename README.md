# CS project - Match madness

Match madness is a game/exercise in Duolingo. It is a game where you are supposed to match word in language you are trying to learn to its translation within the given time period.

I have decided to implement something for my CS year-end project. For my implementation I have decided on few modification from Duolingo's implementation:
- User will have unlimited time for completing the game
- User can create and run their own game from specified file 

## Quick start

Download the `.whl` file from release and run
```bash
python3 -m pip install /path/to/file/*.whl
python3 -m match_madness
```
The module has been written for `python@3.12` or newer

## Documentation

The game is trying to be as user-friendly as possible. Although developers may be interested in reading the supplementary documents:
- [DOCUMENTATION](./assets/DOCUMENTATION.md)

## CS project specification

- [x] The complexity of the solution
    - Algorithm contains nested cycles and branching
- [x] Data types
    - Project combines and uses multiple data types
- [ ] Error prevention
    - [ ] Input requirements are tested
    - [ ] IO data operation are tested
- [x] Error handling
    - User is informed about problem with GUI element
- [x] Data input
    - [x] Get input from GUI element
    - [x] Load data from a file
- [ ] Data output
    - [ ] Return data through GUI element
    - [ ] Write output data to a file
- [x] Problem decomposition
    - Problem is correctly decomposed
    - Logical units are independent functions
- [x] Code
    - Functions are documented according to [Google standard](https://google.github.io/styleguide/pyguide.html)
- [ ] Graphical user interface
    - [x] GUI is clear
    - [ ] Input and output elements are clearly separated
    - [x] Output elements are protected against user input
- [x] Real life use-case
    - Program can be used in real life without further modifications

If you are interested, you can read whole specification in this supplementary document:
- [SPECIFICATION (SK)](./assets/SPECIFICATION-sk.pdf)
