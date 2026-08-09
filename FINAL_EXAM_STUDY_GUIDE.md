# BCPS 425: PARALLEL AND DISTRIBUTED COMPUTING — ULTIMATE EXAM STUDY GUIDE
*Sunyani Technical University (STU) | Faculty of Applied Science & Technology*

---

## 📌 QUICK EXAM CHECKLIST (12 Core Exam Topics)
- [x] **HPC & Parallel Architecture**: Speedup, Amdahl's Law, Flynn's Taxonomy (SISD, SIMD, MISD, MIMD).
- [x] **3-Tier & Client-Server**: Presentation (Tier 1), Business Logic (Tier 2), Data Layer (Tier 3).
- [x] **Concurrency & Race Conditions**: Critical Sections, Race conditions, The Lost Update Problem & remedies.
- [x] **Deadlocks**: 4 Coffman Conditions, Deadlock Prevention, Avoidance (Banker's Algorithm), Detection & Recovery.
- [x] **CPU Scheduling**: Round Robin (RR - fair, time quantum) vs. Shortest Job First (SJF - minimum wait, starvation risk).
- [x] **Distributed Operating Systems (DOS)**: DOS vs. Network OS (NOS), Transparencies (Location, Access, Replication, Failure).
- [x] **Network Protocols & IPC**: TCP (reliable, connection-oriented) vs. UDP (lightweight, connectionless), Sockets.
- [x] **Remote Method Invocation (Java RMI)**: Remote Interface, Remote Object, Stub (client proxy), Skeleton/Server, RMI Registry (`Naming.rebind`, `Naming.lookup`).
- [x] **Cloud Computing & Virtualization**: IaaS, PaaS, SaaS, Hypervisors/VMs, Containers (Docker/Kubernetes).
- [x] **Distributed Security & Fault Tolerance**: Authentication vs Authorization vs Encryption; Active vs Passive Redundancy.
- [x] **Official Textbook Q&A Bank**: Extracted Coulouris exercises (Idempotence, RMI semantics, CORBA CDR vs XML).
- [x] **2023/2024 Solved Past Paper**: Complete solutions for all exam paper questions.

---

## MODULE 1: High Performance Computing (HPC) & Parallel Architectures

### 1. Definitions & Comparisons
* **Parallel Computing**: Multiple processors/cores within a single computer system executing sub-tasks concurrently to increase processing speed.
* **Distributed Computing**: Multiple autonomous computer systems connected over a network, coordinating via message passing to achieve a common goal.
* **High Performance Computing (HPC)**: Aggregation of processing power (supercomputers/clusters) to perform complex calculations at high speeds.

| Feature | Parallel Computing | Distributed Computing |
| :--- | :--- | :--- |
| **Physical Location** | Single machine / tightly coupled chassis | Networked computers across rooms/cities |
| **Memory Architecture** | Shared memory or ultra-fast bus | Distributed / private RAM per node |
| **Communication** | Shared memory variables, semaphores, locks | Message passing over network (TCP/IP, Sockets, RMI) |
| **Primary Goal** | High execution speed & throughput | Resource sharing, scalability, fault tolerance |

### 2. Flynn's Taxonomy
* **SISD**: Single Instruction, Single Data (Legacy single-core PC).
* **SIMD**: Single Instruction, Multiple Data (Vector processors, modern GPUs processing data arrays in parallel).
* **MISD**: Multiple Instruction, Single Data (Rare; used in fault-tolerant flight controls).
* **MIMD**: Multiple Instruction, Multiple Data (Multi-core CPUs, distributed clusters, supercomputers).

### 3. Speedup & Amdahl's Law
* **Speedup**: \( S(p) = \frac{T_1}{T_p} \)
* **Amdahl's Law**: 
  \[ S(p) = \frac{1}{(1-f) + \frac{f}{p}} \]
  where \(f\) is the parallelizable fraction and \((1-f)\) is the strictly sequential portion.

---

## MODULE 2: 3-Tier & Client-Server Architecture

### 1. The 3 Tiers
1. **Tier 1 (Presentation Layer)**: Client UI (Web browser, Mobile app, Desktop GUI).
2. **Tier 2 (Application / Business Logic Layer)**: Application server handling business rules, authorization, and data processing.
3. **Tier 3 (Data Layer)**: Database Management System (DBMS) or Cloud storage (MySQL, PostgreSQL, S3).

### 2. Benefits of 3-Tier Architecture
* **Scalability**: Application servers can scale horizontally without touching the database schema.
* **Maintainability**: Business logic can be updated without re-deploying or modifying client UI code.
* **Security**: Database is completely isolated on a private subnetwork, shielded from direct public internet calls.

---

## MODULE 3: Concurrency, Race Conditions & The Lost Update Problem

### 1. Definitions
* **Concurrency**: Multiple threads or processes executing in overlapping time intervals.
* **Critical Section**: Code section accessing shared resources that must not be concurrently accessed by more than one process.
* **Race Condition**: System output depends unpredictably on execution timing/sequence.

### 2. The Lost Update Problem (Classic Exam Scenario)
Occurs when two concurrent transactions read the same data item, modify it locally, and write back. The second write overwrites the first user's update.

**Example (Airline Seat Booking)**:
1. Seat `22F` status is `AVAILABLE`.
2. User A reads `22F` (`AVAILABLE`).
3. User B reads `22F` (`AVAILABLE`).
4. User A books and writes `BOOKED BY A` to `22F`.
5. User B writes `BOOKED BY B` to `22F` (overwriting A's write).
6. **Result**: User A's update is **permanently lost**; double-booking occurs!

**Remedies**:
* **Pessimistic Locking**: `SELECT ... FOR UPDATE` (locks row before reading).
* **Optimistic Concurrency Control**: Versioning timestamps (`WHERE version = 1`).

---

## MODULE 4: Deadlocks (Coffman Conditions & Strategies)

### 1. The 4 Coffman Conditions (All 4 MUST hold for deadlock to occur)
1. **Mutual Exclusion**: Non-shareable resource (only 1 process at a time).
2. **Hold and Wait**: Process holds a resource while waiting for additional resources.
3. **No Preemption**: Resources cannot be forcibly taken away; must be released voluntarily.
4. **Circular Wait**: Closed loop of processes where \(P_0 \rightarrow P_1 \rightarrow P_2 \rightarrow P_0\).

### 2. Deadlock Handling Strategies
* **Prevention**: Structural rules breaking at least one Coffman condition (e.g. enforce total ordering on resource allocation to prevent Circular Wait).
* **Avoidance**: Dynamic evaluation of resource allocation state to ensure system remains in a **Safe State** (e.g. Dijkstra's **Banker's Algorithm**).
* **Detection & Recovery**: Allow deadlocks, periodically check Wait-For graph for cycles, and recover by **victim selection** (terminating a process or rolling back a transaction).

---

## MODULE 5: CPU Scheduling Algorithms (Round Robin vs SJF)

### Comparison Table
| Criteria | Round Robin (RR) | Shortest Job First (SJF) |
| :--- | :--- | :--- |
| **Mechanism** | Process gets fixed time slice (**quantum** \(q\)) in FIFO queue | Process with shortest CPU burst time runs first |
| **Primary Metric** | Responsiveness & Fairness | Minimum Average Waiting Time / Maximum Throughput |
| **Preemptive?** | Yes (quantum enforced) | Non-preemptive (SRTF is preemptive version) |
| **Starvation Risk** | **Zero starvation** | **High starvation risk** for long jobs |
| **Best Used For** | Interactive time-sharing systems | Predictable batch processing workloads |

---

## MODULE 6: Distributed Operating Systems (DOS) & Protocols

### 1. DOS vs. Network Operating System (NOS)
* **DOS**: Presents a **single-system image** across multiple machines. Location of processors and RAM is completely transparent.
* **NOS**: Collection of standalone autonomous computers on a network (users are aware of distinct machine locations).

### 2. System Transparencies
* **Access Transparency**: Local and remote resources accessed using identical operations.
* **Location Transparency**: Accessing resources without knowing physical network location.
* **Replication Transparency**: Multiple resource copies managed without user awareness.
* **Failure Transparency**: Hiding faults so system recovers automatically.

### 3. Transport Protocols
* **TCP**: Connection-oriented, reliable, ordered stream, flow control.
* **UDP**: Connectionless, lightweight, unordered, zero overhead (ideal for video/audio streaming).

---

## MODULE 7: Remote Method Invocation (Java RMI)

### 1. Java RMI Architecture
* **Remote Interface (RI)**: Interface extending `java.rmi.Remote`; methods declare `throws RemoteException`.
* **Remote Object**: Class implementing RI and extending `UnicastRemoteObject`.
* **Client Stub**: Client-side proxy object that marshals parameters and sends network requests.
* **Server Skeleton**: Unmarshals incoming parameters and calls actual remote object method.
* **RMI Registry**: Naming service mapping lookup strings to remote objects (`Naming.rebind`, `Naming.lookup`).

### 2. Essential Java RMI Code Template
```java
// 1. Remote Interface
import java.rmi.Remote;
import java.rmi.RemoteException;

public interface ComputeService extends Remote {
    int add(int a, int b) throws RemoteException;
}

// 2. Implementation
import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;

public class ComputeServiceImpl extends UnicastRemoteObject implements ComputeService {
    public ComputeServiceImpl() throws RemoteException { super(); }
    public int add(int a, int b) throws RemoteException { return a + b; }
}

// 3. Server Registration
import java.rmi.Naming;
import java.rmi.registry.LocateRegistry;

public class Server {
    public static void main(String[] args) {
        try {
            LocateRegistry.createRegistry(1099);
            Naming.rebind("rmi://localhost:1099/ComputeService", new ComputeServiceImpl());
            System.out.println("RMI Server Running.");
        } catch (Exception e) { e.printStackTrace(); }
    }
}

// 4. Client Invocation
import java.rmi.Naming;

public class Client {
    public static void main(String[] args) {
        try {
            ComputeService service = (ComputeService) Naming.lookup("rmi://localhost:1099/ComputeService");
            System.out.println("Result: " + service.add(10, 20));
        } catch (Exception e) { e.printStackTrace(); }
    }
}
```

---

## MODULE 8: Cloud Computing & Distributed Security / Fault Tolerance

### 1. Service Models
* **IaaS**: Infrastructure as a Service (AWS EC2, Compute Engine).
* **PaaS**: Platform as a Service (Heroku, Elastic Beanstalk).
* **SaaS**: Software as a Service (Google Drive, Gmail, Office 365).

### 2. Security Pillars
* **Authentication**: Verifying identity (Passwords, 2FA, Certificates).
* **Authorization**: Verifying permissions (Role-Based Access Control).
* **Encryption**: Protecting confidentiality (TLS/HTTPS in transit, AES-256 at rest).

---

## MODULE 9: OFFICIAL TEXTBOOK Q&A BANK (Coulouris et al.)

### Q1: What is the difference between Maybe, At-Least-Once, and At-Most-Once RMI Invocation Semantics?
* **Maybe**: No retransmissions on failure; call executes **0 or 1 time**.
* **At-Least-Once**: Retransmits on timeout until reply received; call executes **1 or more times** (safe for idempotent operations).
* **At-Most-Once**: Retransmits on timeout, but server uses duplicate history filter; call executes **0 or 1 time**.

### Q2: Is Appending data to a file Idempotent?
* **Answer**: **No.** Appending extends file length on every execution. Writing to a *fixed offset* or pressing an elevator call button IS idempotent.

### Q3: Why does CORBA CDR lack explicit data-type tags compared to XML?
* **Answer**: CORBA CDR relies on compiled Interface Definition Language (IDL) files shared by client and server. Data types and order are known in advance, allowing compact binary payloads with zero tag overhead. XML is self-describing, carrying textual tags for every element.

---

## MODULE 10: SOLVED 2023/2024 PAST EXAM PAPER (STU BCPS 425)

### Q1(a): State 3 contrasting examples of heterogeneity in distributed systems. (6 Marks)
1. **Hardware & Processors**: x86_64 vs ARM64 vs SIMD GPUs (differ in byte ordering, word size).
2. **Operating Systems**: Linux vs Windows vs macOS (differ in system calls, scheduling, file systems).
3. **Languages & Middleware**: Java RMI vs Python REST APIs vs C++ gRPC (differ in runtime & data types).

### Q1(b): Synchronization requirements for Web Crawlers vs Search Tasks. (4 Marks)
1. **Reader-Writer Locking**: Search tasks (Readers) execute concurrently; crawler index updates (Writers) write without corrupting reader memory.
2. **Atomic Index Swapping**: Crawlers update an offline index copy, then atomically swap pointers to make it live instantly without blocking query threads.

### Q1(c): Service A vs Service B Failure Classes & Reliability. (6 Marks)
* **Service A**: Omission failures, Timing failures, and Arbitrary Payload Corruption (checksum only on headers).
* **Service B**: Omission failures (buffer overflow / delivered too fast) and Timing failures.
* **Is Service B Reliable?** **No**, because dropped messages are not retransmitted or acknowledged.

### Q1(d): Invocation Failure Classes for Client X and Server Y over Service B. (4 Marks)
1. Request message omission failure.
2. Server Y crash / execution failure.
3. Reply message omission failure.
4. Invocation timing failure (timeout).

### Q2(i): How Internet Routing handles massive network scale. (4 Marks)
1. **Autonomous Systems (AS) & Default Routing**: Local routers only store internal subnet routes; external traffic goes to Default Gateways / Border Routers.
2. **CIDR IP Prefix Aggregation**: Hierarchical subnet grouping (`192.168.0.0/16`) condenses millions of host addresses into single routing table entries.

### Q2(ii): 5-Layer Internet Protocol Stack Table (10 Marks)
* **Application**: HTTP, DNS, Java RMI (User formats & protocols).
* **Transport**: TCP, UDP (End-to-end ports, process addressing, retransmission).
* **Network**: IP, ICMP (Packet routing, IP addressing).
* **Data Link**: Ethernet MAC (Frames, physical MAC addresses, error checking).
* **Physical**: Ethernet Cables, Radio Waves (Bits transmission).

### Q3(a): Parallel vs Distributed Computing Table (8 Marks)
| Feature | Parallel Computing | Distributed Computing |
| :--- | :--- | :--- |
| **Architecture** | Single machine with multiple cores | Multiple networked autonomous machines |
| **Memory** | Shared Memory | Distributed / Private RAM per machine |
| **Communication** | Shared memory variables & locks | Message passing (Sockets, TCP/IP, RMI) |
| **Fault Tolerance** | Single failure stops system | High fault tolerance (nodes fail independently) |

### Q3(e): Web Service Architectural Pattern (2 Marks)
* **Components**: Service Provider, Service Requester (Client), Service Registry (UDDI).
* **Flow**: Provider publishes WSDL to Registry -> Requester looks up service -> Requester binds & invokes SOAP/REST API on Provider.

---

## 🎯 FINAL MULTIPLE-CHOICE QUIZ FOR EXAM DAY

1. **In Flynn's Taxonomy, GPUs belong to which class?**
   - [ ] SISD
   - [x] **SIMD**
   - [ ] MISD
   - [ ] MIMD

2. **Which Coffman condition is broken by enforcing a global ordering on resource requests?**
   - [ ] Mutual Exclusion
   - [ ] Hold and Wait
   - [ ] No Preemption
   - [x] **Circular Wait**

3. **Which CPU scheduling algorithm minimizes average waiting time?**
   - [ ] Round Robin
   - [x] **Shortest Job First (SJF)**
   - [ ] Priority Scheduling
   - [ ] First-Come First-Served

4. **Which object acts as the client-side proxy in Java RMI?**
   - [x] **Stub**
   - [ ] Skeleton
   - [ ] Registry
   - [ ] Dispatcher

5. **In a 3-tier system, where does application business logic reside?**
   - [ ] Presentation Layer
   - [x] **Application Layer (Tier 2)**
   - [ ] Data Layer
   - [ ] Client Browser
