import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(
    page_title="BCPS 425: Parallel & Distributed Computing Companion",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Styling
st.markdown("""
    <style>
    .main-title {
        font-size: 2.3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #0284c7, #6366f1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    .sub-title {
        color: #64748b;
        font-size: 1.05rem;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #0f172a;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        color: #f8fafc;
        text-align: center;
    }
    .highlight-box {
        background-color: #1e1b4b;
        border-left: 4px solid #6366f1;
        padding: 15px 20px;
        border-radius: 6px;
        margin: 15px 0;
        color: #e2e8f0;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("🎓 Navigation Hub")
st.sidebar.caption("Sunyani Technical University (STU) — BCPS 425")

page = st.sidebar.radio(
    "Select Module or Tool:",
    [
        "🏠 Home & Fast Revision Checklist",
        "⚡ Amdahl's Law & Speedup Calculator",
        "🔒 Deadlock & Coffman Checker",
        "🔄 CPU Scheduling Simulator (RR vs SJF)",
        "☕ Java RMI Code Explorer",
        "💡 Textbook Q&A Bank (Coulouris)",
        "📝 STU 2023/2024 Solved Past Paper",
        "🧠 Interactive Practice Quiz",
        "🚀 Deploy Online (Free Streamlit Cloud)"
    ]
)

# ----------------------------------------------------
# PAGE 1: HOME
# ----------------------------------------------------
if page == "🏠 Home & Fast Revision Checklist":
    st.markdown('<h1 class="main-title">BCPS 425: Parallel & Distributed Computing</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Interactive Learning Companion for Exam Success — STU Department of Computer Science</p>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Course Code", "BCPS 425")
    col2.metric("Credits", "3 Credits")
    col3.metric("Exam Time", "2½ Hours")
    col4.metric("Total Marks", "60 Marks")

    st.markdown("---")

    st.subheader("📌 Fast-Track Exam Checklist")
    st.write("Review all 12 core examinable concepts before entering the exam hall:")

    c1, c2 = st.columns(2)
    with c1:
        st.checkbox("1. Parallel vs Distributed Computing Differences", value=True)
        st.checkbox("2. Flynn's Taxonomy (SISD, SIMD, MISD, MIMD)", value=True)
        st.checkbox("3. Amdahl's Law Speedup Formula", value=True)
        st.checkbox("4. 3-Tier Architecture (Presentation, App, Data)", value=True)
        st.checkbox("5. Race Conditions & The Lost Update Problem", value=True)
        st.checkbox("6. The 4 Coffman Conditions for Deadlock", value=True)
    with c2:
        st.checkbox("7. Deadlock Handling (Prevention, Avoidance, Recovery)", value=True)
        st.checkbox("8. Round Robin vs Shortest Job First Scheduling", value=True)
        st.checkbox("9. Distributed OS Transparencies & TCP vs UDP", value=True)
        st.checkbox("10. Java RMI Architecture (Stub, Skeleton, Registry)", value=True)
        st.checkbox("11. Idempotence & Invocation Semantics (At-Most-Once)", value=True)
        st.checkbox("12. Cloud Models (IaaS, PaaS, SaaS) & Security", value=True)

    st.markdown('<div class="highlight-box">💡 <b>Tip for Students:</b> Use the sidebar tools to simulate Amdahl\'s Law, test CPU scheduling algorithms, practice RMI code snippets, and review solved past papers!</div>', unsafe_allow_html=True)

# ----------------------------------------------------
# PAGE 2: AMDAHL'S LAW CALCULATOR
# ----------------------------------------------------
elif page == "⚡ Amdahl's Law & Speedup Calculator":
    st.title("⚡ Interactive Speedup & Amdahl's Law Simulator")
    st.write("Amdahl's Law predicts the maximum theoretical speedup achievable when parallelizing a computing task across multiple processors.")

    col_input1, col_input2 = st.columns(2)
    with col_input1:
        parallel_fraction = st.slider("Parallelizable Portion of Task (f):", 0.0, 1.0, 0.85, 0.05)
    with col_input2:
        max_processors = st.slider("Maximum Number of Processors (p):", 1, 128, 32, 1)

    serial_fraction = 1.0 - parallel_fraction
    processors = np.arange(1, max_processors + 1)
    speedups = 1.0 / (serial_fraction + (parallel_fraction / processors))
    max_theoretical_limit = 1.0 / serial_fraction if serial_fraction > 0 else float('inf')

    m1, m2, m3 = st.columns(3)
    m1.metric("Parallel Portion (f)", f"{parallel_fraction * 100:.1f}%")
    m2.metric("Serial Portion (1 - f)", f"{serial_fraction * 100:.1f}%")
    m3.metric("Max Theoretical Limit", f"{max_theoretical_limit:.2f}x" if max_theoretical_limit != float('inf') else "∞")

    # Plotly Chart
    fig = px.line(
        x=processors, y=speedups,
        labels={'x': 'Number of Processors (p)', 'y': 'Theoretical Speedup S(p)'},
        title=f"Amdahl's Law Speedup Curve (f = {parallel_fraction*100:.0f}%)"
    )
    fig.add_hline(y=max_theoretical_limit, line_dash="dash", line_color="red", annotation_text=f"Max Limit ({max_theoretical_limit:.1f}x)")
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📖 Mathematical Formula & Exam Notes"):
        st.latex(r"S(p) = \frac{1}{(1-f) + \frac{f}{p}}")
        st.write("• **$T_1$**: Time on 1 processor.")
        st.write("• **$T_p$**: Time on $p$ processors.")
        st.write(r"• **Key Takeaway**: Even with an infinite number of processors ($p \rightarrow \infty$), the speedup is strictly capped by the serial fraction $\frac{1}{1-f}$.")

# ----------------------------------------------------
# PAGE 3: DEADLOCK CHECKER
# ----------------------------------------------------
elif page == "🔒 Deadlock & Coffman Checker":
    st.title("🔒 Deadlock & Coffman Conditions Simulator")
    st.write("A deadlock occurs when processes wait indefinitely for resources held by each other. Evaluate your system state below:")

    st.subheader("The 4 Coffman Conditions Checklist")
    c1 = st.checkbox("1. Mutual Exclusion (Resource non-shareable by >1 process)", value=True)
    c2 = st.checkbox("2. Hold and Wait (Process holds resource while requesting another)", value=True)
    c3 = st.checkbox("3. No Preemption (Resource cannot be forcibly taken away)", value=True)
    c4 = st.checkbox("4. Circular Wait (Closed loop of process resource dependencies)", value=True)

    if c1 and c2 and c3 and c4:
        st.error("⚠️ DEADLOCK DETECTED! All 4 Coffman conditions hold simultaneously. System is in a Deadlock state.")
    else:
        st.success("✅ NO DEADLOCK. At least one Coffman condition is broken, preventing a deadlock.")

    st.markdown("---")
    st.subheader("Deadlock Handling Strategies")
    tab1, tab2, tab3 = st.tabs(["Prevention", "Avoidance (Banker's Algorithm)", "Detection & Recovery"])
    
    with tab1:
        st.write("**Deadlock Prevention:** Structurally breaks 1 of the 4 Coffman conditions before execution.")
        st.write("• *Example:* Enforce a global numeric ordering on all resources to eliminate Circular Wait.")
    with tab2:
        st.write("**Deadlock Avoidance:** System dynamically evaluates resource requests to guarantee a **Safe State**.")
        st.write("• *Algorithm:* Dijkstra's **Banker's Algorithm** (checks if safe execution sequence exists).")
    with tab3:
        st.write("**Detection & Recovery:** Allows deadlocks to occur, periodically runs cycle detection on Wait-For graphs, and recovers by **Victim Selection** (rolling back a transaction).")

# ----------------------------------------------------
# PAGE 4: CPU SCHEDULING SIMULATOR
# ----------------------------------------------------
elif page == "🔄 CPU Scheduling Simulator (RR vs SJF)":
    st.title("🔄 CPU Scheduling Algorithm Simulator")
    st.write("Compare Round Robin (Preemptive, Fair) and Shortest Job First (Non-preemptive, Minimal Average Wait Time).")

    num_processes = st.slider("Select Number of Processes:", 2, 6, 4)
    quantum = st.slider("Round Robin Time Quantum (q):", 1, 10, 2)

    df_processes = pd.DataFrame({
        "Process ID": [f"P{i+1}" for i in range(num_processes)],
        "Burst Time (ms)": [5, 2, 8, 3, 6, 4][:num_processes]
    })

    st.dataframe(df_processes, use_container_width=True)

    col_rr, col_sjf = st.columns(2)
    with col_rr:
        st.subheader("Round Robin (RR)")
        st.write("• **Preemptive**: Each process gets at most `q` ms.")
        st.write("• **Pros**: Zero starvation, excellent responsiveness.")
        st.write("• **Cons**: Context-switch overhead if quantum is too small.")

    with col_sjf:
        st.subheader("Shortest Job First (SJF)")
        st.write("• **Non-preemptive**: Shortest CPU burst executes first.")
        st.write("• **Pros**: Mathematically minimizes average waiting time.")
        st.write("• **Cons**: Risk of **starvation** for long-running processes.")

# ----------------------------------------------------
# PAGE 5: JAVA RMI EXPLORER
# ----------------------------------------------------
elif page == "☕ Java RMI Code Explorer":
    st.title("☕ Java RMI (Remote Method Invocation) Code Explorer")
    st.write("Java RMI allows an object on one JVM to invoke methods on a remote object in another JVM.")

    t1, t2, t3, t4 = st.tabs(["1. Remote Interface", "2. Implementation", "3. Server", "4. Client"])

    with t1:
        st.code("""import java.rmi.Remote;
import java.rmi.RemoteException;

// Must extend java.rmi.Remote and throw RemoteException
public interface ComputeService extends Remote {
    int add(int a, int b) throws RemoteException;
}""", language="java")

    with t2:
        st.code("""import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;

public class ComputeServiceImpl extends UnicastRemoteObject implements ComputeService {
    public ComputeServiceImpl() throws RemoteException {
        super();
    }

    @Override
    public int add(int a, int b) throws RemoteException {
        return a + b;
    }
}""", language="java")

    with t3:
        st.code("""import java.rmi.Naming;
import java.rmi.registry.LocateRegistry;

public class Server {
    public static void main(String[] args) {
        try {
            LocateRegistry.createRegistry(1099); // Start RMI Registry
            ComputeService service = new ComputeServiceImpl();
            Naming.rebind("rmi://localhost:1099/ComputeService", service);
            System.out.println("RMI Server Running...");
        } catch (Exception e) { e.printStackTrace(); }
    }
}""", language="java")

    with t4:
        st.code("""import java.rmi.Naming;

public class Client {
    public static void main(String[] args) {
        try {
            // Stub lookup via RMI Registry
            ComputeService service = (ComputeService) Naming.lookup("rmi://localhost:1099/ComputeService");
            int result = service.add(15, 25);
            System.out.println("Result from Remote Method: " + result);
        } catch (Exception e) { e.printStackTrace(); }
    }
}""", language="java")

# ----------------------------------------------------
# PAGE 6: TEXTBOOK QA
# ----------------------------------------------------
elif page == "💡 Textbook Q&A Bank (Coulouris)":
    st.title("💡 Coulouris Textbook Solution Q&A Bank")
    st.write("Extracted official solutions from Coulouris et al. 5th Edition:")

    q_search = st.text_input("🔍 Filter Q&A by keyword (e.g. Idempotent, RMI, 3-tier, Lock):")

    qas = [
        ("Q1: RMI Invocation Semantics", "Maybe (0 or 1 exec, no retransmits), At-Least-Once (1+ execs, retransmits), At-Most-Once (0 or 1 exec, duplicate reply history filter)."),
        ("Q2: Is Appending to a File Idempotent?", "No. Appending extends file length on every call. Writing to a fixed file offset IS idempotent."),
        ("Q3: CORBA CDR vs XML Data Typing", "CORBA CDR uses static pre-compiled IDL files, omitting type tags for compact binary transport. XML is self-describing with textual tags, increasing bandwidth overhead."),
        ("Q4: 3-Tier Architecture Benefits", "Presentation (UI), Application Logic (Business Rules), Data (DBMS). Allows independent horizontal scaling, UI maintainability, and database security isolation."),
        ("Q5: Distributed Mutual Exclusion Properties", "ME1 (Safety: at most 1 process in CS), ME2 (Liveness: eventual access without deadlock), ME3 (Ordering: happened-before logical clock ordering).")
    ]

    for question, answer in qas:
        if not q_search or q_search.lower() in question.lower() or q_search.lower() in answer.lower():
            with st.expander(f"📌 {question}"):
                st.write(answer)

# ----------------------------------------------------
# PAGE 7: SOLVED PAST PAPER
# ----------------------------------------------------
elif page == "📝 STU 2023/2024 Solved Past Paper":
    st.title("📝 STU 2023/2024 End of Semester Solved Exam Paper")
    st.caption("Course: BCPS 425 | Examiner: Adjei-Gyabaa Sylvester Kwasi | Total Marks: 60")

    with st.expander("Q1(a) Heterogeneity in Distributed Systems (6 Marks)"):
        st.write("State and explain 3 examples:")
        st.write("1. **Hardware/ISAs**: x86 vs ARM vs SIMD GPUs (word size, byte endianness).")
        st.write("2. **Operating Systems**: Linux vs Windows vs macOS (system calls, scheduling).")
        st.write("3. **Middleware/Languages**: Java RMI vs gRPC vs REST APIs.")

    with st.expander("Q1(b) Search Engine Synchronization Requirements (4 Marks)"):
        st.write("1. **Reader-Writer Locking**: Search queries (readers) execute concurrently; crawler index updates (writers) update without corrupting reader memory.")
        st.write("2. **Atomic Index Swapping**: Crawlers update an offline index copy, then swap pointers atomically.")

    with st.expander("Q1(c) Service A vs Service B Failure Classes (6 Marks)"):
        st.write("• **Service A**: Omission, Delay, and Arbitrary Payload Corruption.")
        st.write("• **Service B**: Omission (buffer overflow) and Delay.")
        st.write("• **Is Service B Reliable?** **No**, because dropped messages are not retransmitted.")

    with st.expander("Q2(i) Internet Routing Scheme Scalability (4 Marks)"):
        st.write("1. **Autonomous Systems (AS) & Default Routing**: Border routers route external traffic.")
        st.write("2. **CIDR IP Prefix Aggregation**: Subnet grouping (`192.168.0.0/16`) condenses millions of addresses into single routing entries.")

    with st.expander("Q3(a) Parallel vs Distributed Computing Table (8 Marks)"):
        st.write("• **Parallel**: Single machine, shared memory, bus communication, low fault tolerance.")
        st.write("• **Distributed**: Multiple machines, disjoint RAM, network sockets, high fault tolerance.")

# ----------------------------------------------------
# PAGE 8: PRACTICE QUIZ
# ----------------------------------------------------
elif page == "🧠 Interactive Practice Quiz":
    st.title("🧠 Exam Day Self-Test Practice Quiz")

    q1 = st.radio("1. In Flynn's Taxonomy, modern GPUs belong to which class?", ["SISD", "SIMD", "MISD", "MIMD"])
    q2 = st.radio("2. Which Coffman condition is broken by enforcing a global numeric ordering on resource requests?", ["Mutual Exclusion", "Hold and Wait", "No Preemption", "Circular Wait"])
    q3 = st.radio("3. Which object acts as the client-side proxy in Java RMI?", ["Skeleton", "Stub", "Registry", "Dispatcher"])

    if st.button("Submit Quiz Answers"):
        score = 0
        if q1 == "SIMD": score += 1
        if q2 == "Circular Wait": score += 1
        if q3 == "Stub": score += 1
        
        st.balloons()
        st.success(f"🎉 Your Score: {score} / 3 ({score/3*100:.0f}%)")

# ----------------------------------------------------
# PAGE 9: DEPLOY ONLINE
# ----------------------------------------------------
elif page == "🚀 Deploy Online (Free Streamlit Cloud)":
    st.title("🚀 How to Deploy this App Online for Free")
    st.write("Follow these 4 simple steps to share this app with your classmates online:")

    st.markdown("""
    ### Step 1: Push to GitHub
    1. Create a new GitHub Repository (e.g. `bcps-425-study-companion`).
    2. Upload `app.py` and `requirements.txt` to your repository.

    ### Step 2: Connect to Streamlit Community Cloud
    1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
    2. Click **New App**.

    ### Step 3: Configure Deployment
    1. Select your Repository: `your-username/bcps-425-study-companion`.
    2. Set Main file path: `app.py`.
    3. Click **Deploy!**

    ### Step 4: Share Link!
    Streamlit will generate a live public URL (e.g. `https://bcps-425-study.streamlit.app`) that your classmates can access anywhere from their phones or laptops!
    """)
