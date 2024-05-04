from enum import Enum
from itertools import product

import pm4py
from pm4py.util import constants, exec_utils, xes_constants


class Parameters(Enum):
    ACTIVITY_KEY = constants.PARAMETER_CONSTANT_ACTIVITY_KEY


class csvFile:
    def main_csv(self, event_log) -> None:
        """
        Imports the given .csv file

        Retruns:
            None
        """

        # sort the event log by TraceID and TimeStamp
        sortedLog = event_log.sort_values(['TraceID', 'TimeStamp'], ascending=True)

        # get the permutations, traces and number of activities and return them
        permuatations, num_acts = self.__createPermutations_CSV(sortedLog)
        traces = self.__extract_traces_CSV(sortedLog)
        return permuatations, traces, num_acts

    
    def __createPermutations_CSV(self, event_log: pm4py.objects.log.obj.EventLog) -> list[tuple] and int:
        """
        Creates permutations of activities based on the given event log.

        Parameters:
            event_log (pm4py.objects.log.obj.EventLog): The event log containing traces and events.

        Returns:
            list[tuple]: A list of permutations of activities.
        """
    
        activities = set()
        # store all activities present in the event log
        for i in range(len(event_log.TraceID)):
            activities.add(event_log.ActivityName[i])

        # get all avaible permutations, of length two, of the activities
        permutations = list(product(activities, repeat=2))

        for act in activities:
            permutations.append(tuple(('0xb2e-start-0x31c', act)))
            permutations.append(tuple((act, '0x31c-end-0x1021')))

        # return the permutations and number of activities +2, due to phony start and end activities
        return permutations, len(activities)


    def __extract_traces_CSV(self, event_log: pm4py.objects.log.obj.EventLog) -> list[list[tuple]]:
        """
        Extracts traces from the given event log and creates tuples representing transitions.

        Parameters:
            event_log (pm4py.objects.log.obj.EventLog): The event log from which traces are to be extracted.

        Returns:
            list[list[tuple]]: A list of traces, where each trace is represented as a list of tuples.
        """

        traces = list()
        edges = list()

        for i in range(len(event_log.TraceID)):
            try:
                if event_log.TraceID[i] == event_log.TraceID[i+1]:
                    for j in range(i+2, len(event_log.TraceID)+2):
                        try:
                            edges.append(tuple(event_log.ActivityName[i:j]))
                            if i == 0:
                                edges.append(tuple(('0xb2e-start-0x31c', event_log.ActivityName[i])))
                            elif i == len(event_log.TraceID)-1:
                                edges.append(tuple((event_log.ActivityName[i], '0x31c-end-0x1021')))
                            break
                        except KeyError:
                            pass
                else:
                    traces.append(edges)
                    edges = list()
            except KeyError:
                pass
        traces.append(edges)

        return traces


class xesFile:
    def createPermutations_XES(self, event_log: pm4py.objects.log.obj.EventLog) -> None:
        """
        Creates permutations of activities based on the given event log. These permutations are stored trace-wise.

        Parameters:
            event_log (pm4py.objects.log.obj.EventLog): The event log containing traces and events.

        Returns:
            None
        """

        traceList = list()

        act_key = exec_utils.get_param_value(Parameters.ACTIVITY_KEY.value, parameters={},
                                                 default=xes_constants.DEFAULT_NAME_KEY)

        # get the trcaes and events of the event log
        for trace in event_log:
            # get the trcaes from the event log
            tmpList = list()
            for i in range(len(trace) -1):
                if i == 0:
                    tmpList.append(('0xb2e-start-0x31c', trace[i][act_key]))
                tmpList.append((trace[i][act_key], trace[i + 1][act_key]))

                if i == len(trace) - 2:
                    tmpList.append((trace[i + 1][act_key], '0x31c-end-0x1021'))

            if len(trace) == 1:
                tmpList.append(('0xb2e-start-0x31c', trace[0][act_key]))
                tmpList.append((trace[0][act_key], '0x31c-end-0x1021'))
                    
            traceList.append(tmpList)

        # store all activities present in the event log
        act_set = set(pm4py.get_event_attribute_values(event_log, act_key).keys())

        # get all avaible permutations, of length two, of the activities
        permutations = list(product(act_set, repeat=2))
            
        # each activity is considered to be able to start and end a trace
        for act in act_set:
            permutations.append(tuple(('0xb2e-start-0x31c', act)))
            permutations.append(tuple((act, '0x31c-end-0x1021')))

        # return the permutations, traces and number of activities +2, due to phony start and end activities
        return permutations, traceList, len(act_set)