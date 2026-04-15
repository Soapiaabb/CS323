
### Member 1 — Saculinggan, Alfer L. 

In this activity, We compare and I noticed how sorting works when done normal (sequential) and when it done in parallel. I noticed that sequential execution process the data step by step, so it takes longer, especially when the data is big. In parallel execution, the work is split into smaller parts and done at the same time, so it can be faster. But for small data, the difference is not really obvious because splitting and combining also take time.

When we test different data sizes, I noticed that small data is sorted very fast even without parallel. Medium data takes more time but still okay to handle. For big data, the time increase a lot, which show that sorting really depends on how big the data is. Merge sort works well in all cases, even if the data is already sorted or reversed, because it always divide the data the same way.

One challenge I encounter is understanding how the algorithm split the list and merge it back correctly. It also a bit confusing to follow how the data move during recursion. If using parallel, it can be more hard because you need to make sure all parts finish first before merging.

I also learned that there is extra work when using parallel processing, like handling many tasks and combining results. Sometimes this make it slower instead of faster, especially for small inputs. So parallel is not always the best choice.

Overall, parallel is helpful when dealing with very big data because it can reduce the total time. But for small data, using simple sequential is already enough and sometimes better because it avoid extra work.

---

### Member 2 — Villarente, Sofia Belle S. 

In our activity, I split the data into smaller parts by dividing the list evenly based on the number of processes. Each part was handled by a separate process, allowing them to sort at the same time, which improved speed for larger datasets.

The challenge I faced was combining the sorted parts into one correctly ordered list. Even though each chunk was already sorted, merging them while keeping the overall order was not easy and required careful steps.

The queue was used to gather the sorted results from each process. It served as a safe way to transfer data between processes so the results could be collected and merged afterward.

I also observed some extra overhead when using multiprocessing. Starting processes, managing them, and merging results added more work, which sometimes made it slower than sequential sorting for small datasets. Overall, multiprocessing is useful for large data but adds complexity and extra cost.

---

### Member 3 — Glanida, Ravien B.

In our activity, I concentrated mainly on the parallel search and could see some obvious differences between this type of search and sequential search. The main difference is that parallel search works with several processes simultaneously, thus allowing to accelerate the process significantly while working with a large number of data – such as 1,000,000 elements. 

When applied to small amounts of data, however, parallel search is less effective due to the necessity to spend additional time on creating processes. Thus, in many cases, the use of this search algorithm leads to worse performance in comparison with sequential one. This experience made me realize that parallel search is highly efficient only when working with a significant amount of data. 

Therefore, it can be recommended when processing large datasets, while small amounts of data do not require it. In terms of implementing this approach, the key challenges I have faced are related to splitting data into equal shares and collecting the results after the search process is over. Moreover, it is rather problematic to coordinate and synchronize the operation of several processes.

---

### Member 4 — Usman, Mark Jason B.

In this activity I saw the difference between doing things one after another and doing things at the time using searching and sorting algorithms. Doing things one after another is easier. Only uses one process but it gets slower when the data gets really big. Doing things at the time is faster for big data because it breaks the data into smaller pieces and works on them all at once using many processes but it also adds some extra work.

The speed was different depending on how data there was. For amounts of data doing things one after another was sometimes faster or just as fast because doing things at the same time has extra work like starting processes and talking between them. But for amounts of data parallel merge sort was faster because the work is split across many CPU cores so it finishes faster.

One hard part I had was getting the processes to talk to each other using queues. I need to make sure each process sends back the sorted data and everything is collected in the right order before putting it all together. Another hard part is making sure the last step still keeps the result sorted correctly even when combining many parts.

I also learned that extra work and synchronization really affect doing things at the time. If doing things at the same time is faster for big jobs it can be slow for small datasets because starting processes and putting results together takes extra time.

Overall doing things at the time is more useful when the data is big and can be broken into pieces while doing things one after another is better, for small data because it is easier and does not have extra work.

---

### Member 5 — Pulpul, Jealry E.

In this activity, I try to compare sorting when it is done one by one (sequential) and when it is done at the same time (parallel). I observe that sequential method go step by step, so it become slower when the data is already big. While in parallel, the task is divided and processed together, so it makes it faster. But if the data is small, you can’t really see much difference because the extra steps also takes time.

While testing different sizes, I notice that small data is very fast to sort even without using parallel. The medium size take a bit longer but still fine. When the data is large, it really take more time, so it shows that size of data really affects the performance. Merge sort still perform good in all cases, even if the data is already sorted or in reverse, because it divide the list the same way always.

One problem I experience is understanding how the list is being divided and then combined again properly. It is also confusing sometimes to follow the flow of data because of recursion. If parallel is applied, it become more complicated since you need to wait all parts to finish before combining them.

I also realize that parallel processing have extra work like handling multiple tasks and merging results. Because of that, it can sometimes be slower instead of faster, especially when the input is small. So parallel is not always useful.

In general, parallel is better when working with very large data since it reduce the time needed. But for small data, doing it sequential is already okay and sometimes even better because there is no extra overhead.

---

### Benchmark GIF

![](benchmark.gif)

---
