# Safety Order Algorithm

## Running Code

Python requirements are listed in [`requirements.txt`](./requirements.txt)

The main entry point for the code is [`src/main.py`](./src/main.py)

## IP Problem

### Definitions
- $o =$ OFACer index, each person in the performance
- $r =$ row index, each performance
- $c =$ column index, each safety position
- $P =$ performer binary, where $P_{or}$ is $1$ when OFACer $o$ is performing in performance $r$
- $S =$ safety binary, where $S_{orc}$ is $1$ when OFACer $o$ is safetying in performance $r$ in safety position $c$
- $M =$ music master binary, where $M_{or}$ is $1$ when OFACer $o$ is the music master for performance $r$
- $E =$ experienced binary, where $E_{o}$ is $1$ if OFACer $o$ is allowed to be safety 1 or 4
- $W =$ swap binary, used to linearize swapping, where $W_{orc} = S_{orc} * S_{o(r+1)c}$

### Givens
- Performance order
- Music masters

### Constraints
All safety slots need to have exactly 1 person
$$\sum_{o=1}^{O} S_{orc} = 1, \forall \ r \in R, \forall \ c \in [1, 5]$$

Only one role per person per row

$$P_{or} + \sum_{c=1}^{5}s_{orc} + m_{or} \le 1, \forall \ r \in R, \forall \ o \in O$$

Can't safety right before or after your performance

$$P_{or} \left( \sum_{c=1}^{5} \left( S_{o(r-1)c} + S_{o(r+1)c} \right) \right) = 0, \forall \ r \in R, \forall \ o \in O$$

Experienced safeties in slots 1 and 4

$$S_{or1} \le E_{o}, \forall \ r \in R, \forall \ o \in O$$

$$S_{or4} \le E_{o}, \forall \ r \in R, \forall \ o \in O$$

At least two safeties must stay the same between performances 

$$W_{orc} \le S_{orc}, $$
$$W_{orc} \le S_{o(r+1)c}, $$
$$W_{orc} \ge S_{orc} + S_{o(r+1)c} - 1,$$
$$ \forall \ o \in O, \forall \ r \in R, \forall \ c \in [1, 5]$$

$$\sum_{o=1}^{O} \sum_{c=1}^{5} W_{orc} \ge 2, \forall \ r \in R$$

### Optimization
$$\Delta \ge \sum_{r=1}^{R} \sum_{c=1}^{5} s_{orc} - \frac{5|R|}{|O|} \ge -\Delta, \forall \ o \in O$$
$$\text{min } Z=\Delta$$


### Current limitations and possible improvements
- Performance order isn't optimized, and there may be infeasible performance orders
- Props aren't considered, so safety 5 is still filled for long props
- Optimize for minimizing swaps
- Include music master in optimization 
