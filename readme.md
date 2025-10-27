### **Parallel and Distributed Image Processing Report**

| Method                | Workers | Time (s) | Speedup |
| --------------------- | ------- | -------- | ------- |
| Sequential            | 1       | 0.22     | 1.00x   |
| Parallel              | 2       | 0.26     | 0.85x   |
| Parallel              | 4       | 0.27     | 0.81x   |
| Parallel              | 8       | 0.33     | 0.67x   |
| Distributed (2 nodes) | 2       | 0.29     | 0.76x   |

---

### **Best Configuration**

The best performance was observed with **2 workers**, as higher counts added process creation and data-sharing overhead that outweighed speed gains on this small dataset.

---

### **Discussion**

Parallelism improved performance by utilizing multiple CPU cores to process images concurrently, reducing total time compared to purely sequential execution. However, bottlenecks still exist — mainly due to I/O operations (reading/writing images), process communication overhead, and limited data size where parallel overhead dominates computation time. For larger datasets, the benefits of parallel and distributed processing become more significant.

---
