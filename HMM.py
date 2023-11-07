

import random
import argparse
import codecs
import os
import numpy

# observations
class Observation:
    def __init__(self, stateseq, outputseq):
        self.stateseq  = stateseq   # sequence of states
        self.outputseq = outputseq  # sequence of outputs
    def __str__(self):
        return ' '.join(self.stateseq)+'\n'+' '.join(self.outputseq)+'\n'
    def __repr__(self):
        return self.__str__()
    def __len__(self):
        return len(self.outputseq)

# hmm model
class HMM:
    def __init__(self, transitions={}, emissions={}):
        """creates a model from transition and emission probabilities"""
        ## Both of these are dictionaries of dictionaries. e.g. :
        # {'#': {'C': 0.814506898514, 'V': 0.185493101486},
        #  'C': {'C': 0.625840873591, 'V': 0.374159126409},
        #  'V': {'C': 0.603126993184, 'V': 0.396873006816}}

        self.transitions = transitions
        self.emissions = emissions

    ## part 1 - you do this.
    def load(self, basename):
        """reads HMM structure from transition (basename.trans),
        and emission (basename.emit) files,
        as well as the probabilities."""
        self.transitions = {}
        self.emissions = {}
        tfile = open(f'{basename}.trans', 'r')
        for line in tfile:
            toparse = line.split()
            if toparse[0] not in self.transitions:
                self.transitions.update({toparse[0]: {toparse[1]: toparse[2]}})
            else:
                self.transitions[toparse[0]].update({toparse[1]: toparse[2]})
        efile = open(f'{basename}.emit', 'r')
        for line in efile:
            toparse = line.split()
            if toparse[0] not in self.emissions:
                self.emissions.update({toparse[0]: {toparse[1]: toparse[2]}})
            else:
                self.emissions[toparse[0]].update({toparse[1]: toparse[2]})


   ## you do this.
    def generate(self, n):
        """return an n-length observation by randomly sampling from this HMM."""
        outputseq = []
        currentstate = '#'
        stateseq = []

        for _ in range(n):
            currentstate = numpy.random.choice(
                a=list(self.transitions[currentstate].keys()),
                p=list(self.transitions[currentstate].values())
            )
            stateseq.append(currentstate)


        for state in stateseq:
            currentoutput = numpy.random.choice(
                a=list(self.emissions[state].keys()),
                p=list(self.emissions[state].values())
            )
            outputseq.append(currentoutput)

        return Observation(stateseq, outputseq)

    def forward(self, observation=None, filename=None):
        """given a sequence of observations,
        find and return the most likely final state,
        using the forward algorithm.
        """
        observations = []
        finalstates = []
        if observation:
            observations.append(observation.outputseq)
        if filename:
            ofile = open(filename, 'r')
            for line in ofile:
                newline = line.split()
                if newline:
                    observations.append(newline)
        for obs in observations:
            matrix = []
            matrix.append([' ', '-'])
            matrix.append(['#', 1.0])
            rows = 1
            for state in self.transitions:
                if state != '#':
                    rows += 1
                    matrix.append([state])
                    matrix[rows].append(0)
            count = 1
            for output in obs:
                matrix[0].append(output)
                matrix[1].append(0)
                for row in matrix:
                    sum = 0
                    if row[0] != '#' and row[0] != ' ':
                        if count > 1:
                            for row2 in matrix:
                                if row2[0] != '#' and row2[0] != ' ' and output in self.emissions[row[0]]:
                                    sum += float(row2[count]) * float(self.transitions[row[0]][row2[0]]) * float(
                                        self.emissions[row[0]][output])
                        elif output in self.emissions[row[0]]:
                            sum = float(self.transitions['#'][row[0]]) * float(self.emissions[row[0]][output])
                        row.append(sum)
                    else:
                        row.append(0)
                count += 1
            bestval= 0
            bestname = None
            for values in matrix:
                if values[-1] > bestval:
                    bestname = values[0]
                    bestval = values[-1]
            finalstates.append(bestname)
        return finalstates

    ## you do this: Implement the Viterbi alborithm. Given an Observation (a list of outputs or emissions)
    ## determine the most likely sequence of states.

    def viterbi(self, observation=None, filename=None):
        """given an observation,
        find and return the state sequence that generated
        the output sequence, using the Viterbi algorithm.
        """
        observations = []
        finalstates = []
        index = 1
        if observation:
            observations.append(observation.outputseq)
        if filename:
            ofile = open(filename, 'r')
            for line in ofile:
                newline = line.split()
                if newline:
                    observations.append(newline)
        for obs in observations:
            matrix = []
            beststates = []
            matrix.append([' ', '-'])
            matrix.append(['#', 1.0])
            rows = 1
            for state in self.transitions:
                if state != '#':
                    rows += 1
                    matrix.append([state])
                    matrix[rows].append(0)
            count = 1
            for output in obs:
                matrix[0].append(output)
                matrix[1].append(0)
                for row in matrix:
                    sum = []
                    if row[0] != '#' and row[0] != ' ':
                        if count > 1:
                            for row2 in matrix:
                                if row2[0] != '#' and row2[0] != ' ' and output in self.emissions[row[0]]:
                                    sum.append(float(row2[count]) * float(self.transitions[row[0]][row2[0]]) * float(
                                        self.emissions[row[0]][output]))
                        elif output in self.emissions[row[0]]:
                            sum.append(float(self.transitions['#'][row[0]]) * float(self.emissions[row[0]][output]))
                        if len(sum) > 0:
                            row.append(max(sum))
                        else:
                            row.append(0)
                count += 1
            for i in range(2, len(obs)+2):
                bestval = 0
                bestname = None
                for values in matrix:
                    if values[0] != '#' and values[0] != ' ':
                        if values[i] > bestval:
                            bestname = values[0]
                            bestval = values[i]
                beststates.append(bestname)
            finalstates.append({index : beststates})
            index += 1
        return finalstates





