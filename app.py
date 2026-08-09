import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random

# Page Configuration
st.set_page_config(
    page_title="BCPS 425: Parallel & Distributed Computing Companion",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
    <style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #0284c7, #6366f1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    .sub-title {
        color: #64748b;
        font-size: 1rem;
        margin-bottom: 20px;
    }
    .highlight-box {
        background-color: #1e1b4b;
        border-left: 4px solid #6366f1;
        padding: 15px 20px;
        border-radius: 8px;
        margin: 15px 0;
        color: #e2e8f0;
    }
    .quiz-card {
        background-color: #0f172a;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("🎓 Course Navigation")
st.sidebar.caption("Sunyani Technical University (STU) — BCPS 425")

page = st.sidebar.radio(
    "Select Module or Tool:",
    [
        "🏠 Home & Course Overview",
        "📡 Distributed APIs & Message Passing (MPI, Sockets, IPC)",
        "⚡ Amdahl's Law & Speedup Calculator",
        "🔒 Deadlock & Coffman Conditions Simulator",
        "🔄 CPU Scheduling Simulator (RR vs SJF)",
        "☕ Java RMI & RPC Architecture Explorer",
        "🌐 Distributed Algorithms & Protocols (2PC, Election, Clocks)",
        "💡 Textbook Q&A Bank (Coulouris)",
        "📝 STU 2023/2024 Solved Past Exam Paper",
        "🧠 40-Question Practice Quiz Engine (10 Sets)"
    ]
)

# ----------------------------------------------------
# 40-QUESTION MCQ QUESTION BANK
# ----------------------------------------------------
MCQ_BANK = [
    # Set 1: Parallel & HPC
    {"q": "1. In Flynn's Taxonomy, modern Graphics Processing Units (GPUs) belong to which classification?", "opts": ["SISD", "SIMD", "MISD", "MIMD"], "ans": 1, "exp": "GPUs execute a Single Instruction across Multiple Data streams simultaneously (SIMD)."},
    {"q": "2. What limits the theoretical maximum speedup according to Amdahl's Law even with infinite processors?", "opts": ["Number of cores", "The strictly sequential fraction (1 - f)", "Network latency", "RAM size"], "ans": 1, "exp": "Amdahl's Law proves speedup S(p) is capped at 1/(1-f) by the serial fraction."},
    {"q": "3. Which parallel architecture features shared memory accessible by all processors in a single machine?", "opts": ["Tightly Coupled / SMP", "Distributed Memory Cluster", "Grid System", "Peer-to-Peer"], "ans": 0, "exp": "Symmetric Multiprocessing (SMP) uses shared physical RAM across processors."},
    {"q": "4. What is the formula for speedup S(p) given execution time T1 on 1 processor and Tp on p processors?", "opts": ["S(p) = T1 * Tp", "S(p) = T1 / Tp", "S(p) = Tp / T1", "S(p) = T1 + Tp"], "ans": 1, "exp": "Speedup is defined as execution time on 1 core divided by execution time on p cores."},

    # Set 2: 3-Tier Architecture
    {"q": "5. In a 3-tier architecture, where is the primary business logic implemented?", "opts": ["Presentation Layer (Tier 1)", "Application Layer (Tier 2)", "Data Layer (Tier 3)", "Client Web Browser"], "ans": 1, "exp": "Tier 2 contains the application servers executing business logic and rules."},
    {"q": "6. Which layer in a 3-tier system directly handles database persistence?", "opts": ["Presentation Layer", "Logic Layer", "Data Layer (Tier 3)", "Session Layer"], "ans": 2, "exp": "Tier 3 consists of RDBMS or cloud storage storing persistent data."},
    {"q": "7. What is a key security advantage of 3-tier architecture over 2-tier architecture?", "opts": ["No passwords needed", "Database is isolated on a private subnet behind app servers", "Client handles encryption", "Removes TCP/IP"], "ans": 1, "exp": "The database is shielded from direct public internet calls by Tier 2 servers."},
    {"q": "8. Web service registration and lookup in SOAP architectures uses which specification?", "opts": ["WSDL", "UDDI", "REST", "JSON"], "ans": 1, "exp": "Universal Description, Discovery and Integration (UDDI) acts as the service registry."},

    # Set 3: Concurrency & Lost Update
    {"q": "9. What causes the Lost Update Problem in concurrent applications?", "opts": ["Unencrypted traffic", "Two transactions reading identical data and both writing back", "Network disconnection", "Deadlock avoidance"], "ans": 1, "exp": "The second transaction overwrites the first transaction's modifications."},
    {"q": "10. Which locking strategy acquires exclusive locks on data before reading or updating?", "opts": ["Optimistic Concurrency Control", "Pessimistic Locking", "Round Robin", "Bully Algorithm"], "ans": 1, "exp": "Pessimistic locking uses SELECT ... FOR UPDATE to lock rows during reading."},
    {"q": "11. A section of code that accesses shared resources and must not be concurrently executed is called:", "opts": ["Critical Section", "Deadlock Zone", "Parallel Region", "Buffer Queue"], "ans": 0, "exp": "Critical Sections require mutual exclusion to prevent data corruption."},
    {"q": "12. Optimistic Concurrency Control handles conflicts using:", "opts": ["Exclusive locks", "Version numbers or timestamps", "Process termination", "CPU quantum"], "ans": 1, "exp": "Optimistic control checks if version numbers changed before committing."},

    # Set 4: Deadlocks
    {"q": "13. How many Coffman conditions must hold simultaneously for a deadlock to exist?", "opts": ["At least 1", "Exactly 2", "Exactly 3", "All 4"], "ans": 3, "exp": "All 4 Coffman conditions must hold simultaneously for a deadlock to occur."},
    {"q": "14. Which deadlock strategy breaks a Coffman condition structurally before execution?", "opts": ["Deadlock Avoidance", "Deadlock Prevention", "Deadlock Recovery", "Victim Selection"], "ans": 1, "exp": "Prevention enforces rules (e.g. global resource ordering) to eliminate a condition."},
    {"q": "15. Dijkstra's Banker's Algorithm is an example of which deadlock handling approach?", "opts": ["Deadlock Prevention", "Deadlock Avoidance", "Deadlock Detection", "Preemption"], "ans": 1, "exp": "Avoidance dynamically evaluates requests to guarantee the system stays in a Safe State."},
    {"q": "16. Circular Wait is eliminated by enforcing which resource policy?", "opts": ["Preemption", "Total numeric ordering on resource requests", "Unlimited RAM", "Time slicing"], "ans": 1, "exp": "Requiring processes to request resources in strictly increasing order prevents cycles."},

    # Set 5: CPU Scheduling
    {"q": "17. Which scheduling algorithm guarantees zero starvation for all processes?", "opts": ["Shortest Job First (SJF)", "Priority Scheduling", "Round Robin (RR)", "LIFO"], "ans": 2, "exp": "Round Robin assigns a fixed quantum in FIFO order, preventing starvation."},
    {"q": "18. Shortest Job First (SJF) scheduling is optimal for minimizing:", "opts": ["CPU utilization", "Average waiting time", "Context switches", "Starvation risk"], "ans": 1, "exp": "SJF mathematically yields the lowest average waiting time for a set of processes."},
    {"q": "19. Preemptive version of Shortest Job First is known as:", "opts": ["Round Robin", "Shortest Remaining Time First (SRTF)", "FCFS", "Multilevel Queue"], "ans": 1, "exp": "SRTF preempts the running process if a new process arrives with shorter remaining time."},
    {"q": "20. What is a major drawback of a very small time quantum in Round Robin scheduling?", "opts": ["Starvation", "High context-switching overhead", "Deadlock", "Long wait times"], "ans": 1, "exp": "Too small a quantum causes the CPU to waste time performing context switches."},

    # Set 6: Distributed OS & Transparencies
    {"q": "21. A Distributed Operating System (DOS) provides users with:", "opts": ["Multiple login prompts", "A single-system image", "Manual node IP configuration", "No file sharing"], "ans": 1, "exp": "DOS hides physical node separation, presenting a unified single system image."},
    {"q": "22. Accessing local and remote resources using identical operations is called:", "opts": ["Location Transparency", "Access Transparency", "Failure Transparency", "Replication Transparency"], "ans": 1, "exp": "Access transparency masks differences in data representation and resource access."},
    {"q": "23. Concealing resource physical network location from users is known as:", "opts": ["Location Transparency", "Migration Transparency", "Concurrency Transparency", "Relocation Transparency"], "ans": 0, "exp": "Location transparency allows accessing resources without knowing their IP or server path."},
    {"q": "24. Which transport protocol provides reliable, ordered stream delivery with flow control?", "opts": ["UDP", "IP", "TCP", "ICMP"], "ans": 2, "exp": "Transmission Control Protocol (TCP) guarantees reliable, in-order delivery."},

    # Set 7: Java RMI & Remote Invocation
    {"q": "25. Which object acts as the client-side proxy in Java RMI?", "opts": ["Skeleton", "Stub", "Registry", "Dispatcher"], "ans": 1, "exp": "The Stub intercepts client calls, marshals arguments, and transmits network requests."},
    {"q": "26. Methods defined in a Java RMI Remote Interface MUST declare which exception?", "opts": ["NullPointerException", "RemoteException", "ClassNotFoundException", "IOException"], "ans": 1, "exp": "Every remote method must throw java.rmi.RemoteException to handle network faults."},
    {"q": "27. In Java RMI, how are non-remote serializable object arguments passed?", "opts": ["By Reference", "By Value (Deep Copy)", "By Address", "By Pointer"], "ans": 1, "exp": "Non-remote objects implementing Serializable are copied and passed by value."},
    {"q": "28. What RMI invocation semantic guarantees 0 or 1 execution using reply history filtering?", "opts": ["Maybe", "At-Least-Once", "At-Most-Once", "Exactly-Never"], "ans": 2, "exp": "At-Most-Once filters duplicates at the server to execute at most once."},

    # Set 8: Distributed Algorithms
    {"q": "29. In the Bully Election Algorithm, which process becomes the new leader upon crash detection?", "opts": ["Process with the smallest ID", "Process with the highest ID", "Random process", "First process to respond"], "ans": 1, "exp": "The Bully algorithm elects the active process with the highest process ID."},
    {"q": "30. The Two-Phase Commit Protocol (2PC) guarantees which property in distributed transactions?", "opts": ["Eventual Consistency", "Atomicity (All-or-Nothing commit)", "High Availability", "Zero Latency"], "ans": 1, "exp": "2PC ensures all participating nodes either commit or abort the transaction together."},
    {"q": "31. Lamport Logical Clocks use logical timestamps to define which relationship between events?", "opts": ["Absolute Universal Time", "Happened-Before relation (->)", "CPU Clock Speed", "Round Trip Time"], "ans": 1, "exp": "Lamport timestamps establish partial ordering based on causality (a -> b)."},
    {"q": "32. In 2PC, what action does the Coordinator take if any participant responds with VOTE_ABORT?", "opts": ["Commit anyway", "Sends GLOBAL_ABORT to all nodes", "Waits 1 hour", "Terminates coordinator"], "ans": 1, "exp": "If any node votes abort, the coordinator enforces a global abort across all nodes."},

    # Set 9: Cloud & Security
    {"q": "33. Cloud service model providing virtualized compute, raw storage, and networking is:", "opts": ["SaaS", "PaaS", "IaaS", "FaaS"], "ans": 2, "exp": "Infrastructure as a Service (IaaS) supplies raw virtual machines and storage."},
    {"q": "34. Verifying the identity of a user or system is defined as:", "opts": ["Authorization", "Authentication", "Encryption", "Auditing"], "ans": 1, "exp": "Authentication verifies WHO a user is (e.g. passwords, 2FA)."},
    {"q": "35. Technology enabling multiple virtual machines with distinct OS instances on one physical host:", "opts": ["Hypervisor / Virtualization", "Compiler", "Load Balancer", "DNS"], "ans": 0, "exp": "Hypervisors (KVM, VMware) manage virtual machine hardware abstractions."},
    {"q": "36. Active Redundancy for fault tolerance differs from Passive Redundancy because:", "opts": ["All redundant nodes process requests in parallel", "Only 1 node is powered on", "Backup node takes 2 hours", "No backups used"], "ans": 0, "exp": "Active redundancy processes requests across all nodes simultaneously for instant failover."},

    # Set 10: Textbook & Code Scenarios
    {"q": "37. Is appending data to a file an idempotent operation?", "opts": ["Yes", "No", "Only on Linux", "Only with TCP"], "ans": 1, "exp": "No. Appending extends file length on each execution. Writing to a fixed offset IS idempotent."},
    {"q": "38. Why does CORBA CDR lack explicit data-type tags compared to XML?", "opts": ["XML is faster", "CORBA relies on pre-compiled IDL files shared by client and server", "CDR is text based", "XML has no tags"], "ans": 1, "exp": "Shared IDL schemas allow CORBA CDR to transmit compact binary data without type tags."},
    {"q": "39. What is the role of the RMI Registry in Java RMI applications?", "opts": ["Executes business logic", "Bootstrap naming lookup mapping strings to remote object stubs", "Encrypts network traffic", "Allocates CPU RAM"], "ans": 1, "exp": "The RMI Registry maps logical names (e.g. 'ComputeService') to remote stubs."},
    {"q": "40. In Ricart-Agrawala Mutual Exclusion Algorithm, requests are ordered using:", "opts": ["IP Addresses", "Lamport Timestamps & Process IDs", "CPU burst times", "File sizes"], "ans": 1, "exp": "Ricart-Agrawala uses Lamport timestamps to grant critical section access fairly."}
]

# ----------------------------------------------------
# PAGE 1: HOME
# ----------------------------------------------------
if page == "🏠 Home & Course Overview":
    st.markdown('<h1 class="main-title">BCPS 425: Parallel & Distributed Computing</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Sunyani Technical University (STU) — Department of Computer Science</p>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Course Code", "BCPS 425")
    c2.metric("Credits", "3 Credits")
    c3.metric("Exam Time", "2½ Hours")
    c4.metric("Total Marks", "60 Marks")

    st.markdown("---")
    st.subheader("📚 Module Breakdown & Exam Focus Areas")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.info("⚡ **Unit 1: HPC & Parallel Architecture**\n- Speedup, Amdahl's Law, Flynn's Taxonomy (SISD, SIMD, MIMD).")
        st.info("🏗️ **Unit 2: System Architectures & APIs**\n- 2-Tier vs 3-Tier, Web Services (WSDL, UDDI, REST), Message Passing (MPI, Sockets).")
        st.info("🔒 **Unit 3: Concurrency & Deadlocks**\n- Critical Sections, Lost Update Problem, 4 Coffman Conditions, Banker's Algorithm.")
        st.info("🔄 **Unit 4: Process Scheduling**\n- Round Robin (RR - quantum, fair) vs Shortest Job First (SJF - minimum wait time).")

    with col_b:
        st.success("☕ **Unit 5: Remote Method Invocation (Java RMI)**\n- Remote Interface, Remote Object, Client Stub, Server Skeleton, RMI Registry.")
        st.success("🌐 **Unit 6: Distributed Algorithms**\n- 2-Phase Commit (2PC), Bully Election Algorithm, Lamport Logical Clocks.")
        st.success("🌐 **Unit 7: Distributed OS & Protocols**\n- Single System Image, Transparencies (Access, Location), TCP vs UDP.")
        st.success("☁️ **Unit 8: Cloud Computing & Security**\n- IaaS, PaaS, SaaS, Virtualization, Authentication vs Authorization vs Encryption.")

# ----------------------------------------------------
# PAGE 2: DISTRIBUTED APIS & MESSAGE PASSING
# ----------------------------------------------------
elif page == "📡 Distributed APIs & Message Passing (MPI, Sockets, IPC)":
    st.title("📡 Distributed Application APIs & Message Passing Primitives")
    st.write("Understand APIs, interprocess communication (IPC) abstractions, and message passing paradigms used in parallel and distributed systems.")

    t_api1, t_api2, t_api3, t_api4 = st.tabs([
        "1. Distributed APIs (REST, gRPC, RMI, MPI)",
        "2. Message Passing Semantics (Sync vs Async)",
        "3. MPI (Message Passing Interface) for HPC",
        "4. Socket Programming API (TCP vs UDP)"
    ])

    with t_api1:
        st.subheader("APIs for Distributed Application Development")
        st.write("An **Application Programming Interface (API)** provides standard protocols and tools for software components to communicate across networks.")
        
        st.markdown("""
        | Distributed API | Transport Protocol | Data Format | Common Use Cases |
        | :--- | :--- | :--- | :--- |
        | **REST API** | HTTP / HTTPS | JSON, XML | Web applications, microservices, mobile backends |
        | **gRPC** | HTTP/2 | Protocol Buffers (Binary) | High-performance microservices, low-latency IPC |
        | **Java RMI** | JRMP / TCP | Serialized Java Objects | Object-oriented Java distributed applications |
        | **SOAP Web Services** | HTTP / SMTP | XML (WSDL / UDDI) | Enterprise banking and legacy web integration |
        | **MPI API** | Infiniband / TCP | Raw Bytes / C/C++ Structs | Supercomputing clusters, HPC parallel simulations |
        """)

    with t_api2:
        st.subheader("Message Passing Communication Semantics")
        col_m1, col_m2 = st.columns(2)
        
        with col_m1:
            st.markdown("### Synchronous vs Asynchronous Send")
            st.write("• **Synchronous Send (Blocking)**: The sending process blocks (waits) until the receiving process accepts the message. Ensures strict synchronization.")
            st.write("• **Asynchronous Send (Non-blocking)**: The sending process hands the message to a buffer and immediately resumes execution without waiting.")

        with col_m2:
            st.markdown("### Blocking vs Non-Blocking Receive")
            st.write("• **Blocking Receive**: Receiver blocks until a message arrives in the queue/socket.")
            st.write("• **Non-Blocking Receive**: Receiver checks if a message is available; if not, returns immediately with a control flag.")

        st.markdown("---")
        st.markdown("### Direct vs Indirect Messaging")
        st.write("• **Direct Messaging**: Processes explicitly specify recipient process ID: `send(Process_B, message)`.")
        st.write("• **Indirect Messaging**: Messages are sent to intermediate entities (Mailboxes, Topics, Ports, Message Queues like RabbitMQ or Apache Kafka).")

    with t_api3:
        st.subheader("MPI (Message Passing Interface) for High Performance Computing")
        st.write("MPI is the de facto standard message passing API for distributed memory supercomputers and computer clusters.")

        st.code("""// Example C MPI Code for Parallel Cluster Computation
#include <mpi.h>
#include <stdio.h>

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv); // Initialize MPI environment

    int world_rank, world_size;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank); // Get ID of process
    MPI_Comm_size(MPI_COMM_WORLD, &world_size); // Get total process count

    if (world_rank == 0) {
        int data = 100;
        MPI_Send(&data, 1, MPI_INT, 1, 0, MPI_COMM_WORLD); // Point-to-point send
        printf("Process 0 sent data %d to Process 1\\n", data);
    } else if (world_rank == 1) {
        int received_data;
        MPI_Recv(&received_data, 1, MPI_INT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        printf("Process 1 received data %d from Process 0\\n", received_data);
    }

    MPI_Finalize(); // Terminate MPI environment
    return 0;
}""", language="c")

        st.markdown("""
        **Core MPI Primitives to Know for the Exam:**
        * `MPI_Init()` & `MPI_Finalize()`: Initializes and terminates the MPI parallel execution context.
        * `MPI_Comm_rank()`: Identifies the unique integer rank (ID) of the calling process.
        * `MPI_Send()` & `MPI_Recv()`: Blocking point-to-point communication calls.
        * `MPI_Bcast()`: Collective broadcast of data from 1 process to all processes in communicator.
        * `MPI_Reduce()`: Collective reduction operation (combining arrays via SUM, MIN, MAX).
        """)

    with t_api4:
        st.subheader("Socket Programming API (TCP Stream vs UDP Datagram)")
        st.write("A **Socket** is an abstraction representing an endpoint of communication identified by `(IP Address : Port Number)`.")

        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown("### Stream Sockets (TCP)")
            st.write("• **Connection-Oriented**: Requires establishing a 3-way handshake before data transfer.")
            st.write("• **Reliable**: Guarantees ordered, loss-free byte stream transmission via retransmissions.")
            st.write("• **Socket Calls**: `socket()`, `bind()`, `listen()`, `accept()`, `connect()`, `send()`, `recv()`.")

        with col_s2:
            st.markdown("### Datagram Sockets (UDP)")
            st.write("• **Connectionless**: Datagrams sent independently without prior connection setup.")
            st.write("• **Unreliable & Fast**: No retransmission, ordering, or flow control overhead.")
            st.write("• **Socket Calls**: `socket()`, `bind()`, `sendto()`, `recvfrom()`.")

# ----------------------------------------------------
# PAGE 3: AMDAHL'S LAW CALCULATOR
# ----------------------------------------------------
elif page == "⚡ Amdahl's Law & Speedup Calculator":
    st.title("⚡ Interactive Speedup & Amdahl's Law Calculator")
    st.write("Amdahl's Law predicts theoretical speedup when executing a task across multiple processors.")

    col1, col2 = st.columns(2)
    with col1:
        parallel_fraction = st.slider("Parallelizable Portion of Task (f):", 0.0, 1.0, 0.85, 0.05)
    with col2:
        max_processors = st.slider("Maximum Number of Processors (p):", 1, 128, 32, 1)

    serial_fraction = 1.0 - parallel_fraction
    processors = np.arange(1, max_processors + 1)
    speedups = 1.0 / (serial_fraction + (parallel_fraction / processors))
    max_limit = 1.0 / serial_fraction if serial_fraction > 0 else float('inf')

    m1, m2, m3 = st.columns(3)
    m1.metric("Parallel Fraction (f)", f"{parallel_fraction*100:.1f}%")
    m2.metric("Serial Fraction (1 - f)", f"{serial_fraction*100:.1f}%")
    m3.metric("Max Speedup Limit", f"{max_limit:.2f}x" if max_limit != float('inf') else "∞")

    fig = px.line(x=processors, y=speedups, labels={'x': 'Processors (p)', 'y': 'Speedup S(p)'}, title=f"Speedup Curve (f = {parallel_fraction*100:.0f}%)")
    fig.add_hline(y=max_limit, line_dash="dash", line_color="red", annotation_text=f"Max Limit ({max_limit:.1f}x)")
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📖 Amdahl's Law Math & Formulas"):
        st.latex(r"S(p) = \frac{1}{(1-f) + \frac{f}{p}}")
        st.write(r"• **$T_1$**: Time on 1 processor.")
        st.write(r"• **$T_p$**: Time on $p$ processors.")
        st.write(r"• **Key Takeaway**: Even with infinite processors ($p \rightarrow \infty$), speedup is strictly capped by the serial fraction $\frac{1}{1-f}$.")

# ----------------------------------------------------
# PAGE 4: DEADLOCK SIMULATOR
# ----------------------------------------------------
elif page == "🔒 Deadlock & Coffman Conditions Simulator":
    st.title("🔒 Deadlock & Coffman Conditions Simulator")
    st.write("A deadlock occurs when processes wait indefinitely for resources held by each other.")

    c1 = st.checkbox("1. Mutual Exclusion (Non-shareable resource)", value=True)
    c2 = st.checkbox("2. Hold and Wait (Holding resource while requesting another)", value=True)
    c3 = st.checkbox("3. No Preemption (Resource released only voluntarily)", value=True)
    c4 = st.checkbox("4. Circular Wait (Closed loop process wait graph)", value=True)

    if c1 and c2 and c3 and c4:
        st.error("⚠️ DEADLOCK DETECTED! All 4 Coffman conditions hold simultaneously.")
    else:
        st.success("✅ NO DEADLOCK. At least one Coffman condition is broken.")

# ----------------------------------------------------
# PAGE 5: CPU SCHEDULING SIMULATOR
# ----------------------------------------------------
elif page == "🔄 CPU Scheduling Simulator (RR vs SJF)":
    st.title("🔄 CPU Scheduling Algorithm Simulator")

    num_p = st.slider("Number of Processes:", 2, 6, 4)
    q = st.slider("Round Robin Time Quantum (ms):", 1, 10, 2)

    df_p = pd.DataFrame({"Process": [f"P{i+1}" for i in range(num_p)], "Burst Time (ms)": [5, 2, 8, 3, 6, 4][:num_p]})
    st.dataframe(df_p, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Round Robin (RR)")
        st.write("• **Preemptive**: Each process gets at most `q` ms.")
        st.write("• **Pros**: Zero starvation, fair interactive response.")
    with col2:
        st.subheader("Shortest Job First (SJF)")
        st.write("• **Non-preemptive**: Shortest CPU burst executes first.")
        st.write("• **Pros**: Minimizes average waiting time.")

# ----------------------------------------------------
# PAGE 6: JAVA RMI EXPLORER
# ----------------------------------------------------
elif page == "☕ Java RMI & RPC Architecture Explorer":
    st.title("☕ Java RMI Code Explorer")
    t1, t2, t3, t4 = st.tabs(["1. Remote Interface", "2. Implementation", "3. Server Registration", "4. Client Invocation"])

    with t1:
        st.code("""import java.rmi.Remote;
import java.rmi.RemoteException;

public interface ComputeService extends Remote {
    int add(int a, int b) throws RemoteException;
}""", language="java")

    with t2:
        st.code("""import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;

public class ComputeServiceImpl extends UnicastRemoteObject implements ComputeService {
    public ComputeServiceImpl() throws RemoteException { super(); }
    public int add(int a, int b) throws RemoteException { return a + b; }
}""", language="java")

    with t3:
        st.code("""import java.rmi.Naming;
import java.rmi.registry.LocateRegistry;

public class Server {
    public static void main(String[] args) {
        try {
            LocateRegistry.createRegistry(1099);
            Naming.rebind("rmi://localhost:1099/ComputeService", new ComputeServiceImpl());
            System.out.println("RMI Server Ready.");
        } catch (Exception e) { e.printStackTrace(); }
    }
}""", language="java")

    with t4:
        st.code("""import java.rmi.Naming;

public class Client {
    public static void main(String[] args) {
        try {
            ComputeService service = (ComputeService) Naming.lookup("rmi://localhost:1099/ComputeService");
            System.out.println("Result: " + service.add(15, 25));
        } catch (Exception e) { e.printStackTrace(); }
    }
}""", language="java")

# ----------------------------------------------------
# PAGE 7: DISTRIBUTED ALGORITHMS
# ----------------------------------------------------
elif page == "🌐 Distributed Algorithms & Protocols (2PC, Election, Clocks)":
    st.title("🌐 Distributed Algorithms & Coordination Protocols")

    t_algo1, t_algo2, t_algo3 = st.tabs(["Two-Phase Commit (2PC)", "Bully Election Algorithm", "Lamport Logical Clocks"])

    with t_algo1:
        st.subheader("Two-Phase Commit Protocol (2PC)")
        st.write("Guarantees **Atomicity (All-or-Nothing)** across distributed transaction nodes.")
        st.write("1. **Phase 1 (Prepare / Voting)**: Coordinator asks all participants `VOTE_COMMIT` or `VOTE_ABORT`.")
        st.write("2. **Phase 2 (Commit / Abort)**: If ALL vote commit, Coordinator sends `GLOBAL_COMMIT`. If any node votes abort, Coordinator sends `GLOBAL_ABORT`.")

    with t_algo2:
        st.subheader("Bully Election Algorithm")
        st.write("Elects the active node with the **highest Process ID** as coordinator when leader failure is detected.")
        st.write("1. Process $P_i$ detects leader timeout and sends `ELECTION` messages to all processes with higher IDs.")
        st.write("2. If no higher process responds, $P_i$ wins and broadcasts `COORDINATOR` to all nodes.")

    with t_algo3:
        st.subheader("Lamport Logical Clocks")
        st.write("Establishes a **happened-before relation ($a \rightarrow b$)** without synchronized physical clocks.")
        st.write("• Before executing an event, process increments local clock: $L = L + 1$.")
        st.write(r"• On receiving message with timestamp $t$: $L = \max(L, t) + 1$.")

# ----------------------------------------------------
# PAGE 8: TEXTBOOK QA
# ----------------------------------------------------
elif page == "💡 Textbook Q&A Bank (Coulouris)":
    st.title("💡 Coulouris Textbook Solution Q&A Bank")
    q_filter = st.text_input("🔍 Search Q&A bank:")

    qas = [
        ("Q1: RMI Invocation Semantics?", "Maybe (0 or 1 exec, no retransmits), At-Least-Once (1+ execs, retransmits), At-Most-Once (0 or 1 exec, duplicate reply history filter)."),
        ("Q2: Is Appending to a File Idempotent?", "No. Appending extends file length on every call. Writing to a fixed file offset IS idempotent."),
        ("Q3: CORBA CDR vs XML Data Typing?", "CORBA CDR uses static pre-compiled IDL files, omitting type tags for compact binary transport. XML is self-describing with textual tags."),
        ("Q4: 3-Tier Architecture Benefits?", "Presentation (UI), Application Logic (Business Rules), Data (DBMS). Allows independent horizontal scaling and database security isolation."),
        ("Q5: Distributed Mutual Exclusion Conditions?", "ME1 (Safety: at most 1 process in CS), ME2 (Liveness: eventual access without deadlock), ME3 (Ordering: happened-before clock ordering).")
    ]

    for q_text, ans_text in qas:
        if not q_filter or q_filter.lower() in q_text.lower() or q_filter.lower() in ans_text.lower():
            with st.expander(f"📌 {q_text}"):
                st.write(ans_text)

# ----------------------------------------------------
# PAGE 9: PAST PAPER
# ----------------------------------------------------
elif page == "📝 STU 2023/2024 Solved Past Exam Paper":
    st.title("📝 STU 2023/2024 End of Semester Solved Exam Paper")

    with st.expander("Q1(a) Heterogeneity in Distributed Systems (6 Marks)"):
        st.write("1. Hardware/ISAs (x86 vs ARM vs GPU). 2. Operating Systems (Linux vs Windows). 3. Middleware (Java RMI vs gRPC).")
    with st.expander("Q1(b) Search Engine Synchronization (4 Marks)"):
        st.write("Reader-Writer locking between query threads and crawlers; atomic index swapping.")
    with st.expander("Q2(i) Internet Routing Scheme Scalability (4 Marks)"):
        st.write("Autonomous Systems default routing and CIDR IP prefix aggregation (`192.168.0.0/16`).")
    with st.expander("Q3(a) Parallel vs Distributed Computing Table (8 Marks)"):
        st.write("Parallel: single machine, shared memory, bus. Distributed: multiple machines, disjoint RAM, network sockets.")

# ----------------------------------------------------
# PAGE 10: 40-QUESTION PRACTICE QUIZ ENGINE
# ----------------------------------------------------
elif page == "🧠 40-Question Practice Quiz Engine (10 Sets)":
    st.title("🧠 40-Question Practice Quiz Engine")
    st.write("Select a Quiz Set or generate a Random Quiz from the 40-question course bank:")

    quiz_mode = st.selectbox(
        "Select Quiz Set:",
        [
            "Set 1: Parallel & HPC Architecture (Q1 - Q4)",
            "Set 2: 3-Tier & Client-Server Architecture (Q5 - Q8)",
            "Set 3: Concurrency & Lost Update (Q9 - Q12)",
            "Set 4: Deadlocks & Coffman Conditions (Q13 - Q16)",
            "Set 5: CPU Scheduling Algorithms (Q17 - Q20)",
            "Set 6: Distributed OS & Transparencies (Q21 - Q24)",
            "Set 7: Java RMI & Remote Invocation (Q25 - Q28)",
            "Set 8: Distributed Algorithms (2PC, Election, Clocks) (Q29 - Q32)",
            "Set 9: Cloud Computing & Security (Q33 - Q36)",
            "Set 10: Textbook Scenarios & Mutual Exclusion (Q37 - Q40)",
            "🎲 Random 10-Question Comprehensive Exam Challenge"
        ]
    )

    if "Random" in quiz_mode:
        selected_questions = random.sample(MCQ_BANK, 10)
    else:
        set_idx = int(quiz_mode.split(":")[0].replace("Set ", "")) - 1
        start_i = set_idx * 4
        selected_questions = MCQ_BANK[start_i:start_i + 4]

    st.markdown("---")
    user_answers = {}

    for i, item in enumerate(selected_questions):
        st.markdown(f"#### {item['q']}")
        user_answers[i] = st.radio(
            f"Select Answer for Question {i+1}:",
            item['opts'],
            key=f"q_{set_idx if 'Set' in quiz_mode else 'rand'}_{i}"
        )
        st.write("")

    if st.button("Submit & Grade Quiz"):
        score = 0
        total = len(selected_questions)
        
        st.markdown("### 📊 Quiz Results & Detailed Explanations")
        for i, item in enumerate(selected_questions):
            user_choice_idx = item['opts'].index(user_answers[i])
            if user_choice_idx == item['ans']:
                score += 1
                st.success(f"✅ **Q{i+1}: Correct!** Choice: {user_answers[i]}")
            else:
                st.error(f"❌ **Q{i+1}: Incorrect.** Your Choice: {user_answers[i]} | **Correct Choice: {item['opts'][item['ans']]}**")
            st.info(f"💡 **Explanation:** {item['exp']}")
            st.write("---")

        pct = (score / total) * 100
        st.balloons()
        st.metric("Final Quiz Score", f"{score} / {total}", f"{pct:.0f}%")
