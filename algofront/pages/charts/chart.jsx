import * as d3 from "d3";
import { useState, useContext, useEffect } from "react";
import { ChartContext } from "./_chartcontext";
import { XAxis } from "./xaxis";
import { YAxis } from "./yaxis";
import { CandleStickChart } from "./candlestickchart";
import { ToolTipContext } from "./_tooltipcontext";
import { ToolTip } from "./tooltip";

export default function Chart(props) {
  const { data } = props;

  const prefs = {
    containerWidth: 700,
    containerHeight: 500,
    padding: 0.5,
    xTickCount: 700 / 40,
    yTickCount: 20,
    containerMargin: {
      top: 50,
      bottom: 40,
      left: 60,
      right: 40,
    },
  };
  const xDomain = data.map((d) => new Date(d.datetime));
  const yDomain = [
    d3.min(data, (d) => d.l) - 10,
    d3.max(data, (d) => d.h) + 10,
  ];

  const [TTData, setTTData] = useState(null);

  const callSetTTData = (data) => {
    setTTData(data);
  };

  return (
    <ChartContext.Provider value={prefs}>
      <ToolTipContext.Provider
        value={{ data: {}, updateTTData: callSetTTData }}
      >
        <ToolTip data={TTData} width={prefs.containerWidth} />
        <svg
          className="candlestick-chart"
          width={prefs.containerWidth}
          height={prefs.containerHeight}
          viewBox={`0, 0, ${prefs.containerWidth}, ${prefs.containerHeight}`}
        >
          <CandleStickChart data={data} xDomain={xDomain} yDomain={yDomain} />
          <XAxis xDomain={xDomain} tickCount={prefs.xTickCount} />
          <YAxis yDomain={yDomain} tickCount={prefs.yTickCount} />
        </svg>
      </ToolTipContext.Provider>
    </ChartContext.Provider>
  );
}
