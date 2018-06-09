#!/usr/bin/env python

import csv
import re
import sys

with open(sys.argv[1], "r") as f:
    reader = csv.reader(f)

    # Extract component list from first (header) line
    header = next(reader)
    components = []
    component_reqs = dict()
    for c in header:
        # Separate component from package
        component = c.split(" [")[0]
        # Protect ampersand from LaTeX and make readable
        component = re.sub(r'\&', 'and', component)
        # Remove leading digits used for sort ordering
        component = re.sub(r'^\d+\s+', '', component)
        components.append(component)
        component_reqs[component] = []
    n = len(components)


    print(r"""
\newpage
\section{Appendix: Traceability}\label{appendix-traceability}

\subsection{Requirement to Component
Traceability}\label{requirement-to-component-traceability}

\footnotesize
\tablefirsthead{\hline \multicolumn{1}{c}{\textbf{Requirement}} &
                       \multicolumn{1}{c}{\textbf{Components}} \\ \hline}
\tablehead{\hline \multicolumn{1}{c}{\textbf{Requirement}} &
                       \multicolumn{1}{c}{\textbf{Components}} \\ \hline}
\begin{xtabular}{p{0.4\textwidth}p{0.55\textwidth}}
""")

    # Each succeeding line corresponds to a requirement
    for row in reader:
        req = row[0]
        # Separate requirement from package
        req = req.split(" [")[0]
        # Protect ampersand from LaTeX and make readable
        req = re.sub(r'\&', 'and', req)
        # Remove digits after req id used for sort ordering
        req = re.sub(r'\s+\d+', '', req)
        clist = []
        for i in range(1, n):
            if row[i]:
                clist.append(components[i])
                component_reqs[components[i]].append(req)
        print("{} & {}".format(req, ", ".join(clist)))


print(r"""
\end{xtabular}
\normalsize

\subsection{Component to Requirement
Traceability}\label{component-to-requirement-traceability}

Note that only ``leaf'' components are traced to requirements.

\setitemize{noitemsep,topsep=0pt,parsep=0pt,partopsep=0pt}
\tablefirsthead{\hline \multicolumn{1}{c}{\textbf{Component}} &
                       \multicolumn{1}{c}{\textbf{Requirements}} \\ \hline}
\tablehead{\hline \multicolumn{1}{c}{\textbf{Component}} &
                       \multicolumn{1}{c}{\textbf{Requirements}} \\ \hline}
\footnotesize
\begin{xtabular}{lp{0.7\textwidth}}
""")

for component in components:
    if len(component_reqs[component]) == 0:
        continue
    print(component + " &\n" + r"\begin{itemize}" + \
            "\n\\item ".join(component_reqs[component]) + \
            "\n" + r"\end{itemize} \\ \hline")

print(r"\end{xtabular}")
