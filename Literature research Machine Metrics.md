---
tags: [literature]
title: 'Literature research: Machine Metrics'
created: '2019-10-01T16:19:19.201Z'
modified: '2019-10-07T08:14:40.466Z'
---

# Literature research: Machine Metrics
**Author**: Tycho Atsma
**Date**: September 30th, 2019

## About
This document contains a series of summaries of papers. The subject of these papers ~~should be~~ is related to machine metrics. The summaries should present new insights into machine metrics, improving its understanding.

## Papers
This section contains a series of potentially valuable papers and a series of valuable papers, where each paper is summarized.

### Kotarba, M. (2017). Measuring digitalization–key metrics. _Foundations of Management_, _9_(1), 123-138.
Kotorba tries to measure digitalization in various industries through a set of submeasurements done on metrics in commonly found in those industries. Such an industry can be the banking sector. He devides those metrics into a couple of categories, where the most relevant cateogory is: *Digital Client Metrics*. He mentions a number of KPIs specific to the banking sectors where one of them defines usages of online solutions:
- usage of online solutions:
  - logins per day/month (time of day analysis,
  session duration),
  - number/volume of transactions per session/in time series,
  - customer login journey (origination patterns),
  - most frequently used functionalities,
  - hardware technological platform used, with
  change history (iOS, Android, Windows),
  - software platform used (system, browser, type),
  - origination IP for security tracking purposes.

### Pandis, I., Johnson, R., Hardavellas, N., & Ailamaki, A. (2010). Data-oriented transaction execution. _Proceedings of the VLDB Endowment_, _3_(1-2), 928-939.
This paper is focused on stressing systems with a high workload using different benchmarking systems. These benchmarks can be identified with TPC-[A-C]. These benchmarks are a way to measure the stress levels on transactional systems. In the paper, they state they have developed their own prototype, DORA, to experiment with some multithreaded parallel system. This system does not look to be very useful related to our research.

They do, however, mention a benchmark, TCP-B, which seems to be something that we can use. In section 5.1 under **workloads** they mention the following:
> TPC-B models  a  bank  where  customers  deposit  and  withdraw  from their accounts.

The website of the TPC organization defines the benchmark as follows:
> TPC Benchmark B is designed to be a stress test on the core portion of a database system. It focuses in on the portion of a system which performs the actual transaction processing, much like a magnifying glass.


## Potentially valuable
- Fenton, N., & Bieman, J. (2014).  _Software metrics: a rigorous and practical approach_. CRC press.
- Kotarba, M. (2017). Measuring digitalization–key metrics. _Foundations of Management_, _9_(1), 123-138.
- Pandis, I., Johnson, R., Hardavellas, N., & Ailamaki, A. (2010). Data-oriented transaction execution. _Proceedings of the VLDB Endowment_, _3_(1-2), 928-939.
- Nicola, M., Kogan, I., & Schiefer, B. (2007, June). An XML transaction processing benchmark. In _Proceedings of the 2007 ACM SIGMOD international conference on Management of data_ (pp. 937-948). ACM.
- Jeong, E., Wood, S., Jamshed, M., Jeong, H., Ihm, S., Han, D., & Park, K. (2014). mTCP: a Highly Scalable User-level {TCP} Stack for Multicore Systems. In _11th {USENIX} Symposium on Networked Systems Design and Implementation ({NSDI} 14)_ (pp. 489-502).
- Alonso, G., Agrawal, D., El Abbadi, A., Kamath, M., Gunthor, R., & Mohan, C. (1996, February). Advanced transaction models in workflow contexts. In _Proceedings of the Twelfth International Conference on Data Engineering_ (pp. 574-581). IEEE.
- Barford, P., & Crovella, M. (2000). Critical path analysis of TCP transactions. _ACM SIGCOMM Computer Communication Review_, _30_(4), 127-138.


