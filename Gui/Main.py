# !/usr/bin/env python

from Dialogs import *
from NetworkSimulator.Simulation import Simulation

import math
import matplotlib.pyplot as plotter
import tkMessageBox
import tkFileDialog

def CreateMain():
    global csv
    global plotData

    # Build main window.
    mainWindow = Tk()
    mainWindow.title("Network Channel Simulator")
    mainWindow.geometry("800x600+50+100")
    mainWindow.minsize(1024,768)

    # Simulation variables.
    simRunsText = StringVar()
    simRunsText.set("10")
    packetsPerRunText = StringVar()
    packetsPerRunText.set("100")
    maxPacketSizeText = StringVar()
    maxPacketSizeText.set("1340")
    minPacketSizeText = StringVar()
    minPacketSizeText.set("8")

    # Channel variables.
    pRemainGoodText = StringVar()
    pRemainGoodText.set("0.9913")
    pErrorGoodText = StringVar()
    pErrorGoodText.set("0.0004")
    pGoodSpeedText = StringVar()
    pGoodSpeedText.set("38.4")

    pRemainBadText = StringVar()
    pRemainBadText.set("0.8509")
    pErrorBadText = StringVar()
    pErrorBadText.set("0.001")
    pBadSpeedText = StringVar()
    pBadSpeedText.set("2")

    pStartGoodText = StringVar()
    pStartGoodText.set("0.9449")

    # Router variables.
    pLossText = StringVar()
    pLossText.set("0.000001")
    wiredSpeedText = StringVar()
    wiredSpeedText.set("1000000")
    wiredBottleneckText = StringVar()
    wiredBottleneckText.set("20")
    wiredProbDelayText = StringVar()
    wiredProbDelayText.set("1")
    wiredMaxDelayText = StringVar()
    wiredMaxDelayText.set("30000")
    wiredMinDelayText = StringVar()
    wiredMinDelayText.set("30")

    # Sets the parameters for the channel's good state.
    def GetGoodStateParams():
        dlg = StateDialog(mainWindow,
                          args=(pRemainGoodText.get(), pErrorGoodText.get(), pGoodSpeedText.get()),
                          title="Good State Parameters")
        params = dlg.result
        if params != None:
            pRemainGoodText.set(params["pRemain"])
            pErrorGoodText.set(params["pError"])
            pGoodSpeedText.set(params["speed"])

    # Sets the parameters for the channel's bad state.
    def GetBadStateParams():
        dlg = StateDialog(mainWindow,
                          args=(pRemainBadText.get(), pErrorBadText.get(), pBadSpeedText.get()),
                          title="Bad State Parameters")
        params = dlg.result
        if params != None:
            pRemainBadText.set(params["pRemain"])
            pErrorBadText.set(params["pError"])
            pBadSpeedText.set(params["speed"])

    # Runs the simulation.
    def RunSimulation():
        global results

        if ValidateParams():
            results = DoSimRuns()

    def ValidateParams():
        # Make sure variables are set to values.
        if simRunsText.get() == "" or IsNumeric(simRunsText.get()) == False:
            tkMessageBox.showerror(
                "Invalid Entry",
                "You must enter a valid number of times to run the simulation.")
            return False
        elif packetsPerRunText.get() == "" or IsNumeric(packetsPerRunText.get()) == False:
            tkMessageBox.showerror(
                "Invalid Entry",
                "You must enter a valid number of packets to generate per run.")
            return False
        elif minPacketSizeText.get() == "" or IsNumeric(minPacketSizeText.get()) == False:
            tkMessageBox.showerror(
                "Invalid Entry",
                "You must enter a valid minimum packet size.")
            return False
        elif maxPacketSizeText.get() == "" or IsNumeric(maxPacketSizeText.get()) == False:
            tkMessageBox.showerror(
                "Invalid Entry",
                "You must enter a valid maximum packet size.")
            return False
        elif pRemainGoodText.get() == "" or IsNumeric(pRemainGoodText.get()) == False or \
                pErrorGoodText.get() == "" or IsNumeric(pErrorGoodText.get()) == False or \
                pGoodSpeedText.get() == "" or IsNumeric(pGoodSpeedText.get()) == False:
            tkMessageBox.showerror(
                "Invalid Entry",
                "You must set valid parameters for the good state.")
            return False
        elif pRemainBadText.get() == "" or IsNumeric(pRemainBadText.get()) == False or \
                pErrorBadText.get() == "" or IsNumeric(pErrorBadText.get()) == False or \
                pBadSpeedText.get() == "" or IsNumeric(pBadSpeedText.get()) == False:
            tkMessageBox.showerror(
                "Invalid Entry",
                "You must set valid parameters for the bad state.")
            return False
        elif pStartGoodText.get() == "" or IsNumeric(pStartGoodText.get()) == False:
            tkMessageBox.showerror(
                "Invalid Entry",
                "You must enter a valid probability that the channel will start in the good state.")
            return False
        elif pLossText.get() == "" or IsNumeric(pLossText.get()) == False:
            tkMessageBox.showerror(
                "Invalid Entry",
                "You must enter a valid probability of a packet loss due to buffer overflows in the router.")
            return False
        elif wiredSpeedText.get() == "" or IsNumeric(wiredSpeedText.get()) == False:
            tkMessageBox.showerror(
                "Invalid Entry",
                "You must enter a valid speed of the wired portion.")
            return False
        elif wiredBottleneckText.get() == "" or IsNumeric(wiredBottleneckText.get()) == False:
            tkMessageBox.showerror(
                "Invalid Entry",
                "You must enter a valid speed for the wired link bottleneck.")
            return False
        elif wiredProbDelayText.get() == "" or IsNumeric(wiredProbDelayText.get()) == False:
            tkMessageBox.showerror(
                "Invalid Entry",
                "You must enter a valid probability of delay between the router and the destination.")
            return False
        elif wiredMaxDelayText.get() == "" or IsNumeric(wiredMaxDelayText.get()) == False:
            tkMessageBox.showerror(
                "Invalid Entry",
                "You must enter a valid maximum delay.")
            return False
        elif wiredMinDelayText.get() == "" or IsNumeric(wiredMinDelayText.get()) == False:
            tkMessageBox.showerror(
                "Invalid Entry",
                "You must enter a valid minimum delay.")
            return False

        pLoss = float(pLossText.get())
        pDelay = float(wiredProbDelayText.get())

        if pLoss < 0 or pLoss > 1:
            tkMessageBox.showerror(
                "Invalid Entry",
                "Loss probability must be 0 to 1 inclusive.")
        if pDelay < 0 or pDelay > 1:
            tkMessageBox.showerror(
                "Invalid Entry",
                "Wired delay probability must be 0 to 1 inclusive.")

        pStartGood = float(pStartGoodText.get())

        if pStartGood < 0 or pStartGood > 1:
            tkMessageBox.showerror(
                "Invalid Entry",
                "Good start probability must be 0 to 1 inclusive.")

        return True

    def DoSimRuns():
        # Set up the simulation object.
        pLoss = float(pLossText.get())
        pDelay = float(wiredProbDelayText.get())
        pStartGood = float(pStartGoodText.get())
        runs = int(simRunsText.get())

        AppendOutput("Starting simulation...")
        statsList = list()

        for run in range(runs):
            router = Simulation.GetRouter(float(wiredSpeedText.get()), float(wiredBottleneckText.get()), pLoss,
                                          pDelay, float(wiredMinDelayText.get()), float(wiredMaxDelayText.get()))

            channel = Simulation.GetChannel(float(pErrorGoodText.get()), float(pRemainGoodText.get()),
                                            float(pGoodSpeedText.get()), float(pErrorBadText.get()),
                                            float(pRemainBadText.get()),
                                            float(pBadSpeedText.get()), pStartGood)

            sim = Simulation(int(packetsPerRunText.get()), int(minPacketSizeText.get()), int(maxPacketSizeText.get()),
                             channel, router)
            statsList.append(sim.RunSimulation())

        AppendOutput("Done.\n\n")
        CompileResults(runs, statsList)

        # Enable disabled buttons.
        saveButton["state"] = "normal"
        droppedButton["state"] = "normal"
        erroredPlotButton["state"] = "normal"
        bitErrorsPlotButton["state"] = "normal"
        delayPlotButton["state"] = "normal"
        transitPlotButton["state"] = "normal"
        idealTransitPlotButton["state"] = "normal"

        return statsList

    # Build the results.
    def CompileResults(simRuns, resultsList):
        global plotData
        global csv

        # Plot variables.
        plotData = dict()
        plotData["droppedList"] = list()
        plotData["erroredList"] = list()
        plotData["bitErrorList"] = list()
        plotData["delayList"] = list()
        plotData["transitTimeList"] = list()
        plotData["idealTransitTimeList"] = list()
        
        # Total variables.
        droppedPackets = 0.0
        erroredPackets = 0.0
        bitErrors = 0.0
        totalDelay = 0.0
        transitTime = 0.0
        idealTransitTime = 0.0

        run = 1
        csv = "run\tsent\tdropped\terrored\tbitErrors\tdelay\ttransitTime\tidealTransitTime\n"

        # Compile totals.
        for result in resultsList:
            # Build CSV file contents.
            csv += "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\n".format(
                run,
                result["sent"],
                result["dropped"],
                result["erroredPackets"],
                result["totalBitErrors"],
                result["totalDelay"],
                result["transitTime"],
                result["idealTransitTime"]
            )
            run += 1
            
            # Compile plot lists.
            plotData["droppedList"].append(result["dropped"])
            plotData["erroredList"].append(result["erroredPackets"])
            plotData["bitErrorList"].append(result["totalBitErrors"])
            plotData["delayList"].append(result["totalDelay"])
            plotData["transitTimeList"].append(result["transitTime"])
            plotData["idealTransitTimeList"].append(result["idealTransitTime"])
            
            # Calculate totals.
            droppedPackets += result["dropped"]
            erroredPackets += result["erroredPackets"]
            bitErrors += result["totalBitErrors"]
            totalDelay += result["totalDelay"]
            transitTime += result["transitTime"]
            idealTransitTime += result["idealTransitTime"]

        droppedAvg = droppedPackets / simRuns
        errorAvg = erroredPackets / simRuns
        bitErrorAvg = bitErrors / simRuns
        delayAvg = totalDelay / simRuns
        transitAvg = transitTime / simRuns
        idealTransitAvg = idealTransitTime / simRuns

        # Calculate confidence intervals.
        z = 1.96

        droppedError = 0.0
        errorError = 0.0
        bitErrorError = 0.0
        delayError = 0.0
        transitError = 0.0
        idealTransitError = 0.0

        for result in resultsList:
            droppedError = (droppedAvg - result["dropped"]) ** 2
            errorError = (errorAvg - result["erroredPackets"]) ** 2
            bitErrorError = (bitErrorAvg - result["totalBitErrors"]) ** 2
            delayError = (delayAvg - result["totalDelay"]) ** 2
            transitError = (transitAvg - result["transitTime"]) ** 2
            idealTransitError = (idealTransitAvg - result["idealTransitTime"]) ** 2

        droppedMargin = z * (math.sqrt(droppedError) / math.sqrt(simRuns))
        errorMargin = z * (math.sqrt(errorError) / math.sqrt(simRuns))
        bitErrorMargin = z * (math.sqrt(bitErrorError) / math.sqrt(simRuns))
        delayMargin = z * (math.sqrt(delayError) / math.sqrt(simRuns))
        transitMargin = z * (math.sqrt(transitError) / math.sqrt(simRuns))
        idealTransitMargin = z * (math.sqrt(idealTransitError) / math.sqrt(simRuns))

        AppendOutput("Statistics: (Margin of Error = 95% confidence)\n")
        AppendOutput("\tAvg. Dropped Packets: " + str(droppedAvg) + " (+/- " + str(droppedMargin) + ")\n")
        AppendOutput("\tAvg. Errored Packets: " + str(errorAvg) + " (+/- " + str(errorMargin) + ")\n")
        AppendOutput("\tAvg. Bit Errors: " + str(bitErrorAvg) + " (+/- " + str(bitErrorMargin) + ")\n")
        AppendOutput("\tAvg. Delay: " + str(delayAvg) + " (+/- " + str(delayMargin) + ")\n")
        AppendOutput("\tAvg. Transit Time (w/ delays): " + str(transitAvg) + " (+/- " + str(transitMargin) + ")\n")
        AppendOutput("\tAvg. Ideal Transit Time (w/o delays): " + str(idealTransitAvg) + " (+/- " +
                     str(idealTransitMargin) + ")\n")

    # Shows the specified plot.
    def ShowPlot(plot):
        global plotData

        plotter.close()

        if plot == "dropped":
            plotter.figure("Dropped Packets")
            plotter.plot(xrange(1, len(plotData["droppedList"]) + 1), plotData["droppedList"])
            plotter.xlabel("Run (1)")
            plotter.ylabel("Count (1)")
            plotter.title("Dropped Packets")
            plotter.show()
        elif plot == "errored":
            plotter.figure("Errored Packets")
            plotter.plot(xrange(1, len(plotData["erroredList"]) + 1), plotData["erroredList"])
            plotter.xlabel("Run (1)")
            plotter.ylabel("Count (1)")
            plotter.title("Errored Packets")
            plotter.show()
        elif plot == "bitErrors":
            plotter.figure("Total Bit Errors")
            plotter.plot(xrange(1, len(plotData["bitErrorList"]) + 1), plotData["bitErrorList"])
            plotter.xlabel("Run (1)")
            plotter.ylabel("Total (1)")
            plotter.title("Total Bit Errors")
            plotter.show()
        elif plot == "delay":
            plotter.figure("Total Delays")
            plotter.plot(xrange(1, len(plotData["delayList"]) + 1), plotData["delayList"])
            plotter.xlabel("Run (1)")
            plotter.ylabel("Total Delay (ms)")
            plotter.title("Total Delays")
            plotter.show()
        elif plot == "transitTime":
            plotter.figure("Total Transit Time")
            plotter.plot(xrange(1, len(plotData["transitTimeList"]) + 1), plotData["transitTimeList"])
            plotter.xlabel("Run (1)")
            plotter.ylabel("Transit Time (ms)")
            plotter.title("Total Transit Time")
            plotter.show()
        elif plot == "idealTransitTime":
            plotter.figure("Total Ideal Transit Time")
            plotter.plot(xrange(1, len(plotData["transitTimeList"]) + 1), plotData["transitTimeList"])
            plotter.xlabel("Run (1)")
            plotter.ylabel("Ideal Transit Time (ms)")
            plotter.title("Total Ideal Transit Time")
            plotter.show()
        else:
            tkMessageBox.showerror("Invalid Plot Type", "An invalid plot type was selected.")

    # Appends the specified string to the output text area.
    def AppendOutput(value):
        outputText.insert(END, value)

    # Saves the results to the specified file.
    def SaveResults():
        if csv != "":
            f = tkFileDialog.asksaveasfile(mode="w", defaultextension="csv")
            f.write(csv)
            f.close()
        else:
            tkMessageBox.showerror("No Results", "There are no results to save.")
            #tkMessageBox.showinfo("Test", "Saving...")

    # Returns a Boolean indicating whether the specified value is numeric.
    def IsNumeric(value):
        try:
            float(value)
            return True
        except:
            return False

    leftFrame = Frame(mainWindow)
    rightFrame= Frame(mainWindow)

    # Build the channel parameters group.
    channelParams = LabelFrame( leftFrame, text="Channel Parameters")
    channelParams.grid_columnconfigure(0, weight=1)
    channelParams.grid_columnconfigure(1, weight=1)

    Button(channelParams, text="Set Good State...", command=lambda:GetGoodStateParams())\
         .grid(row=0, column=0, padx=5, pady=5, sticky=(N, S, E, W))
    Button(channelParams, text="Set Bad State...", command=lambda:GetBadStateParams()) \
        .grid(row=0, column=1, padx=5, pady=5, sticky=(N, S, E, W))

    Label(channelParams, text="Good Start Probability")\
        .grid(row=1, column=0, padx=5, pady=5, sticky=W)
    Entry(channelParams, textvariable=pStartGoodText) \
        .grid(row=1, column=1, padx=5, pady=5)

    channelParams.grid(row=0, column=0, padx=5, pady=5, sticky=(W, E))

    # Build the router parameters group.
    routerParams = LabelFrame(leftFrame, text="Router Parameters")
    routerParams.grid_columnconfigure(0, weight=1)
    routerParams.grid_columnconfigure(1, weight=1)

    Label(routerParams, text="Loss Probability") \
        .grid(row=0, column=0, padx=5, pady=5, sticky=W)
    Entry(routerParams, textvariable=pLossText) \
        .grid(row=0, column=1, padx=5, pady=5)
    Label(routerParams, text="Wired Speed (b/ms)") \
        .grid(row=1, column=0, padx=5, pady=5, sticky=W)
    Entry(routerParams, textvariable=wiredSpeedText) \
        .grid(row=1, column=1, padx=5, pady=5)
    Label(routerParams, text="Bottleneck Speed (b/ms)") \
        .grid(row=2, column=0, padx=5, pady=5, sticky=W)
    Entry(routerParams, textvariable=wiredBottleneckText) \
        .grid(row=2, column=1, padx=5, pady=5)
    Label(routerParams, text="Wired Add'l. Delay Prob.") \
        .grid(row=3, column=0, padx=5, pady=5, sticky=W)
    Entry(routerParams, textvariable=wiredProbDelayText) \
        .grid(row=3, column=1, padx=5, pady=5)
    Label(routerParams, text="Wired Delay (ms)") \
        .grid(row=4, column=0, padx=5, pady=5, sticky=W)
    Entry(routerParams, textvariable=wiredMinDelayText) \
        .grid(row=4, column=1, padx=5, pady=5)
    Label(routerParams, text="Wired Max. Add'l. Delay (ms)") \
        .grid(row=5, column=0, padx=5, pady=5, sticky=W)
    Entry(routerParams, textvariable=wiredMaxDelayText) \
        .grid(row=5, column=1, padx=5, pady=5)

    routerParams.grid(row=1, column=0, padx=5, pady=5, sticky=(W, E))

    # Build the simulation parameters group.
    simParams = LabelFrame(leftFrame, text="Simulation Parameters")
    simParams.grid_columnconfigure(0, weight=1)
    simParams.grid_columnconfigure(1, weight=1)

    Label(simParams, text="Number of Runs") \
        .grid(row=0, column=0, padx=5, pady=5, sticky=W)
    Entry(simParams, textvariable=simRunsText) \
        .grid(row=0, column=1, padx=5, pady=5)
    Label(simParams, text="Packets per Run (bits)") \
        .grid(row=1, column=0, padx=5, pady=5, sticky=W)
    Entry(simParams, textvariable=packetsPerRunText) \
        .grid(row=1, column=1, padx=5, pady=5)
    Label(simParams, text="Min. Packet Size (bits)") \
        .grid(row=2, column=0, padx=5, pady=5, sticky=W)
    Entry(simParams, textvariable=minPacketSizeText) \
        .grid(row=2, column=1, padx=5, pady=5)
    Label(simParams, text="Max. Packet Size (bits)") \
        .grid(row=3, column=0, padx=5, pady=5, sticky=W)
    Entry(simParams, textvariable=maxPacketSizeText) \
        .grid(row=3, column=1, padx=5, pady=5)
    Button(simParams, text="Run Simulation", command=lambda: RunSimulation()) \
        .grid(row=4, column=0, padx=5, pady=5, sticky=(N, S, E, W))
    saveButton = Button(simParams, text="Save Results...", state=DISABLED, command=lambda: SaveResults())
    saveButton.grid(row=4, column=1, padx=5, pady=5, sticky=(N, S, E, W))

    simParams.grid(row=2, column=0, padx=5, pady=5, sticky=(W, E))

    # Build the results group.
    results = LabelFrame(rightFrame, text="Results")
    results.grid_propagate(False)

    # Text area.
    textArea = Frame(results)
    textArea.grid_rowconfigure(0, weight=1)
    textArea.grid_columnconfigure(0, weight=1)
    hScroll = Scrollbar(textArea, orient=HORIZONTAL)
    hScroll.grid(row=1, column=0, sticky=(E, W))
    vScroll = Scrollbar(textArea)
    vScroll.grid(row=0, column=1, sticky=(N, S))
    outputText = Text(textArea, wrap=NONE, xscrollcommand=hScroll.set, yscrollcommand=vScroll.set, height=3)
    outputText.grid(row=0, column=0, sticky=(N, S, E, W))
    hScroll.configure(command=outputText.xview)
    vScroll.configure(command=outputText.yview)
    textArea.grid(row=0, column=0, padx=5, pady=5, sticky=(N, S, E, W))

    # Plot area.
    plotButtons = LabelFrame(rightFrame, text="Show Plots")
    droppedButton = Button(plotButtons, text="Dropped Packets", state=DISABLED,
        command=lambda: ShowPlot("dropped"))
    droppedButton.grid(row=0, column=0, padx=5, pady=5, sticky=(N, S, E, W))
    erroredPlotButton = Button(plotButtons, text="Errored Packets", state=DISABLED,
        command=lambda: ShowPlot("errored"))
    erroredPlotButton.grid(row=0, column=1, padx=5, pady=5, sticky=(N, S, E, W))
    bitErrorsPlotButton = Button(plotButtons, text="Bit Errors", state=DISABLED,
        command=lambda: ShowPlot("bitErrors"))
    bitErrorsPlotButton.grid(row=0, column=2, padx=5, pady=5, sticky=(N, S, E, W))
    delayPlotButton = Button(plotButtons, text="Delay", state=DISABLED,
        command=lambda: ShowPlot("delay"))
    delayPlotButton.grid(row=0, column=3, padx=5, pady=5, sticky=(N, S, E, W))
    transitPlotButton = Button(plotButtons, text="Transit Time", state=DISABLED,
        command=lambda: ShowPlot("transitTime"))
    transitPlotButton.grid(row=0, column=4, padx=5, pady=5, sticky=(N, S, E, W))
    idealTransitPlotButton = Button(plotButtons, text="Ideal Transit Time", state=DISABLED,
        command=lambda: ShowPlot("idealTransitTime"))
    idealTransitPlotButton.grid(row=0, column=5, padx=5, pady=5, sticky=(N, S, E, W))

    plotButtons.grid(row=1, column=0, padx=5, pady=5, sticky=(N, S, E, W))

    results.grid_columnconfigure(0, weight=1)
    results.grid_rowconfigure(0, weight=1)
    results.grid(row=0, column=0, padx=5, pady=5, sticky=(N, S, E, W))

    rightFrame.grid_columnconfigure(0, weight=1)
    rightFrame.grid_rowconfigure(0, weight=1)

    # Configure main window weights.
    mainWindow.grid_columnconfigure(1, weight=1)
    mainWindow.grid_rowconfigure(0, weight=1)

    leftFrame.grid(row=0, column=0, sticky=(N, S, E, W))
    rightFrame.grid(row=0, column=1, sticky=(N, S, E, W))

    mainloop()