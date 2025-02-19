# evef-shortest-path

Finding the shortest path in the Eve: Frontier universe. Specifically, this will take any region and find a shortest path (approximation) to reach each of the star systems in that region by ship jumps.

## Requirements

This code requires you to have Eve: Frontier installed. It is currently in closed alpha but you may learn more here (https://www.evefrontier.com/en). This code may change dramatically over time as more is learned about Eve: Frontier.

## How to use

First you need to build the galaxy by using the extractdata tool. By default it points to the default installation directory in Windows. If you changed that directory or are using linux/mac then use the --installdirectory flag.

```console
python extractdata.py
```

Next, specify the the starting solar system, maximum ship jump distance (in light years), and the output format. Using the --format flag will put it in a pasteable format for pasting into your notes. It is split based on the limitations of characters per note.

```console
python shortestpath.py --solarsystem "D:3347" --jumpdistance 168 --format
```

The mapanalysis file grabs some basic numbers for the galaxy and has examples of using the galaxy and graph classes. When I group the star systems in mapanalysis I use the default ~500ly max distance. However, when I check to see if a group of stars is traversable I'll use the --jumpdistance value. The former is good for checking if a gate can be built. The latter is checking if a particular ship can jump through them.

```console
python mapanalysis.py --jumpdistance 168
```
