---
tags:
  - ddia/glossary
  - cheat-sheet
date: 2026-11-21
---

# Chapter 13: Glossary (cheat sheet)

> [!abstract] Summary
> The book's glossary gives short definitions of recurring terms. This sheet regroups them by theme, with a one-line meaning and the main chapter to revisit. The book itself warns the definitions are simplified, so follow the references for subtleties.

## Data models and storage

| Term | Meaning | Revisit |
|---|---|---|
| **schema** | structure of data (fields, types); can be checked at write or read time and can evolve | Ch. 2, 4 |
| **graph** | vertices (nodes, entities) plus edges (relationships, arcs) | Ch. 2 |
| **index** | structure for finding all records with a given field value | Ch. 3 |
| **secondary index** | extra structure beside primary storage for other conditions | Ch. 3, 6 |
| **full-text search** | arbitrary keyword search, fuzzy matching, synonyms; a kind of secondary index | Ch. 3 |
| **primary key** | unique record identifier, usually system generated | Ch. 3 |
| **normalized** | no duplication; change in one place | Ch. 2 |
| **denormalize** | add redundancy (cache, index, precomputed result) to speed reads, like a materialized view | Ch. 2, 11 |
| **cache** | remembers recent data for fast reads; incomplete, falls back to slower storage | Ch. 1 |
| **locality** | keep data used together in the same place | Ch. 2 |
| **hash** | function giving a random-looking, deterministic number; collisions possible | Ch. 6 |
| **log** | append-only file: write-ahead log, log-structured engine, replication log, event log | Ch. 3, 5, 11 |

## Analytics and derived data

| Term | Meaning | Revisit |
|---|---|---|
| **OLTP** | fast queries reading or writing few records by key | Ch. 3 |
| **OLAP** | aggregates (count, sum, average) over many records | Ch. 3 |
| **data warehouse** | combined, prepared data from several OLTP systems for analytics | Ch. 3 |
| **ETL** | extract, transform, load into a warehouse or batch system | Ch. 3, 10 |
| **derived data** | produced from other data by a repeatable process (indexes, caches, materialized views) | Part III |
| **system of record** | authoritative source of truth; others are derived from it | Part III |
| **materialize** | compute eagerly and store, instead of on demand | Ch. 3, 10 |
| **batch process** | fixed input, produces output, does not modify the input | Ch. 10 |
| **stream process** | continuous computation over a never-ending event stream | Ch. 11 |
| **join** | bring together records sharing something, e.g., via foreign key | Ch. 2, 10 |
| **declarative** | state wanted properties, not steps; optimizer picks the plan | Ch. 2 |
| **stored procedure** | transaction logic executed entirely on the DB server | Ch. 7 |

## Scaling and replication

| Term | Meaning | Revisit |
|---|---|---|
| **replication** | same data on several nodes (replicas) | Ch. 5 |
| **leader** | replica allowed to accept writes (primary, master) | Ch. 5 |
| **follower** | replica that only applies the leader's changes (secondary, slave, read replica, hot standby) | Ch. 5 |
| **failover** | moving leadership to another node | Ch. 5 |
| **split brain** | two nodes both believe they are leader; breaks guarantees | Ch. 5, 8 |
| **partitioning** | splitting data or work across machines (sharding) | Ch. 6 |
| **rebalance** | moving data or services between nodes to even out load | Ch. 6 |
| **skew** | (1) uneven load across partitions (hot spots); (2) timing anomaly: read skew, write skew, clock skew | Ch. 6, 7, 8 |
| **shared-nothing** | independent nodes with own CPU, memory and disk over a normal network | Part II |
| **quorum** | minimum number of votes for an operation to count | Ch. 5 |
| **percentile** | value below which a given share of observations fall (p95 = 95% faster) | Ch. 1 |

## Transactions and concurrency

| Term | Meaning | Revisit |
|---|---|---|
| **transaction** | group of reads and writes as one logical unit | Ch. 7 |
| **atomic** | (1) concurrent: appears to happen at one instant; (2) transactional: all writes commit or all roll back | Ch. 7 |
| **isolation** | degree concurrent transactions can interfere | Ch. 7 |
| **serializable** | behaves as if transactions ran one at a time | Ch. 7 |
| **durable** | believed not to be lost despite faults | Ch. 7 |
| **lock** | mutual exclusion: others wait until released | Ch. 7, 8 |
| **two-phase locking (2PL)** | lock everything read or written, hold until transaction end; gives serializability | Ch. 7 |
| **two-phase commit (2PC)** | all nodes commit or all abort | Ch. 9 |
| **idempotent** | safe to retry; repeated execution has the same effect as once | Ch. 11 |
| **deterministic** | same input always gives the same output (no randomness, clock, network) | Ch. 11, 12 |

## Distributed systems and faults

| Term | Meaning | Revisit |
|---|---|---|
| **distributed** | multiple nodes over a network; partial failures, unclear what is broken | Ch. 8 |
| **node** | an instance of software on a computer communicating over a network | Ch. 8 |
| **fault-tolerant** | recovers automatically from machine or link failures | Ch. 1 |
| **timeout** | simplest fault detector; cannot tell node failure from network problem | Ch. 8 |
| **Byzantine fault** | node behaves arbitrarily wrong or maliciously | Ch. 8 |
| **synchronous / asynchronous** | waiting for completion vs not waiting and assuming nothing about duration | Ch. 5, 8 |
| **bounded / unbounded** | known upper limit on size or delay, or none | Ch. 8, 11 |
| **backpressure** | slowing the sender because the receiver cannot keep up (flow control) | Ch. 11 |

## Consistency and ordering

| Term | Meaning | Revisit |
|---|---|---|
| **linearizable** | behaves as if one copy updated atomically | Ch. 9 |
| **causality** | dependency from "happens before": responses, builds-upon | Ch. 5, 9 |
| **total order** | any two items comparable; a *partial order* leaves some incomparable | Ch. 9 |
| **consensus** | getting nodes to agree (e.g., on a leader); harder than it looks | Ch. 9 |
| **CAP theorem** | the book calls it widely misunderstood and not useful in practice | Ch. 9 |

## Quick recall

- Many terms come in pairs: OLTP/OLAP, normalized/denormalized, leader/follower, bounded/unbounded, synchronous/asynchronous.
- "Derived data" plus "system of record" frame Part III; "log" is the unifying structure across storage, replication and streams.
- Idempotent and deterministic are the keys to safe retries and replay.
- "Skew" and "atomic" each have two meanings; read context.
