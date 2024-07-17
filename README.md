# Differentially Private Inductive Miner (DPIM)
Before executing the **DPIM**, please make sure the requirements are installed. If not, please install the requirements by running the following command:
```
python3 pip install -r requirements.txt
```
The DPIM offers two modes of execution:
1. **Differential private** In this mode, the DPIM is executed with differential privacy. The user can specify the epsilon ($\epsilon$) value, as well as needed lower and upper bounds. The DPIM will then execute with the specified epsilon value and bounds. To avoid errors the lowest lower bound is the total number of activities $(\\#unique\ activities)$ and the highest upper bound is the $(\\#unique\ activities)^2 -1$. 
2. **Non-differential private** In this mode, the DPIM is executed using $\epsilon \rightarrow \infty$. The lower and upper bounds are not needed as only those permutations are considered that occur in at least one trace.

Out of these two modi, the differential private mode is the default mode. To execute the DPIM in non-differential private mode, specify the `--no-dp` flag.

To test the **DPIM** on a specific event log, you can run the following command:
```
python3 main.py <eventlog> --epsilon <epsilon> --lower <lower_bound> --upper <upper_bound>
```
where:
- `<eventlog>` is the path to the event log. This is a required argument.
- `<epsilon>` is the epsilon value.
- `<lower_bound>` is the lower bound.
- `<upper_bound>` is the upper bound.

Or, for non-differential private mode, the user can run the following command:
```
python3 main.py <event_log> --no-dp
```
All synthetic event logs and the URLs to the BPI Challenges are in the [event_logs](/evaluation_data/) directory.

**Info:** If no flag is given, or a specific flag is forgotten the **DPIM** asks the user to input the missing values.

# Arguments
The following arguments are available for the **DPIM**:
- `eventlog` The path to the event log. This is a required argument.
- `-e, --epsilon` The $\epsilon$ value for differential privacy. The default value is 1.0.
- `-l, --lower` The lower bound for the number of permutations. The default value is the $\\#unique\ activities$ in the event log.
- `-u, --upper` The upper bound for the number of permutations. The default value is the $(\\#unique\ activities)^2 -1$.
- `-t --threshold` The threshold used by the Rejection sampler to accept the generated PST. The default is 0.95
- `--no-dp` The flag to run the DPIM in non-differential private mode, $\epsilon \rightarrow \infty$.

# Example
To test the **DPIM** on the `TF_5` event log with $\epsilon = 1.0$, the user can run the following command:
```
python3 main.py event_logs\synthetic_EventLogs\TF_5.xes -e 1.0 -l 6 -u 35 -t 0.9
```
# Bounds used
The following tables show the lower and upper bounds used for the BPI Challenge datasets (all links can be found at [BPI](evaluation_data/BPI_Challenges.md)) and the [synthetic logs](evaluation_data/synthetic_EventLogs/).

|BPI Challanges|Synthetic Logs|
|:---:|:---:|
| <table> <tr><th>Event Log</th> <th>Lower Bound</th> <th>  Upper Bound </th> </tr><tr> <td> BPI_Challenge_2011 </td> <td> 4280 </td> <td> 4310 </td> <tr> <td> BPI_Challenge_2012 </td> <td> 120 </td> <td> 150 </td> <tr> <td> BPI_Challenge_2013_closed_problems </td> <td> 5 </td> <td> 20 </td> <tr> <td> BPI_Challenge_2013_incidents </td> <td> 5 </td> <td> 20 </td> <tr> <td> BPI_Challenge_2013_open_problems </td> <td> 5 </td> <td> 15 </td> <tr> <td> BPI_Challenge_2015_1 </td> <td> 4805 </td> <td> 4835 </td> <tr> <td> BPI_Challenge_2015_2 </td> <td> 4885 </td> <td> 4915 </td> <tr> <td> BPI_Challenge_2015_3 </td> <td> 5020 </td> <td> 5050 </td> <tr> <td> BPI_Challenge_2015_4 </td> <td> 3650 </td> <td> 3680 </td> <tr> <td> BPI_Challenge_2015_5 </td> <td> 4960 </td> <td> 4990 </td> <tr> <td> BPI_Challenge_2017 </td> <td> 175 </td> <td> 205 </td> <tr> <td> BPI_Challenge_2018 </td> <td> 605 </td> <td> 635 </td> <tr> <td> BPI_Challenge_2019 </td> <td> 525 </td> <td> 555 </td> <tr> <td> DomesticDeclarations_2020 </td> <td> 30 </td> <td> 60 </td> <tr> <td> InternationalDeclarations_2020 </td> <td> 195 </td> <td> 225 </td> <tr> <td> PermitLog_2020 </td> <td> 555 </td> <td> 585 </td> <tr> <td> PrepaidTravelCost_2020 </td> <td> 160 </td> <td> 190 </td> <tr> <td> RequestForPayment_2020 </td> <td> 40 </td> <td> 70 </td> <tr> <td> Sepsis Cases-Event Log </td> <td> 120 </td> <td> 150 </td> </tr></table> |<table> <tr>  <th>Event Log</th> <th>Lower Bound</th> <th>  Upper Bound </th> </tr><tr> <td> TF_04  </td> <td> 6 </td> <td> 20  </td> <tr> <td> TF_05  </td> <td> 6 </td> <td> 35  </td> <tr> <td> TF_06  </td> <td> 6 </td> <td> 35  </td> <tr> <td> TF_07  </td> <td> 3 </td> <td> 8  </td> <tr> <td> TF_08  </td> <td> 3 </td> <td> 8  </td> <tr> <td> TF_09  </td> <td> 6 </td> <td> 35  </td> <tr> <td> TF_10  </td> <td> 6 </td> <td> 35  </td> <tr> <td> TF_11  </td> <td> 5 </td> <td> 24  </td> <tr> <td> TF_12  </td> <td> 5 </td> <td> 24  </td> <tr> <td> TF_13 </td> <td> 5 </td> <td> 24  </td> <tr> <td> TF_14 </td> <td> 30 </td> <td>60  </td> <tr> <td> TF_15 </td> <td> 3 </td> <td> 8  </td> <tr> <td> TF_16 </td> <td> 6 </td> <td> 35  </td> </tr> </table> |