# Thesis Project README

This document is a separate public-facing README for the additional work carried out on top of the original CORE project.

## Project purpose

The goal of this work was to extend the CORE engine with new quarantine-based strategies for handling delayed and out-of-order events in complex event recognition systems.

The project focuses on improving event processing robustness when late events arrive and on evaluating how different quarantine policies affect correctness, dropped events, execution time, and detection delay.

## What was added

The work introduced and evaluated several quarantine policies, including:

- Direct policy
- Fixed-Time policy
- Bounded-Time policy
- New Fixed-Time policy
- Average Dynamic policy
- Jump-and-Decay Dynamic policy
- Max Dynamic policy
- Max-EMA Dynamic policy
- p99 Dynamic policy
- Per-Event Dynamic policy

These policies were integrated into the parser and evaluation flow of the engine and tested over multiple datasets.

## Thesis materials

The thesis and the presentation used for this work are included in the repository:

- Thesis PDF: [docs/thesis/thesis.pdf](docs/thesis/thesis.pdf)
- Presentation: [docs/thesis/Final-Presentation.pptx](docs/thesis/Final-Presentation.pptx)

## Main research focus

The project studies how quarantine time affects stream-processing quality in the presence of disorder. In particular, it compares how different strategies balance:

- correctness of detected complex events
- number of dropped events
- execution time
- detection delay
- memory usage of the quarantine buffer

## Repository context

This repository is based on the original CORE project:

- Original project paper: [CORE: a Complex Event Recognition Engine](https://www.vldb.org/pvldb/vol15/p1951-riveros.pdf)
- Original project license remains in place: [LICENSE.txt](LICENSE.txt)

## Notes

This file is intended to describe the thesis-related extension of the project in a clear and public-friendly way. The original repository README remains unchanged as the project’s canonical upstream documentation.
