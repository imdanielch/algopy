import * as d3 from "d3";
import { useEffect, useRef, useContext, useState } from "react";
import { ChartContext } from "./_chartcontext";
import { CandleStick } from "./candlestick";

export const CandleStickChart = ({ data, xDomain, yDomain }) => {
  const prefs = useContext(ChartContext);
  const height = prefs.containerHeight;
  const width = prefs.containerWidth;
  const { left, right, top, bottom } = prefs.containerMargin;
  const containerRef = useRef(null);

  const [candlesticks, setCandlesticks] = useState(null);

  useEffect(() => {
    //d3.select(containerRef.current).selectAll('*').remove();

    const x = d3
      .scaleBand()
      .domain(xDomain)
      .rangeRound([left, width - right])
      .padding(prefs.padding);

    const y1 = d3
      .scaleLinear()
      .domain(yDomain)
      .range([
        height - prefs.containerMargin.bottom,
        prefs.containerMargin.top,
      ]);

    const candlestick_group = data.map((d, index) => {
      const scaled = {
        y: d.o > d.c ? y1(d.o) : y1(d.c),
        yo: y1(d.o),
        yh: y1(d.h),
        yl: y1(d.l),
        yc: y1(d.c),
        x: x(new Date(d.datetime)),
        containerWidth: width,
        containerHeight: height,
        marginTop: top,
        marginBottom: bottom,
        width: x.bandwidth(),
        height: Math.abs(y1(d.o) - y1(d.c)),
        isLong: d.o < d.c,
      };

      return <CandleStick key={index} data={scaled} tt={d} />;
    });
    setCandlesticks(candlestick_group);
  }, [
    prefs.containerMargin.bottom,
    prefs.containerMargin.top,
    prefs.padding,
    data,
    height,
    left,
    right,
    top,
    bottom,
    width,
    xDomain,
    yDomain,
  ]);

  return (
    <g className="candlestick-chart-data" ref={containerRef}>
      {candlesticks}
    </g>
  );
};
