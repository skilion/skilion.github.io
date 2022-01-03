---
title: "Designing Data Intensive Applications, Chapter 1"
date: 2021-12-22
---

This post is a summary of chapter 1 from the book "Designing Data Intensive Applications". Chapter 1 introduces the fundamental terminology and metrics to evaluate data-intensive applications.

At the time of writing, "DDIA" is the number 1 best seller on Amazon in the category "Data Modeling & Design". In the book, the author, [Martin Kleppmann](https://martin.kleppmann.com/) covers the architecture of a broad range of databases and distributed data processing systems that are essential knowledge for engineers that want to to develop distributed, scalable modern applications that process huge amount of data.

## Data Intensive applications

Data-intensive means that the application is bounded by the amount of data, its complexity, and the speed at which the data is changing. This is opposed to compute-intensive application which are bounded by the amount of raw CPU power available.

Data-intensive applications are usually built from standard building blocks. These blocks have been defined empirically over a long period of time. These blocks are:

- Databases: for medium and long term data storage.
- Caches: for speeding up reads and remembering the result of expensive operations for short term.
- Search indexes: to search and filter data in various ways, efficiently.
- Stream processing: for sending data to another process to be handles asynchronously.
- Batch processing: for periodically processing a large amount of accumulated data.

However each of this blocks can be implemented in many different ways and most of the time an implementation can fall in more than one category. Therefore we need a more granular way to categorize data systems and we can use the non-functional requirements that we want from the system that ultimately we want to design:

- Reliability
- Scalability
- Maintainability

### Reliability

Reliable means that the system should work correctly (performing the correct function at the desired level of performance) even in faces of errors.

Errors can be caused by hardware (power outages, hard disk failures, network partitioning, etc.), by software (code bugs, exhaustion of resources, cascading faults), or by the humans that operate those systems.

Hardware errors can be reduced by adding redundancy, ex. backup generators, RAID systems, multiple network connections.

Software errors can be reduced with testing, behavior monitoring, process isolation.

Human errors can be reduced with sandboxes (i.e. non-production environments), gradual roll outs and fast roll backs, telemetry, training.

### Scalability

As the system grows in data volume, traffic volume, or complexity there should be reasonable ways to handle that growth.

Growth can happen on many axis such as number of concurrent users, volume of information processed, number of read and writes, or something else. These factors depends on the architecture of the system and they ultimately affect its *load*.

Once these load factors have been identified we can define how their changes affect the performances of the system, again which performances we care about depends on the nature of the system. Examples of performance metrics are throughput, latency, or response time.

When reporting on performance metrics it is common to use the average. However it is usually better to use [*percentiles*](https://en.wikipedia.org/wiki/Percentile) (such as the median) because they tells how many users actually experience that performance. Also by looking at the higher percentiles you can see how bad your outliers are.

Copying with load can be done in two ways: horizontal or vertical scaling. In reality you will most likely use a pragmatic mixture of the two approaches.

While distributing the stateless services across multiple machines is fairly straightforward, taking a stateful system from a single machine to a distributed model can introduce a lot of complexity. The architecture of systems that operate at large scale is usually highly specific to the application.

### Maintainability

New people working on the system should be able to work on it productively either maintaining the current behavior or implementing new use cases.

Three design principles help when creating maintainable systems:
- Operability: make it easy for the operations teams to keep the system running smoothly (health monitoring, debugging, capacity planning, establishing good practices for deployment and configuration, documentation, good defaults, predictable behavior).
- Simplicity: make it easy for new engineers to understand the system, by removing complexity as much as possible (good abstractions, decoupling of components).
- Evolvability: make it easy for engineers to make changes to the system in the future, adapting it for unanticipated use cases as requirements change (this is closely related to simplicity as easy to understands systems are usually easier to modify than complex ones).